from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Date
import logging

logger = logging.getLogger(__name__)

SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    department = Column(String, nullable=False)
    salary = Column(Integer, nullable=False)
    hire_date = Column(Date, nullable=False)
    position = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)


class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    budget = Column(Integer, nullable=False)
    location = Column(String, nullable=False)


def init_db(db):
    try:
        # Create tables
        Base.metadata.create_all(bind=engine)

        # Check if data exists using text()
        result = db.execute(text("SELECT COUNT(*) FROM employees")).scalar()

        if result == 0:
            # Insert sample employees
            db.execute(
                text("""
                    INSERT INTO employees (name, department, salary, hire_date, position, email)
                    VALUES 
                        (:name1, :dept1, :salary1, :date1, :pos1, :email1),
                        (:name2, :dept2, :salary2, :date2, :pos2, :email2)
                """),
                {
                    "name1": "John Doe",
                    "dept1": "Engineering",
                    "salary1": 85000,
                    "date1": "2020-01-15",
                    "pos1": "Senior Developer",
                    "email1": "john.doe@company.com",
                    "name2": "Jane Smith",
                    "dept2": "Marketing",
                    "salary2": 75000,
                    "date2": "2019-03-20",
                    "pos2": "Marketing Manager",
                    "email2": "jane.smith@company.com"
                }
            )

        # Check departments
        result = db.execute(text("SELECT COUNT(*) FROM departments")).scalar()

        if result == 0:
            # Insert sample departments
            db.execute(
                text("""
                    INSERT INTO departments (name, budget, location)
                    VALUES 
                        (:name1, :budget1, :loc1),
                        (:name2, :budget2, :loc2)
                """),
                {
                    "name1": "Engineering",
                    "budget1": 1000000,
                    "loc1": "Building A",
                    "name2": "Marketing",
                    "budget2": 500000,
                    "loc2": "Building B"
                }
            )

        db.commit()
        logger.info("Database initialized successfully")

    except Exception as e:
        db.rollback()
        logger.error(f"Error initializing database: {str(e)}")
        raise