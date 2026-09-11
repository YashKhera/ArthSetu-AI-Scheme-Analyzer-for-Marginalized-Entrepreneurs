"""
Database migration script to create schemes_v2 table
Run this to add the new comprehensive scheme structure
"""
from sqlalchemy import create_engine, inspect
from app.database import Base, engine
from app.config import settings
from app.models.scheme_v2 import SchemeV2, EligibilityRule
from data.schemes_seed_v2 import seed_schemes_v2

def migrate_to_v2():
    """Create v2 tables and seed data"""
    print("=" * 60)
    print("Database Migration: Creating schemes_v2 tables")
    print("=" * 60)

    # Check if tables exist
    inspector = inspect(engine)
    existing_tables = inspector.get_table_names()

    print(f"\nExisting tables: {existing_tables}")

    # Create v2 tables
    print("\nCreating schemes_v2 and eligibility_rules tables...")
    Base.metadata.create_all(bind=engine, tables=[
        SchemeV2.__table__,
        EligibilityRule.__table__
    ])

    print("[OK] Tables created successfully!")

    # Seed data
    print("\nSeeding comprehensive scheme data...")
    seed_schemes_v2()

    print("\n" + "=" * 60)
    print("Migration complete!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Update main.py to include recommendations_v2 router")
    print("2. Test the new eligibility-based matching endpoint")
    print("3. Update frontend to use the new API response format")
    print("=" * 60)

if __name__ == "__main__":
    migrate_to_v2()
