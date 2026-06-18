from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.validate import router as validate_router
from routes.upload import router as upload_router
from routes.chunk import router as chunk_router

app = FastAPI(title="TransactIQ AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload_router, prefix="/api")
app.include_router(validate_router, prefix="/api")
app.include_router(
    chunk_router,
    prefix="/api"
)

@app.get("/")
def home():
    return {
        "message": "Backend Running Successfully"
    }

