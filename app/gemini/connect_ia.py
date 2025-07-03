import getpass
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI,GoogleGenerativeAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

GOOGLE_API_KEY= os.getenv("GOOGLE_API_KEY")
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS") #la librería oficial de Google (que LangChain usa por debajo) automáticamente carga esa cuenta de servicio y la usa para autenticarte.



llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-001")

embedding_model = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001",  # Este es el modelo oficial de embeddings de Gemini
)

async def invoke(sentece):
    print(sentece)
    messages = [
        ("system", "Translate the user sentence to French."),
        ("human", sentece),

    ]
    print(llm.invoke(messages))


async def splitter_text(text:str):
    # print(text)
    # 1. Configuramos el splitter:
    #    - chunk_size: tamaño máximo de cada fragmento en caracteres.
    #    - chunk_overlap: solapamiento en caracteres entre fragmentos adyacentes,
    #      útil para no perder contexto en los límites.
    #    - separators: orden de prioridad para dividir el texto (párrafos, líneas,
    #      puntos, espacios, y finalmente carácter a carácter si no queda otra).
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,    # Máximo 1000 caracteres por chunk
        chunk_overlap=200,     # 200 caracteres de solapamiento
        separators=["\n\n", "\n", ".", " ", ""]  
    )
    # 2. Dividimos el texto usando la configuración anterior
    chunks = text_splitter.split_text(text)

    return chunks     


async def save_data_in_chroma(user_id,doc_id,chuncks):
    # Chroma.from_texts(...) es una forma rápida de construir una base vectorial desde cero.

    # Un chunk es simplemente un fragmento de texto, es decir, una porción dividida del texto original para poder procesarlo mejor.

    # Guarda los chunks de texto en una base vectorial (Chroma),
    # generando embeddings y asignando metadatos por usuario y documento.
    
    # Parámetros:
    # - user_id: ID del usuario dueño del documento.
    # - doc_id: ID del documento al que pertenecen los chunks.
    # - chuncks: Lista de textos (strings) previamente divididos con el splitter.
    
     # 1. Creamos una lista de metadatos, uno por chunk.
    #    Cada metadata guarda el ID de usuario y de documento.


    metadatas = [{"user_id": user_id, "doc_id": doc_id} for _ in chuncks]

     # 2. Creamos una instancia de Chroma a partir de los textos.
    #    Esto:
    #    - genera automáticamente los embeddings usando embedding_model,
    #    - asocia los metadatos a cada chunk,
    #    - guarda los datos en el directorio "db_fabrica".
    Chroma.from_texts(
        texts=chuncks,  # Lista de chunks de texto
        embedding=embedding_model,
        persist_directory="db_fabrica", # Carpeta donde se guarda la base vectorial
        metadatas=metadatas  # Lista de metadatos por chunk
    )



async def ask_question(user_id: str, question: str, doc_ids: list[str] | None = None, top_k: int = 4):

    """
    Recupera los chunks más relevantes (embeddings) desde Chroma según una pregunta,
    filtra por user_id y opcionalmente por uno o varios doc_ids,
    y genera una respuesta con base únicamente en esos documentos.

    Parámetros:
    - user_id: ID del usuario que hizo la consulta.
    - question: Pregunta que se quiere responder.
    - doc_ids: Lista opcional de IDs de documentos específicos para filtrar.
    - top_k: Número de chunks más similares que se quieren recuperar.

    Retorna:
    - Respuesta generada por el modelo LLM (Gemini) basada solo en el contexto recuperado.
    """

    # 1. Conectamos a la base vectorial local (Chroma) con el modelo de embeddings configurado.

    vectorstore = Chroma(
        persist_directory="db_fabrica", # Carpeta donde se guardan los vectores
        embedding_function=embedding_model
    )

    # 2. Construimos el filtro para limitar la búsqueda:
    #    Si hay doc_ids, usamos un filtro compuesto con $and
    filter_kwargs = {"user_id": user_id}
    if doc_ids:
        filter_kwargs = {
            "$and": [
                {"user_id": user_id},
                {"doc_id": {"$in": doc_ids}}
            ]
        }
    else:
        filter_kwargs = {"user_id": user_id}
    # 3. Hacemos la búsqueda semántica:
    #    Busca los top_k chunks más similares a la pregunta, filtrando por metadatos.
    docs = vectorstore.similarity_search(
        query=question,
        k=top_k,
        filter=filter_kwargs
    )
    contexto = "\n\n".join([doc.page_content for doc in docs])
    
    prompt = [
        ("system","Responde SOLO con base en el siguiente contexto:"),
        ("human", f"{contexto}\n\nPregunta: {question}")
    ]
     # 6. Invocamos al modelo y retornamos la respuesta
    return llm.invoke(prompt)