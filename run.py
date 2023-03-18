from app import app
import os

if __name__ == "__main__":
    app.run(host="localhost", port = os.environ.get('PORT', 5000), debug=True)
