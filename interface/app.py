from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5

app = Flask(__name__)
Bootstrap5(app)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/test")
def test():
    return "Let's eat sushi!"

if __name__ == "__main__":
    app.run(host="127.0.0.1", port="8000", debug=True)
