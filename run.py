#!/usr/bin/env python
"""
BirdQuest - Run Script
Easy startup script for the BirdQuest application.
"""

import os
import sys


def check_and_init_database():
    """Check if database exists and initialize tables if needed."""
    from app import CompletedHabit, CustomHabit, HiddenHabit, OwnedBird, User, app, db

    with app.app_context():
        # Get the instance folder path (where Flask-SQLAlchemy stores the db)
        instance_path = app.instance_path
        db_filename = app.config["SQLALCHEMY_DATABASE_URI"].replace("sqlite:///", "")
        db_path = os.path.join(instance_path, db_filename)

        # Ensure instance folder exists
        if not os.path.exists(instance_path):
            os.makedirs(instance_path)
            print(f"📁 Created instance folder: {instance_path}")

        # Check if database file exists
        db_exists = os.path.exists(db_path)

        if not db_exists:
            print(f"📁 Database not found at {db_path}. Creating new database...")

        # Create all tables
        db.create_all()

        # Verify all tables exist by trying to query them
        tables_ok = True
        try:
            # Try to query each table to verify it exists
            User.query.limit(1).all()
            OwnedBird.query.limit(1).all()
            CompletedHabit.query.limit(1).all()
            CustomHabit.query.limit(1).all()
            HiddenHabit.query.limit(1).all()
        except Exception as e:
            print(f"⚠️ Table verification failed: {e}")
            tables_ok = False

        if not tables_ok:
            print("🔄 Recreating database tables...")
            db.drop_all()
            db.create_all()
            print("✅ Database tables recreated!")
        elif not db_exists:
            print("✅ Database and tables created successfully!")
        else:
            print("✅ Database verified!")

        return True


def main():
    """Initialize and run the BirdQuest application."""
    # Ensure we're in the correct directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)

    # Add the script directory to the Python path
    if script_dir not in sys.path:
        sys.path.insert(0, script_dir)

    # Import the app
    from app import app

    # Initialize and verify the database
    print("🐦 Initializing BirdQuest...")
    check_and_init_database()

    # Configuration
    host = os.environ.get("FLASK_HOST", "127.0.0.1")
    port = int(os.environ.get("FLASK_PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG", "1") == "1"

    # Run the application
    print(f"\n🚀 Starting BirdQuest on http://{host}:{port}")
    print("📝 Press CTRL+C to stop the server\n")

    try:
        app.run(host=host, port=port, debug=debug)
    except KeyboardInterrupt:
        print("\n\n👋 BirdQuest stopped. See you next time!")
        sys.exit(0)


if __name__ == "__main__":
    main()
