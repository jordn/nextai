from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

errors = []

@app.get("/error")
def handle_error(error):
    print("Got error", error)
    errors.append(error)

@app.get("/errors")
def get_errors():
    return errors

@app.delete("/errors")
def clear_errors():
    global errors
    errors = []
    return

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
