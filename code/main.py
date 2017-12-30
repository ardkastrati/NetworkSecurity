from flask import Flask, render_template, request, make_response, send_from_directory
app = Flask(__name__)

currentValidCookie = "123"

'''
    This methodes checkes the cookie 
'''
def checkCookie(cookie):
    if cookie == currentValidCookie:
        return True
    else:
        return False

@app.route('/robots.txt')
def static_from_root():
    return send_from_directory(app.static_folder, request.path[1:])

@app.route('/')
def display():
    response = make_response(render_template('login.html'))
    response.set_cookie('terrorLoginCookie',value='notAuth')
    return response

@app.route('/home')
def displayHome():
    if 'terrorLoginCookie' in request.cookies and checkCookie(request.cookies['terrorLoginCookie']):
        return render_template('home.html')
    else:
        return display()

@app.route('/news')
def displayNews():
    if 'terrorLoginCookie' in request.cookies and checkCookie(request.cookies['terrorLoginCookie']):
        return render_template('news.html')
    else:
        return display()

@app.route('/chat')
def displayChat():
    if 'terrorLoginCookie' in request.cookies and checkCookie(request.cookies['terrorLoginCookie']):
        return render_template('chat.html')
    else:
        return display()

if __name__=='__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)