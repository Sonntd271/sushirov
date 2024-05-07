from threading import Thread
from flask import Flask, render_template, session, redirect, url_for
from scanner.sushi import Scanner
from scanner.motor import Motor

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

def motor_task(arg):
    global motor, stop_threads
    # while True:
    for _ in range(arg):
        if stop_threads:
            motor.ena.off()
            motor.pul.off()
            break
        motor.move_cont()
    motor.ena.off()
    motor.pul.off()

@app.route("/")
def home():
    summary_dict = session.get("summary_dict", {})
    total = summary_dict.get("total_price", 0)
    plate_count = sum(dict(summary_dict.get("count", {})).values())
    print(total, plate_count)
    return render_template("home.html", total=total, count=plate_count)

@app.route("/scan")
def scan():
    global scanner, stop_threads
    stop_threads = False

    # Run linear stage as a thread
    thread = Thread(target=motor_task, args=(10, ))
    thread.start()

    # Run scanner
    rfid = ""
    while rfid != "q":
        rfid = input()
        ok = scanner.add_item(rfid)
        if not ok:
            break
    
    # Exit thread when white card is detected
    stop_threads = True
    thread.join()

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
    global scanner

    session["summary_dict"] = DEFAULT_SUMMARY_DICT
    scanner.summary_dict = DEFAULT_SUMMARY_DICT
    return redirect(url_for("home"))

@app.route("/thankyou")
def thankyou():
    return render_template("thankyou.html")

# @app.route("/loading")
# def loading():
#     return render_template("loading.html")

# @app.route("/instruction")
# def instruction():
#     return render_template("instruction.html")

if __name__ == "__main__":
    motor = Motor()
    scanner = Scanner(fp=FILE_PATH)
    app.run(host="127.0.0.1", port="8000", debug=True)
