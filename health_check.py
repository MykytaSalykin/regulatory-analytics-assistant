#!/usr/bin/env python3
"""
Health check script for Regulatory Analytics Assistant
"""

import sys
import os


def check_docker():
    """Check if Docker is running"""
    import subprocess

    try:
        result = subprocess.run(
            ["docker", "ps"], capture_output=True, text=True, check=True
        )
        if "regulatory_analytics_db" in result.stdout:
            print("✅ PostgreSQL container is running")
            return True
        else:
            print("❌ PostgreSQL container not found")
            print("   Run: docker-compose up -d")
            return False
    except subprocess.CalledProcessError:
        print("❌ Docker is not running or not installed")
        return False
    except FileNotFoundError:
        print("❌ Docker command not found")
        return False


def check_database():
    """Check if database is accessible"""
    try:
        from sqlalchemy import create_engine, text
        from dotenv import load_dotenv

        load_dotenv()

        db_url = (
            f"postgresql+psycopg2://{os.getenv('DB_USER', 'postgres')}:"
            f"{os.getenv('DB_PASSWORD', 'postgres')}@"
            f"{os.getenv('DB_HOST', 'localhost')}:"
            f"{os.getenv('DB_PORT', '5432')}/"
            f"{os.getenv('DB_NAME', 'regulatory_analytics')}"
        )

        engine = create_engine(db_url)
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))

        print("✅ Database connection successful")
        return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False


def check_schema():
    """Check if required tables exist"""
    try:
        from sqlalchemy import create_engine, inspect
        from dotenv import load_dotenv

        load_dotenv()

        db_url = (
            f"postgresql+psycopg2://{os.getenv('DB_USER', 'postgres')}:"
            f"{os.getenv('DB_PASSWORD', 'postgres')}@"
            f"{os.getenv('DB_HOST', 'localhost')}:"
            f"{os.getenv('DB_PORT', '5432')}/"
            f"{os.getenv('DB_NAME', 'regulatory_analytics')}"
        )

        engine = create_engine(db_url)
        inspector = inspect(engine)

        required_tables = {
            "finance": ["survey_metrics"],
            "rag": ["document_chunks_raw", "document_embeddings"],
            "meta": ["data_sources"],
        }

        all_ok = True
        for schema, tables in required_tables.items():
            schema_tables = inspector.get_table_names(schema=schema)
            for table in tables:
                if table in schema_tables:
                    print(f"✅ Table {schema}.{table} exists")
                else:
                    print(f"❌ Table {schema}.{table} not found")
                    all_ok = False

        return all_ok
    except Exception as e:
        print(f"❌ Schema check failed: {e}")
        return False


def check_env():
    """Check if environment variables are set"""
    from dotenv import load_dotenv

    load_dotenv()

    required_vars = ["OPENAI_API_KEY"]
    all_ok = True

    for var in required_vars:
        value = os.getenv(var)
        if value and value != "your_openai_api_key_here":
            print(f"✅ {var} is set")
        else:
            print(f"❌ {var} not set or using placeholder")
            all_ok = False

    return all_ok


def check_dependencies():
    """Check if required Python packages are installed"""
    required_packages = [
        "fastapi",
        "uvicorn",
        "streamlit",
        "sqlalchemy",
        "openai",
        "pandas",
        "psycopg2",
    ]

    all_ok = True
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} installed")
        except ImportError:
            print(f"❌ {package} not installed")
            all_ok = False

    return all_ok


def main():
    print("🔍 Regulatory Analytics Assistant - Health Check\n")

    checks = [
        ("Docker", check_docker),
        ("Database Connection", check_database),
        ("Database Schema", check_schema),
        ("Environment Variables", check_env),
        ("Python Dependencies", check_dependencies),
    ]

    results = []
    for name, check_func in checks:
        print(f"\n📋 Checking {name}...")
        try:
            result = check_func()
            results.append(result)
        except Exception as e:
            print(f"❌ Error during {name} check: {e}")
            results.append(False)

    print("\n" + "=" * 50)
    if all(results):
        print("✅ All checks passed! System is ready.")
        sys.exit(0)
    else:
        print("❌ Some checks failed. Please review the output above.")
        sys.exit(1)


if __name__ == "__main__":
    main()
