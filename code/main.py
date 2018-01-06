from flask import Flask, render_template, request, make_response, send_from_directory, session
import json
import random
import os
import threading

""" The website has 2 users: ordinary user and an admin. We have credentials for the ordinary user,
    but we want to log in as an administrator."""
app = Flask(__name__)

loggedInUserCookies = {}

prng = random.Random(1337)

userData = {"user1": "password1"}


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

    if token is not None:
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

    with open('db.json', 'r') as file:
        db = json.load(file)

    try:
        # send the user to its home
        #
        user = loggedInUserCookies[request.cookies.get('netsecLoginCookie')]
        return make_response(render_template('home.html', profile=db['profiles'][user]))
        # If there is no login cookie or it is not in the hashtable, send user back to login page
        #
    except KeyError:
        return make_response(render_template('login.html'))


@app.route('/login', methods=['GET', 'POST'])
def login_form():
    global loggedInUserCookies
    global prng

    data = request.form
    value = str(prng.getrandbits(32))

    with open('db.json', 'r') as file:
        db = json.load(file)

    # This can be used to test admin pages. In the final version, admin prompt should be removed
    #
    if data['user'] == 'admin' and data['password'] == 'verylongandsecretpassword':
        response = make_response(render_template('home.html', profile=db['profiles']['admin']))
        response.set_cookie('netsecLoginCookie', value)
        loggedInUserCookies[value] = 'admin'
        session['username'] = 'admin'
        return response

    # Log in user, and send him his cookie :)
    #
    elif userData[data['user']] == data['password']:
        response = make_response(render_template('home.html', profile=db['profiles'][data['user']]))
        response.set_cookie('netsecLoginCookie', value)
        loggedInUserCookies[value] = data['user']
        session['username'] = data['user']
        return response
    # If the login is fails the login page is sent again
    #
    else:
        return make_response(render_template('login.html'))


@app.route('/logout', methods=['GET', 'POST'])
def logout():

    # Redirect user to login, and expire his login cookie
    #
    response = make_response(render_template('login.html'))
    response.set_cookie('netSecLoginCookie', '', expires=0)
    
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

    if token is None:
        return response

    loggedInUserCookies[token] = None

    return response


@app.route('/news', methods=['GET', 'POST'])
def news():
    with open('db.json', 'r') as file:
        db = json.load(file)
    try:
        user = loggedInUserCookies[request.cookies.get('netsecLoginCookie')]
        return make_response(render_template('news.html', news=db['profiles'][user]['news']))
    except KeyError:
        return make_response(render_template('login.html'))


@app.route('/chat', methods=['GET', 'POST'])
def chat():
    with open('db.json', 'r') as file:
        db = json.load(file)
    try:
        user = loggedInUserCookies[request.cookies.get('netsecLoginCookie')]
        return make_response(render_template('chat.html', chat=db['profiles'][user]['chat'],
                                             profile_pic=db['profiles'][user]['image']))
    except KeyError:
        return make_response(render_template('login.html'))


""" Create a json dump with the user profile's data """
def populate_db():
    data = {'profiles': {'admin': {'name': 'Johnny Appleseed',
                                   'city': 'San Francisco, CA',
                                   'reputation': 185,
                                   'kills_title': 'Kills',
                                   'kills': 344,
                                   'days out': 127,
                                   'about me': 'Eniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
                                   'image': 'static/terrorist2.jpg',
                                   'friends': 'Your friends - 106 total',
                                   'friend names': ['Osama', 'Imad', 'Hasan', 'Ali', 'Abdul', 'Mohamed'],
                                   'chat': {'messages': [["Hello. How are you today?", "Hey! I'm fine. Thanks for asking!"],
                                                         ["Sweet! So, are you ready for your mission?", "Yes bro I am so ready! 72 Virgins cant wait."],
                                                         ["All right, you know what to do?", "Yes, I just need the coordinates!"],
                                                         ],
                                            'image message': ['static/image.jpg', 'All right! See you on ther other side'],
                                            'image recipient': 'static/terrorist1.jpg'
                                            },
                                   'news': {'cover': 'static/cover.jpg', 'one third': 'static/rifle.jpg',
                                            'two thirds': 'static/grenade.jpg', 'three thirds': 'static/knife.jpg',
                                            'final': 'static/explosion.jpg'}
                                   },
                         'user1': {'name': 'Philip Dickens',
                                   'city': 'Boston, MA',
                                   'reputation': 0,
                                   'kills_title': 'Followers',
                                   'kills': 12,
                                   'days out': 0,
                                   'about me': 'Eniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
                                   'image': 'static/user_profile_pic.jpg',
                                   'friends': 'Your friends - 59 total',
                                   'friend names': ['Jerry K.', 'Katie F.', 'Ash K.', 'Sponge B.', 'Frank', 'Alexa S.'],
                                   'chat': {'messages': [["Hello Mom. How are you today?", "Hello darling! I'm fine. How are you?"],
                                                         ["I am good too. Can you buy some ice cream? ", "Of course son!"],
                                                         ["Thank you mom! You are the best!", "I know. Don't forget to tidy your room before your dad gets home"],
                                                         ["No worries, I already tidied it", "Great! A big kiss!"],
                                                         ["Love you! Bye", "Bye bye my baby <3"],
                                                         ],
                                            'image recipient': 'static/mom.jpg'
                                            },
                                   'news': {'cover': 'static/friendly_cover.jpg', 'one third': 'static/ship.jpg',
                                            'two thirds': 'static/pengu.jpg', 'three thirds': 'static/trump.jpg',
                                            'final': 'static/countries.jpg'}
                                   }
                         }
            }

    with open('db.json', 'w') as file:
        json.dump(data, file)


if __name__ == '__main__':

    # Schedule admin login code
    #
    populate_db()
    adminLogin()

    # Generate application key so we can use flask sessions
    #
    app.secret_key = os.urandom(24)

    # Run the application
    #
    app.run(host='0.0.0.0', debug=True, port=5000)
