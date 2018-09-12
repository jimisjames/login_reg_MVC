from flask import Flask, render_template, request, redirect, session, flash

from login_reg_MVC.config.mysqlconnection import connectToMySQL

from login_reg_MVC import bcrypt

class Log():
    def checkEmail(self):
        myData = connectToMySQL('myDB')
        for user in myData.query_db("SELECT users.email FROM users;"):
            if session["email"] == user["email"]:
                return True
        return False

    def addToDb(self):
        myData = connectToMySQL('myDB')
        query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, now(), now());"
        data = { 
            "first_name" : request.form["first_name"],
            "last_name" : request.form["last_name"],
            "email" : request.form["email"],
            "password" : bcrypt.generate_password_hash(request.form["password"])
            }
        newClientId = myData.query_db(query, data)
        session["logged_in"] = newClientId
        return

    def logIn(self):
        myData = connectToMySQL('myDB')
        query = "SELECT * FROM users WHERE email = %(email)s;"
        data = { "email" : request.form["email"] }
        return myData.query_db(query, data)