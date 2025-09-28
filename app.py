from routes import app
from db_schema import get_db_connection, init_db

init_db()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6000, debug=True)

