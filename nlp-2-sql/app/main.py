from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text
from datetime import datetime
import importlib.util
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Check for required packages
required_packages = ['spacy', 'sqlalchemy']
missing_packages = []

for package in required_packages:
    if importlib.util.find_spec(package) is None:
        missing_packages.append(package)

if missing_packages:
    logger.error(f"Missing required packages: {', '.join(missing_packages)}")
    logger.error("Please install required packages using: pip install -r requirements.txt")
    raise ImportError(f"Missing required packages: {', '.join(missing_packages)}")

# Now import the rest of the dependencies
from . import models, database
from .nlp_parser import NLQueryParser

app = FastAPI(title="NLP Database Query API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize NLP Parser
try:
    query_parser = NLQueryParser()
except Exception as e:
    logger.error(f"Error initializing NLP Parser: {str(e)}")
    query_parser = None


# Dependency to get database session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "nlp_parser": "loaded" if query_parser else "not loaded"
    }


@app.post("/query", response_model=models.QueryResult)
async def execute_query(query: models.Query, db: Session = Depends(get_db)):
    if not query_parser:
        raise HTTPException(
            status_code=500,
            detail="NLP Parser not initialized. Please ensure spaCy is installed correctly."
        )

    try:
        start_time = datetime.now()

        # Parse natural language to SQL
        sql_query = query_parser.parse_query(query.text)
        logger.info(f"Generated SQL query: {sql_query}")

        # Execute raw SQL query using text()
        result = db.execute(text(sql_query))

        # Get column names from result
        columns = result.keys()

        # Fetch all rows
        rows = result.fetchall()

        # Convert rows to list of dictionaries
        results = [dict(zip(columns, row)) for row in rows]

        execution_time = (datetime.now() - start_time).total_seconds()

        return models.QueryResult(
            sql_query=sql_query,
            results=results,
            execution_time=execution_time
        )
    except Exception as e:
        logger.error(f"Error executing query: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# Initialize database
@app.on_event("startup")
async def startup_event():
    try:
        db = next(get_db())
        if db.query(database.Employee).count() == 0:
            logger.info("Initializing database with sample data...")
            database.init_db(db)
        logger.info("Database initialization completed")
    except Exception as e:
        logger.error(f"Error during startup: {str(e)}")