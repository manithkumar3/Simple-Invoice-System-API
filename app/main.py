from fastapi import FastAPI
from app.api_endpoints.routes import router
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="Invoice API's.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/")
async def root():
    return {"message": "Welcome to Invoice API's."}
