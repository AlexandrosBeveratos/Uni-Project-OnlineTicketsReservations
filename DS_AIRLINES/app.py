from functools import wraps
from flask import Flask, jsonify, redirect, session, url_for, request, render_template, flash
from user.models import User
from flight.models import Flight
from reservation.models import Reservation

app = Flask(__name__)
app.secret_key = '3ijengposkl3mdkg4rlex'

# Decorators
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You must be logged in', "info")
            return redirect('/user/login/')

    return wrap


def roles_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if not 'logged_in' in session:
            return redirect('/user/login/')

        if not session['user']['role'] == "admin":
            flash('Access to the page denied', "info")
            return redirect('/')
        else:
            return f(*args, **kwargs)

    return wrap

# Routes


@app.route('/')
def index():
    session['admin'] = False
    if 'logged_in' in session:
        if session['user']['role'] == 'admin':
            session['admin'] = True

    return render_template('home.html')


@app.route("/user/signup/")
def signup():
    return render_template('signup.html')


@app.route("/user/login/")
def login():
    return render_template('login.html')


@app.route('/user/register/', methods=['POST'])
def createuser():
    return User().registeruser()


@app.route('/user/signout/')
def signout():
    return User().signout()


@app.route('/user/signin/', methods=['POST'])
def log():
    return User().signin()


@app.route('/user/accountdisabled/', methods=['GET', 'POST'])
def accountdis():
    return render_template('enableaccount.html')


@app.route('/user/enableaccount/', methods=['POST'])
def enableacc():
    return User().enableaccount()


@app.route('/user/deactivate/')
@login_required
def deactivateaccount():
    return User().deactivateaccount()


@app.route('/user/deactivated/')
def deactivated():
    return render_template('accdeactivated.html')


@app.route('/user/reservations/')
@login_required
def reservations():
    reservation = None
    return render_template('reservations.html', reservation=reservation)


@app.route('/user/reservations/search/', methods=['POST'])
@login_required
def searchreservations():
    reservation = Reservation().searchreservation()
    return render_template('reservations.html', reservation=reservation)


@app.route('/user/reservations/cancel/', methods=['POST'])
@login_required
def cancelreservation():
    return Reservation().cancelreservation()


@app.route('/dash/')
@login_required
def dash():
    reservations = Reservation().showreservations()
    return render_template('dash.html', reservations=reservations)


@app.route('/searchflight/', methods=['POST'])
@login_required
def searchfl():
    results = Flight().searchflight()
    return render_template('flights.html', flights=results)


@app.route('/flights/')
@login_required
def flights():
    return render_template('flights.html')


@app.route('/flights/reserve/', methods=['POST'])
def reserveflight():
    return Reservation().createreservation()


@app.route('/about/')
def about():
    return render_template('about.html')

# Admin routes


@app.route('/admin/')
@roles_required
def admin():
    return render_template('admin.html')


@app.route('/admin/addflight/')
@roles_required
def addflight():
    return render_template('addflight.html')


@app.route('/admin/editflight/')
@roles_required
def editflight():
    return render_template('editflight.html')


@app.route('/admin/createflight/', methods=['POST'])
@roles_required
def createflight():
    return Flight().addflight()


@app.route('/admin/editcost/', methods=['POST'])
@roles_required
def editcost():
    return Flight().editflightcost()


@app.route('/admin/deleteflight/', methods=['POST'])
@roles_required
def deleteflight():
    return Flight().deleteflight()


@app.route('/admin/usermanagement/')
@roles_required
def usermanagement():
    return render_template('usermanagement.html')


@app.route('/admin/makeadmin/', methods=['POST'])
@roles_required
def makeadmin():
    return User().add_admin()


@app.route('/admin/removeadmin/', methods=['POST'])
@roles_required
def removeadmin():
    return User().remove_admin()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
