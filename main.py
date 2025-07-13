import os
import dotenv
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, Header, Depends
from fastapi.middleware.cors import CORSMiddleware

dotenv.load_dotenv()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or replace "*" with ["http://localhost:5173"] for stricter security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_KEY_Credits = {os.getenv("API_KEY"): 1000}
print("API_KEY_Credits:", API_KEY_Credits)


def check_api_key(api_key: str = Header(None)):
    """
    Middleware to check API key.
    """
    credits = API_KEY_Credits.get(api_key, 0)
    if credits <= 0:
        raise HTTPException(status_code=401, detail="Invalid API Key")

    return api_key


@app.get("/")
async def read_root():
    return {"message": "Welcome to the FastAPI application!"}


class JobContext(BaseModel):
    role_title: str
    company: str
    role_description: str
    required_skills: str
    years_of_experience: int


@app.post("/startInterview")
async def start_interview_api(job: JobContext, api_key: str = Depends(check_api_key)):
    """
    Initialize chat and return first interview question.
    """
    API_KEY_Credits[api_key] -= 1
    print("Remaining Credits:", API_KEY_Credits[api_key])

    return {
        "question": "Amazon has come a long way since opening on the World Wide Web in July 1995. Today, we operate retail websites in multiple countries across geographies, offering products in many categories (books, media, digital, electronics etc.) worldwide, and we still like to work hard, have fun and make history! The Amazon.com brand has become synonymous with a superior level of convenience, selection, low prices, and customer service. We are looking for Fresh College Graduate or software engineers with less than 1 year of Software engineering experience involving solving complex problems."
    }
