from flask import Flask, render_template, request, redirect, session, flash

import re

from login_reg_MVC import bcrypt

from login_reg_MVC.models.log import Log

log = Log()

class Logs():

    def home(self):
        return render_template("login_reg.html")


    def success(self):
        if "logged_in" in session:
            return render_template("login_reg_success.html")
        else:
            flash("Please log in to view that page!", "login")
            print(session["_flashes"])
            return redirect("/")


    def reg(self):
        session["first_name"] = request.form["first_name"]
        session["last_name"] = request.form["last_name"]
        session["email"] = request.form["email"]

        if len(session["first_name"]) <= 1:
            flash("Plese enter a valid first name", "first")
        elif not session["first_name"].isalpha():
            flash("Names may only contain letters", "first")

        if len(session["last_name"]) <= 1:
            flash("Plese enter a valid last name", "last")
        elif not session["last_name"].isalpha():
            flash("Names may only contain letters", "last")

        emailRegEx = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

        if len(session["email"]) <= 1:
            flash("Please enter a valid Email Address", "email")
        elif not emailRegEx.match(session["email"]):
            flash("You must enter a valid Email Address", "email")
        
        if log.checkEmail():
            flash("That email address is already registered!", "email")

        if len(request.form["password"]) == 0:
            flash("Please enter a password", "password")
        elif len(request.form["password"]) <= 7:
            flash("Password must be at least 8 characters", "password")

        if len(request.form["confirm_password"]) == 0:
            flash("Please confirm your password", "confirm")
        elif request.form["confirm_password"] != request.form["password"]:
            flash("Your passwords must match", "password")
            flash("Your passwords must match", "confirm")

        if "_flashes" in session.keys():
            return redirect("/") #failure
        else:
            flash("You are now registered!")
            log.addToDb()
            return redirect("/success")


    def logIn(self):
        users = log.logIn()

        if not users:
            flash("Incorrect email or password", "login")
            return redirect("/")

        if bcrypt.check_password_hash(users[0]["password"], request.form["password"]):
            session["logged_in"] = users[0]["id"]
            session["first_name"] = users[0]["first_name"]
            session["last_name"] = users[0]["last_name"]
            session["email"] = users[0]["email"]
            return redirect("/success")
        else:
            flash("Incorrect email or password", "login")
            return redirect("/")

    def logOut(self):
        session.clear()
        return redirect("/")
