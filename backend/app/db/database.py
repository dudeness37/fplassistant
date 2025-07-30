"""
Database connection and session management for FPL Assistant - psycopg3 compatible
"""
import os
from typing import Generator
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import logging

logger = logging.getLogger(__name__)

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is required")

# For psycopg3, we need to use the psycopg:// scheme
if DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg://", 1)

# Create engine with optimized settings for Neon
engine = create_engine(
    DATABASE_URL,
    # Connection pool settings optimized for serverless
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True,
    pool_recycle=300,  # 5 minutes
    echo=False,  # Set to True for SQL debugging
)

# Create sessionmaker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

def get_db() -> Generator[Session, None, None]:
    """
    Database session dependency for FastAPI
    """
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error(f"Database session error: {e}")
        db.rollback()
        raise
    finally:
        db.close()

def test_connection() -> bool:
    """
    Test database connection
    """
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            logger.info("Database connection successful")
            return True
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        return False

def get_table_counts() -> dict:
    """
    Get row counts for all main tables (useful for monitoring)
    """
    tables = [
        'teams', 'players', 'fixtures', 'player_gameweek_stats',
        'match_statistics', 'player_match_stats', 'match_odds',
        'team_feature_ratings', 'player_feature_ratings'
    ]
    
    counts = {}
    try:
        with engine.connect() as conn:
            for table in tables:
                try:
                    result = conn.execute(text(f"SELECT COUNT(*) FROM {table}"))
                    counts[table] = result.scalar()
                except Exception as e:
                    counts[table] = f"Error: {e}"
        return counts
    except Exception as e:
        logger.error(f"Failed to get table counts: {e}")
        return {}

class DatabaseManager:
    """
    Utility class for database operations
    """
    
    @staticmethod
    def upsert_record(db: Session, model_class, data: dict, unique_fields: list):
        """
        Insert or update a record based on unique fields
        
        Args:
            db: Database session
            model_class: SQLAlchemy model class
            data: Dictionary of field values
            unique_fields: List of fields that determine uniqueness
        """
        try:
            # Build filter conditions
            filters = {field: data[field] for field in unique_fields if field in data}
            
            # Check if record exists
            existing = db.query(model_class).filter_by(**filters).first()
            
            if existing:
                # Update existing record
                for key, value in data.items():
                    if hasattr(existing, key):
                        setattr(existing, key, value)
                db.commit()
                logger.debug(f"Updated {model_class.__name__} with {filters}")
                return existing
            else:
                # Create new record
                new_record = model_class(**data)
                db.add(new_record)
                db.commit()
                db.refresh(new_record)
                logger.debug(f"Created new {model_class.__name__} with {filters}")
                return new_record
                
        except Exception as e:
            db.rollback()
            logger.error(f"Upsert failed for {model_class.__name__}: {e}")
            raise
    
    @staticmethod
    def bulk_upsert(db: Session, model_class, records: list, unique_fields: list):
        """
        Bulk insert/update records efficiently
        """
        try:
            created_count = 0
            updated_count = 0
            
            for record_data in records:
                filters = {field: record_data[field] for field in unique_fields if field in record_data}
                existing = db.query(model_class).filter_by(**filters).first()
                
                if existing:
                    for key, value in record_data.items():
                        if hasattr(existing, key):
                            setattr(existing, key, value)
                    updated_count += 1
                else:
                    new_record = model_class(**record_data)
                    db.add(new_record)
                    created_count += 1
            
            db.commit()
            logger.info(f"Bulk upsert completed: {created_count} created, {updated_count} updated")
            return {"created": created_count, "updated": updated_count}
            
        except Exception as e:
            db.rollback()
            logger.error(f"Bulk upsert failed: {e}")
            raise