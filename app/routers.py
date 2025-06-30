import importlib
import pkgutil
from fastapi import APIRouter

api_router = APIRouter()

package = "app.modules"

for loader, module_name, is_pkg in pkgutil.iter_modules(["app/modules"]):
    try:
        module_path = f"{package}.{module_name}.router"
        module = importlib.import_module(module_path)
        router = getattr(module, "router", None)
        if router:
            print(f"✅ Router cargado: {module_path}")
            api_router.include_router(router)
        else:
            print(f"⚠️  No se encontró 'router' en {module_path}")
    except ModuleNotFoundError as e:
        print(f"❌ Error importando {module_name}: {e}")