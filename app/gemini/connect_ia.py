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
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,    
        chunk_overlap=200,    
        separators=["\n\n", "\n", ".", " ", ""]  
    )

    chunks = text_splitter.split_text(text)

    for i, chunk in enumerate(chunks):
        print(f"Chunk {i}:\n{chunk}\n{'-'*40}")
    return chunks     


async def save_data_in_chroma(user_id,doc_id,chuncks):
    metadatas = [{"user_id": user_id, "doc_id": doc_id} for _ in chuncks]
    vectorstore = Chroma.from_texts(
        texts=chuncks,
        embedding=embedding_model,
        persist_directory="db_fabrica",
        metadatas=metadatas
    )
    # vectorstore.persist()


async def ask_question(user_id: str, question: str, doc_ids: list[str] | None = None, top_k: int = 4):
    vectorstore = Chroma(
        persist_directory="db_fabrica",
        embedding_function=embedding_model
    )
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
    return llm.invoke(prompt)