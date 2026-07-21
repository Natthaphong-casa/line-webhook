from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {
        "status": "Visitor Registration API Running",
        "version": "2.0"
    }


@app.get("/health")
def health():
    return {
        "status": "ok"
    }
