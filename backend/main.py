from fastapi import FastAPI

from backend.api.auth import router

app = FastAPI(

    title="KeyShield AI"

)

app.include_router(router)