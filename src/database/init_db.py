"""
Initialize database - create all tables
"""

from src.database.database import engine, Base
from src.database.models import Resume, JobDescription, Match, User

def init_database():
    """Create all database tables"""
    print("="*70)
    print("INITIALIZING DATABASE")
    print("="*70)
    
    print("\nCreating tables...")
    Base.metadata.create_all(bind=engine)
    
    print("✓ Tables created successfully!")
    print("\nCreated tables:")
    print("  • resumes")
    print("  • job_descriptions")
    print("  • matches")
    print("  • users")
    
    print("\n" + "="*70)
    print("DATABASE READY")
    print("="*70)

if __name__ == "__main__":
    init_database()