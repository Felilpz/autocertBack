from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route('/teste')
def home():
    return "testando api"


if __name__ == '__main__':
    app.run(debug=True)
