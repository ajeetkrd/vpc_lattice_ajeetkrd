#!/usr/bin/env python3
"""
FastAPI Server for Insurance Database Queries
Provides API endpoints to query user and policy information from MySQL database
"""

import logging
from typing import Dict, List, Optional, Union
import mysql.connector
from mysql.connector.cursor import MySQLCursorDict
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from contextlib import asynccontextmanager
import uvicorn
from datetime import date, datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("insurance-api-server")

# Database configuration
DB_CONFIG = {
    'host': '<update>',
    'database': 'policydb',
    'user': 'admin',  # Changed from 'postgres' to 'root' (common MySQL default)
    'password': '<update>',
    'port': 3306,  # Changed from 5432 to 3306 (MySQL default port)
    'autocommit': True
}

# Pydantic models for request/response
class UserResponse(BaseModel):
    user_id: int
    first_name: str
    last_name: str
    email: str
    phone: Optional[str] = None
    date_of_birth: Optional[Union[date, str]] = None
    policy_number: str
    policy_type: str
    premium_amount: Optional[float] = None
    policy_start_date: Optional[Union[date, str]] = None
    policy_end_date: Optional[Union[date, str]] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    created_at: Optional[Union[datetime, str]] = None
    updated_at: Optional[Union[datetime, str]] = None

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None,
            date: lambda v: v.isoformat() if v else None
        }

class PolicyResponse(BaseModel):
    policy_id: int
    user_id: int
    policy_number: str
    policy_type: str
    policy_status: str
    premium_amount: float
    coverage_amount: Optional[float] = None
    deductible_amount: Optional[float] = None
    policy_start_date: Union[date, str]
    policy_end_date: Union[date, str]
    payment_frequency: str
    agent_name: Optional[str] = None
    agent_phone: Optional[str] = None
    policy_description: Optional[str] = None
    created_at: Optional[Union[datetime, str]] = None
    updated_at: Optional[Union[datetime, str]] = None

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None,
            date: lambda v: v.isoformat() if v else None
        }

class DatabaseConnection:
    def __init__(self):
        self.connection = None

    def connect(self):
        try:
            logger.info(f"Attempting to connect to MySQL host: {DB_CONFIG['host']}:{DB_CONFIG['port']}")
            self.connection = mysql.connector.connect(**DB_CONFIG)
            return True
        except Exception as e:
            logger.error(f"Database connection failed: {e}")
            return False

    def disconnect(self):
        if self.connection:
            self.connection.close()

    def execute_query(self, query: str, params: tuple = None) -> List[Dict]:
        try:
            if not self.connection or not self.connection.is_connected():
                if not self.connect():
                    return []

            cursor = self.connection.cursor(dictionary=True)  # MySQL equivalent of RealDictCursor
            cursor.execute(query, params)
            results = cursor.fetchall()
            cursor.close()

            # Convert datetime and date objects to strings for JSON serialization
            serialized_results = []
            for row in results:
                row_dict = dict(row)
                for key, value in row_dict.items():
                    if isinstance(value, datetime):
                        row_dict[key] = value.isoformat()
                    elif isinstance(value, date):
                        row_dict[key] = value.isoformat()
                serialized_results.append(row_dict)

            return serialized_results
        except Exception as e:
            logger.error(f"Query execution failed: {e}")
            return []

# Initialize database connection
db = DatabaseConnection()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting up Insurance API server...")
    if not db.connect():
        logger.error("Failed to connect to database on startup")
    else:
        logger.info("Database connection established")
    yield
    # Shutdown
    logger.info("Shutting down Insurance API server...")
    db.disconnect()

# Create FastAPI app with lifespan
app = FastAPI(
    title="Insurance Database API",
    version="1.0.0",
    lifespan=lifespan
)

@app.get("/")
async def root():
    return {"message": "Insurance Database API", "version": "1.0.0"}

@app.get("/users/{user_id}")
async def get_user_by_id(user_id: int):
    """Get user details by user ID"""
    query = "SELECT * FROM insurance_users WHERE user_id = %s"
    results = db.execute_query(query, (user_id,))

    if not results:
        raise HTTPException(status_code=404, detail="User not found")

    return results

@app.get("/users/email/{email}")
async def get_user_by_email(email: str):
    """Get user details by email address"""
    query = "SELECT * FROM insurance_users WHERE email = %s"
    results = db.execute_query(query, (email,))

    if not results:
        raise HTTPException(status_code=404, detail="User not found")

    return results

@app.get("/users/search/{name}")
async def search_users(name: str):
    """Search users by name (first or last name)"""
    search_term = f"%{name}%"
    query = """
    SELECT * FROM insurance_users
    WHERE first_name LIKE %s OR last_name LIKE %s
    """
    results = db.execute_query(query, (search_term, search_term))

    if not results:
        raise HTTPException(status_code=404, detail="No users found")

    return results

@app.get("/policies/{policy_number}")
async def get_policy_by_number(policy_number: str):
    """Get policy details by policy number"""
    query = "SELECT * FROM policies_summ WHERE policy_number = %s"
    results = db.execute_query(query, (policy_number,))

    if not results:
        raise HTTPException(status_code=404, detail="Policy not found")

    return results

@app.get("/policies/user/{user_id}")
async def get_policies_by_user(user_id: int):
    """Get all policies for a specific user"""
    query = "SELECT * FROM policies_summ WHERE user_id = %s"
    results = db.execute_query(query, (user_id,))

    if not results:
        raise HTTPException(status_code=404, detail="No policies found for this user")

    return results

@app.get("/policies/status/{status}")
async def get_policies_by_status(status: str):
    """Get all policies with a specific status"""
    if status not in ['Active', 'Expired', 'Cancelled', 'Pending']:
        raise HTTPException(status_code=400, detail="Invalid status")

    query = "SELECT * FROM policies_summ WHERE policy_status = %s"
    results = db.execute_query(query, (status,))

    if not results:
        raise HTTPException(status_code=404, detail="No policies found with this status")

    return results

@app.get("/policies/type/{policy_type}")
async def get_policies_by_type(policy_type: str):
    """Get all policies of a specific type"""
    if policy_type not in ['Auto', 'Home', 'Life', 'Health', 'Business']:
        raise HTTPException(status_code=400, detail="Invalid policy type")

    query = "SELECT * FROM policies_summ WHERE policy_type = %s"
    results = db.execute_query(query, (policy_type,))

    if not results:
        raise HTTPException(status_code=404, detail="No policies found with this type")

    return results

if __name__ == "__main__":
    uvicorn.run("mcp:app", host="127.0.0.1", port=8000, reload=True)
