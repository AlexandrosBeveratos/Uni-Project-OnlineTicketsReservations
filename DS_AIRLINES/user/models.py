import email
from hashlib import new
import random
import uuid
from flask import jsonify, redirect, request, session, flash
import pymongo
from werkzeug.security import generate_password_hash, check_password_hash
from databaseinit import db


# USER
class User:

    def start_session(self, user):
        del user['password']
        session['logged_in'] = True
        session['user'] = user
        return jsonify(user), 200

    def registeruser(self):
        enablingnum = str(random.randint(100000000000, 999999999999))
        user = {
            "_id": uuid.uuid4().hex,
            "email": request.form.get('email'),
            "username": request.form.get('username'),
            "fullname": request.form.get('fullname'),
            "password": request.form.get('password'),
            "idnum": request.form.get('idnum'),
            "role": 'simple_user',
            "status": 'enabled',
            "enablingnum": enablingnum
        }
        d = 0
        if (len(user['password']) >= 8):
            for i in user['password']:
                if (i.isdigit()):
                    d += 1
        if(d >= 1):
            # Encrypt the password
            user['password'] = generate_password_hash(user['password'])
        else:
            return jsonify({"error": "Password must be 8 characters long with at least 1 digit"}), 400

        # Check for existing email address
        if db.users.find_one({"email": user['email']}):
            return jsonify({"error": "Email address already in use"}), 400

        # Check for existing username
        if db.users.find_one({"username": user['username']}):
            return jsonify({"error": "Username already in use"}), 400
        
        # Check if passport number is valid
        passpcheck = user["idnum"][0] + user["idnum"][1]
        if(passpcheck.isnumeric()):
            return jsonify({"error": "Passport number is invalid"}), 400
        elif( not len(user["idnum"]) == 9 ):
            return jsonify({"error": "Passport number is invalid"}), 400

        # Check for existing Passport number
        if db.users.find_one({"idnum": user['idnum']}):
            return jsonify({"error": "Passport number already in use"}), 400

        if db.users.insert_one(user):
            return self.start_session(user)

        return jsonify({"error": "Signup failed"}), 400

    def signout(self):
        session.clear()
        flash("You have been logged out!", "info")
        return redirect('/')

    def signin(self):

        user = db.users.find_one({
            "email": request.form.get('email')
        })

        if user and check_password_hash(user['password'], request.form.get('password')):
            if not user['status'] == 'enabled':
                return jsonify({"error": "Account Disabled"}), 401
            if user['role'] == 'admin':
                session['admin'] = True
            return self.start_session(user)

        return jsonify({"error": "Invalid login credentials"}), 401

    def make_admin(self):
        session['user']['role'] = 'admin'

    def enableaccount(self):
        enabling_code = request.form.get('enabling_code')
        idnum = request.form.get('idnum')
        query_val = {"idnum": idnum, "enablingnum": enabling_code}
        new_value = {"$set": {"status": "enabled"}}
        user = db.users.find_one_and_update(query_val, new_value)

        if user == None:
            flash("Invalid Account Enabling code or Passport Number")
            return redirect('/user/accountdisabled/')

        flash("Account Enabled Succesfully")
        return redirect('/user/login/')

    def deactivateaccount(self):
        usermail = session['user']['email']
        query_val = {"email": usermail}
        new_value = {"$set": {"status": "disabled"}}
        user = db.users.find_one_and_update(query_val, new_value)
        return redirect("/user/deactivated/")

    def add_admin(self):
        email = request.form.get('email')
        query_val = {"email": email}
        new_value = {"$set": {"role": "admin"}}
        user = db.users.find_one(query_val)
        if user == None:
            return jsonify({"error": "Could not find any users with entered email"}), 401
        db.users.find_one_and_update(query_val, new_value)
        flash("Admin Added Succesfully")
        return user

    def remove_admin(self):
        email = request.form.get('email')
        query_val = {"email": email}
        new_value = {"$set": {"role": "simple_user"}}
        user = db.users.find_one(query_val)
        if user == None:
            return jsonify({"error": "Could not find any users with entered email"}), 401

        if user['email'] == session['user']['email']:
            return jsonify({"error": "You can't remove your admin role by yourself"}), 401

        db.users.find_one_and_update(query_val, new_value)

        flash("Admin Removed Succesfully")
        return user
