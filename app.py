from flask import Flask

app = Flask(__name__)


@app.route('/api/v1/hello-world-9')
def hello():
    return 'Hello World 9'
    
if __name__ == "__main__":
    app.run()