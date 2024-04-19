from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5
from scanner.sushi import Scanner

app = Flask(__name__, static_url_path='/static')
Bootstrap5(app)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/test")
def test():
    scanner = Scanner()
    print("Welcome to Sushirov")
    print("Please return the dishes on the tray")
    scanner.initialize()

    scanned_price = input()
    scanner.add_item(scanned_price)
    return scanned_price

@app.route("/summary")
def summary():
    return render_template("summary.html")

if __name__ == "__main__":
    app.run(host="127.0.0.1", port="8000", debug=True)
