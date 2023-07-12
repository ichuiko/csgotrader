from flask import Flask
from data.db import parseData

app = Flask(__name__)

@app.route('/')
def index():
    res = parseData()
    return res

if __name__ == "__main__":
    app.run(debug=True)