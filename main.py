from fastapi import FastAPI
from app.views import router
from service_config import settings

app = FastAPI(
    debug=settings.debug,
    title=settings.project_name,
    version=settings.version
)

app.include_router(router)


@app.get("/")
async def version():
    return settings.version
