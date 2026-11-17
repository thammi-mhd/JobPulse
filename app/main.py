from fastapi import FastAPI, status

from app.api.v1.router import router as api_router


app = FastAPI(
    title="JobPulse",
    description="JobPulse is a job search platform that helps users find their dream jobs by providing personalized job recommendations, company insights, and career resources.",
    version="0.1.0",
)

app.include_router(api_router,
                   prefix="/api/v1",)

@app.get("/", status_code=status.HTTP_200_OK) 
async def home():
    return {
        "message": "welcome to JobPulse",
        "status": "success"
    }

@app.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    return {
        "message": "JobPulse is healthy and running",
        "status": "success"
    }

