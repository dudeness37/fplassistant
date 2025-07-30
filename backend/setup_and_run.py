"""
Setup and run script for FPL Assistant backend
This script will:
1. Check environment variables
2. Test database connection  
3. Run the initial data ingestion
4. Start the API server
"""
import os
import sys
import subprocess
import logging
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def check_environment():
    """Check required environment variables"""
    required_vars = [
        "DATABASE_URL",
        "SPORTMONKS_API_KEY", 
        "ODDS_API_KEY"
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        logger.error(f"Missing required environment variables: {missing_vars}")
        logger.error("Please set these in your infra/.env file")
        return False
    
    logger.info("✅ All required environment variables are set")
    return True

def install_requirements():
    """Install Python requirements"""
    try:
        logger.info("Installing Python requirements...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                      check=True, capture_output=True)
        logger.info("✅ Requirements installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to install requirements: {e}")
        return False

def test_database_connection():
    """Test database connection"""
    try:
        # Add app to path
        sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))
        
        from db.database import test_connection
        
        if test_connection():
            logger.info("✅ Database connection successful")
            return True
        else:
            logger.error("❌ Database connection failed")
            return False
            
    except Exception as e:
        logger.error(f"Database connection test failed: {e}")
        return False

def run_data_ingestion():
    """Run the initial data ingestion"""
    try:
        logger.info("🚀 Starting data ingestion...")
        
        # Run the ingestion script
        script_path = os.path.join(os.path.dirname(__file__), "scripts", "ingest_all_data.py")
        result = subprocess.run([sys.executable, script_path], 
                              capture_output=False, text=True)
        
        if result.returncode == 0:
            logger.info("✅ Data ingestion completed successfully")
            return True
        else:
            logger.error("❌ Data ingestion failed")
            return False
            
    except Exception as e:
        logger.error(f"Data ingestion failed: {e}")
        return False

def start_api_server():
    """Start the FastAPI server"""
    try:
        logger.info("🚀 Starting FastAPI server...")
        
        # Start uvicorn server
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "app.main:app", 
            "--host", "0.0.0.0", 
            "--port", "8000", 
            "--reload"
        ])
        
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Failed to start server: {e}")

def main():
    """Main setup and run function"""
    logger.info("🔧 FPL Assistant Backend Setup")
    logger.info("=" * 50)
    
    # Step 1: Check environment
    if not check_environment():
        logger.error("Environment check failed. Please fix the issues above.")
        return
    
    # Step 2: Install requirements
    if not install_requirements():
        logger.error("Failed to install requirements")
        return
    
    # Step 3: Test database
    if not test_database_connection():
        logger.error("Database connection failed. Please check your DATABASE_URL")
        return
    
    # Step 4: Ask user if they want to run data ingestion
    response = input("\n🤔 Do you want to run initial data ingestion? (y/n): ").lower().strip()
    
    if response in ['y', 'yes']:
        if not run_data_ingestion():
            logger.error("Data ingestion failed")
            response = input("Do you want to continue and start the API server anyway? (y/n): ").lower().strip()
            if response not in ['y', 'yes']:
                return
    else:
        logger.info("Skipping data ingestion")
    
    # Step 5: Start API server
    logger.info("\n🚀 Starting API server...")
    start_api_server()

if __name__ == "__main__":
    main()