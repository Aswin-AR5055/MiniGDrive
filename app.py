from routes import app
from db_schema import init_db

# Initialize database
init_db()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

