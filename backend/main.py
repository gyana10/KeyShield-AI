from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api.authenticate import router as auth_ai_router
from backend.api.auth import router as auth_router
from backend.api.enrollment import router as enroll_router

app = FastAPI(
    title="KeyShield AI",
    version="0.1.0"
)

# Allow frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API Routers
app.include_router(auth_router)
app.include_router(enroll_router)
app.include_router(auth_ai_router)


@app.get("/")
def root():
    return {
        "message": "Welcome to KeyShield AI API 🚀"
    }