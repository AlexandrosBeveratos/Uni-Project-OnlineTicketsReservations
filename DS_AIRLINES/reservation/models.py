from email import message
import random
from databaseinit import db
from flask import session
import uuid

from flask import jsonify, redirect, request, flash


class Reservation:
    def createreservation(self):

        flightnumber = request.form.get("flightnumber")
        name = request.form.get("name")
        idnum = request.form.get("idnum")
        credit = request.form.get("credit")
        query_val = {"flightnumber": flightnumber, "availability": {"$gt": 0}}
        new_value = {"$inc": {"availability": -1}}

        d = 0
        if len(credit) == 16:
            for i in credit:
                if (i.isdigit()):
                    d += 1
        if(d <= 15):
            return jsonify({"error": "Credit Card Number Is Invalid"}), 400

        flight = db.flights.find_one_and_update(query_val, new_value)
        cost = flight["cost"]
        if(flight == None):
            return jsonify({"error": "Flight Number Is Invalid"}), 400

        while(True):
            resnumber = str(random.randint(100000000000, 999999999999))
            if(resnumber != db.reservations.find_one({"resnumber": resnumber})):
                break

        reservation = {
            "_id": uuid.uuid4().hex,
            "resnumber": resnumber,
            "flightnumber": flightnumber,
            "name": name,
            "idnum": idnum,
            "credit": credit,
            "cost": cost
        }
        if db.reservations.insert_one(reservation):
            flash('Reservation successful')
            return reservation

    def showreservations(self):
        passport = session['user']['idnum']
        reservations = db.reservations.find({"idnum": passport})
        reservlist = list(reservations)
        return reservlist

    def searchreservation(self):
        resnumber = request.form.get("resnumber")

        reservation = db.reservations.find_one({"resnumber": resnumber})

        if(reservation == None):
            return flash("Reservation Number Invalid")

        flightnumber = reservation["flightnumber"]
        flight = db.flights.find_one({"flightnumber": flightnumber})
        destination = flight["destination"]
        reservation["destination"] = destination

        return reservation

    def cancelreservation(self):
        resnumber = request.form.get("resnumber")

        reservation = db.reservations.find_one({"resnumber": resnumber})
        if(reservation == None):
            return jsonify({"error": "Reservation Number Is Invalid"}), 400

        query_val = {"flightnumber": reservation['flightnumber']}
        new_val = {"$inc": {"availability": 1}}
        if(db.reservations.find_one_and_delete({"resnumber": resnumber})):
            db.flights.find_one_and_update(query_val, new_val)
            message = f"Reservation Refunded to: {reservation['credit']}"
            flash(message)
            return reservation
