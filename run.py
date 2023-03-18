from waitress import serve
from app import app
import os
serve(app, host='localhost', port=os.environ.get('PORT', 5000))