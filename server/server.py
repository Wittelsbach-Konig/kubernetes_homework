from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():
    """Hello world function

    Returns:
        str : 'Hello World!'
    """
    return 'Hello World!'
