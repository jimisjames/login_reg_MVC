
from login_reg_MVC import app
from login_reg_MVC.controllers.logs import Logs

logs = Logs()


@app.route("/")
def home():
    return logs.home()


@app.route("/success")
def success():
    return logs.success()


@app.route("/reg", methods=["POST"])
def reg():
    return logs.reg()


@app.route("/login", methods=["POST"])
def logIn():
    return logs.logIn()


@app.route("/logout", methods=["POST", "GET"])
def logOut():
    return logs.logOut()