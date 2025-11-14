import uvicorn
from fastapi import FastAPI

from Backend.auth.routes import router as auth_router
from Backend.roles.routes import router as role_router
from Backend.permissions.routes import router as permission_router
from Backend.Rag.api import router as rag_router

from Backend.Database.connections import Base, engine
from Backend.Database import models

app = FastAPI(title="RBAC RAG System")

app.include_router(auth_router)
app.include_router(role_router)
app.include_router(permission_router)
app.include_router(rag_router)

@app.get("/")
def root():
    return {"msg": "RBAC RAG Chatbot API running"}

# Create DB tables
Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    uvicorn.run("Backend.main:app", host="127.0.0.1", port=8000, reload=True)
