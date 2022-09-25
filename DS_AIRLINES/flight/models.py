from datetime import datetime

from databaseinit import db
import uuid

from flask import jsonify, redirect, request, flash


class Flight:

    def addflight(self):
        datestr = request.form.get('datetime')
        fldate = datetime.strptime(datestr, "%Y-%m-%d %H:%M")
        
        destination = request.form.get('destination').title()
        departure = request.form.get('departure').title()
        cost = request.form.get('cost')

        dep = departure[0]
        dest = destination[0]
        year = str(fldate.year)
        year = year[-2:]
        month = str(fldate.month)
        if len(month)==1:
            month = "0"+month
        day = str(fldate.day)
        hour = str(fldate.hour)
        flightnumber = dep + dest + year + month + day + hour
        availability = int(220)

        # Check if cost is more than 0
        if(int(cost) <= 0):
            return jsonify({ "error": "Cost must be more than 0" }), 400

        flight = {
            "_id": uuid.uuid4().hex,
            "flightnumber": flightnumber,
            "date": fldate,
            "departure": departure,
            "destination": destination,
            "cost": cost,
            "flhours": request.form.get('flhours'),
            "availability": availability
        }

        # Check if flight hours is more than 0
        if(int(flight["flhours"]) <= 0):
            return jsonify({ "error": "Flight hours must be more than 0" }), 400

        if db.flights.insert_one(flight):
            return flight
        
        return jsonify({ "error": "Flight creation failed" }), 400

    def editflightcost(self):
        flightnumber = request.form.get('flightnumber')
        cost = request.form.get('cost')

        if(int(cost) <= 0):
            return jsonify({ "error": "Cost must be more than 0" }), 400

        result = db.flights.find_one_and_update({ "flightnumber": flightnumber}, {"$set": {"cost": cost}})

        if result == None:
            return jsonify({ "error": "No flight found"}), 400
        flash("Price changed successfully")
        return result

    def deleteflight(self):
        flightnumber = request.form.get('flightnumber')

        result = db.flights.find_one_and_delete({ "flightnumber": flightnumber})

        if result == None:
            return jsonify({ "error": "No flight found"}), 400
        flash("Flight deleted successfully")
        return result
    
    def searchflight(self): 
        datestr = request.form.get('datetime')
        fldate = datetime.strptime(datestr, "%Y-%m-%d %H:%M")
        destination = request.form.get('destination').title()
        departure = request.form.get('departure').title()

        searchflight = {
            "date": fldate,
            "departure": departure,
            "destination": destination
        }

        results = db.flights.find({ "departure": searchflight['departure'],
                          "destination": searchflight['destination'],
                          "date": searchflight['date'],
                          "availability": { "$gt": 0 }})
        resultslist = list(results)
        if len(resultslist) == 0:
            flash('No Flights Found...')
        return resultslist