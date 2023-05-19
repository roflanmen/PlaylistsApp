from app import socketio, app
import os
if __name__ == "__main__":
    socketio.run(app, debug=True, port=os.environ.get('PORT', 8000))
