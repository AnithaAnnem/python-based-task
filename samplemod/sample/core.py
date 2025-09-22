from flask import Flask
from . import helpers

app = Flask(__name__)

@app.route('/')
def home():
    if helpers.get_answer():
        return 'hmmm...'
    else:
        return 'No answer!'

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
