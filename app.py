from flask import Flask, render_template, session, redirect, url_for
from scanner.sushi import Scanner

FILE_PATH = "static/assets/registered.txt"

app = Flask(__name__, static_url_path='/static')
app.config["SECRET_KEY"] = "hello_readers"

DEFAULT_SUMMARY_DICT = {
    "count": {
        "red": 0,
        "silver": 0,
        "gold": 0,
        "black": 0,
        "others": 0
    },
    "total_price": 0
}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/scan")
def scan():
    print(f"Testing...\nOpening file from path: {FILE_PATH}")
    scanner = Scanner(fp=FILE_PATH, testing=True)
    scanned_price = ""
    while scanned_price != "q":
        scanned_price = input()
        scanner.add_item(scanned_price)
    session["summary_dict"] = scanner.summary_dict
    print(f"Data added to session: {session['summary_dict']}")
    return redirect(url_for("summary"))

@app.route("/summary")
def summary():
    print(session)
    summary_dict = session.get("summary_dict", {})
    red_price = summary_dict.get("count", {}).get("red", 0) * 40
    silver_price = summary_dict.get("count", {}).get("silver", 0) * 60
    gold_price = summary_dict.get("count", {}).get("gold", 0) * 80
    black_price = summary_dict.get("count", {}).get("black", 0) * 120
    total = summary_dict.get("total_price", 0)
    print(red_price, silver_price, gold_price, black_price, total)
    return render_template("summary.html", red=red_price, silver=silver_price, gold=gold_price, black=black_price, total=total)

@app.route("/payment")
def payment():
    return render_template("payment.html")

@app.route("/reset")
def reset():
    session["summary_dict"] = DEFAULT_SUMMARY_DICT
    return redirect(url_for("summary"))

@app.route("/loading")
def loading():
    return render_template("loading.html")

@app.route("/thankyou")
def thankyou():
    return render_template("thankyou.html")

@app.route("/instruction")
def instruction():
    return render_template("instruction.html")

@app.route("/main")
def main():
    return render_template("main.html")

if __name__ == "__main__":
    app.run(host="127.0.0.1", port="8000", debug=True)
