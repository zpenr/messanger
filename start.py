#!/usr/bin/env python3
"""
Startup script with detailed logging for Railway deployment debugging
"""
import os
import sys
from app import create_app

def main():
    print("=" * 50)
    print("ZPENR MESSENGER STARTUP")
    print("=" * 50)
    
    # Print environment info
    print(f"Python version: {sys.version}")
    print(f"Current working directory: {os.getcwd()}")
    print(f"PORT environment variable: {os.environ.get('PORT', 'NOT SET')}")
    print(f"DATABASE_URL environment variable: {'SET' if os.environ.get('DATABASE_URL') else 'NOT SET'}")
    
    # List all environment variables that start with POSTGRES
    postgres_vars = {k: v for k, v in os.environ.items() if k.startswith('POSTGRES')}
    print(f"PostgreSQL environment variables: {postgres_vars}")
    
    try:
        print("\nCreating Flask app...")
        app = create_app()
        print("Flask app created successfully!")
        
        # Test the health endpoint
        print("\nTesting health endpoint...")
        with app.test_client() as client:
            response = client.get('/health')
            print(f"Health check response: {response.status_code}")
            print(f"Health check data: {response.get_json()}")
        
        print("\nApp is ready to serve requests!")
        return app
        
    except Exception as e:
        print(f"\nERROR during app creation: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    app = main()
    
    # Run the app
    port = int(os.environ.get('PORT', 8080))
    print(f"\nStarting server on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)
