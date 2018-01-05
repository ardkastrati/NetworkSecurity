from flask import Flask, render_template, request, make_response, send_from_directory, session
import random
import os
import threading

""" The website has 2 users: ordinary user and an admin. We have credentials for the ordinary user,
    but we want to log in as an administrator."""
app = Flask(__name__)

loggedInUserCookies = {}

prng = random.Random(1337)

userData = {"user1":"password1"}

""" Create a task which logs in the admin every ADMIN_PERIOD seconds """
def adminLogin():
    global prng
    global loggedInUserCookies

    ADMIN_PERIOD = 300.0

    threading.Timer(ADMIN_PERIOD, adminLogin).start()
    
    token = None
    
    for key, value in loggedInUserCookies.items():
        if value == 'admin':
            token = key
            break

    if token != None:
        loggedInUserCookies[token] = None

    token = str(prng.getrandbits(32))

    loggedInUserCookies[token] = 'admin'

    # If you uncomment this line, brute force attack (which takes a couple of hours)
    # won't be possible
    #
    # prng.seed(os.urandom())


@app.route('/robots.txt')
def static_from_root():
    return send_from_directory(app.static_folder, request.path[1:])

@app.route('/')
def display():
    global loggedInUserCookies

    # print(loggedInUserCookies)

    try:
        # If there is no login cookie, show login page
        #
        if not "netsecLoginCookie" in request.cookies:
            return make_response(render_template('login.html'))
        # If we have an admin, send him to admin home
        #
        elif loggedInUserCookies[request.cookies['netsecLoginCookie']] == 'admin':
            return make_response(render_template('adminHome.html'))
        # If we have a logged in user, send him to user home
        #
        elif loggedInUserCookies[request.cookies['netsecLoginCookie']] != None:
            return make_response(render_template('home.html'))
        # If the login token isn't in a hashtable, send user back to login page
        #
        else:
            return make_response(render_template('login.html'))
    except KeyError:
        return make_response(render_template('login.html'))



@app.route('/login', methods=['GET','POST'])
def loginForm():
    global loggedInUserCookies
    global prng

    data = request.form
    value = str(prng.getrandbits(32))

    # This can be used to test admin pages. In the final version, admin prompt should be removed
    #
    if data['user'] == 'admin' and data['password'] == 'verylongandsecretpassword':
        response = make_response(render_template('adminHome.html'))     
        response.set_cookie('netsecLoginCookie',value)
        loggedInUserCookies[value] = 'admin'
        session['username'] = 'admin'
        return response

    # Log in user, and send him his cookie :)
    #
    elif userData[data['user']] == data['password']:
        response = make_response(render_template('home.html'))
        response.set_cookie('netsecLoginCookie', value)
        loggedInUserCookies[value] = data['user']
        session['username'] = data['user']
        return response

@app.route('/logout', methods=['GET','POST'])
def logOut():

    # Redirect user to login, and expire his login cookie
    #
    response = make_response(render_template('login.html'))
    response.set_cookie('netSecLoginCookie','', expires=0)
    
    # Find the token with the username, and delete it
    #
    token = None

    try:
        username = session['username']
        
    
        for key, value in loggedInUserCookies.items():
            if value == username:
                token = key
                break
    
    
    except Exception:
        return response

    if token == None:
        return response

    loggedInUserCookies[token] = None

    return response


if __name__=='__main__':

    # Schedule admin login code
    #
    adminLogin()

    # Generate application key so we can use flask sessions
    #
    app.secret_key = os.urandom(24)

    # Run the application
    #
    app.run(host='0.0.0.0', debug=True, port=5000)
