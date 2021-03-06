from flask import Flask, request, render_template, session, make_response

app = Flask(__name__)
app.secret_key = b'*EF63./w[9'

@app.route('/')
def main_point():
    # Не передается имя авторизированного пользователя на страницу index.html
    visit_counter = 0
    if session.get('visited'):
        visit_counter = session['visited']
    else:
        session['visited'] = 0
    response = make_response(render_template('index.html', visited=visit_counter))
    session['visited'] += 1
    return response

# @app.route('/login', methods=['GET', 'POST'])
# def login_page():
#     # Не послучается связать условия куки и юзера
#     username = ""
#     log = ""
#     if request.method == 'GET' and log == "":
#         # if request.cookies.get('logged'):
#         log = request.cookies.get('logged')
#         return render_template('login.html')
#     elif log == "yes":
#         return render_template('index.html')
#     elif request.method == 'POST':
#         username = request.form['username']
#         request.cookies.get('logged')
#         response = make_response(render_template('index.html', username=username))
#         # Не передает ли username в темплейт значение
#         response.set_cookie("logged", "yes")
#         return f"User logged in as: <b>{username}</b>"
#     return username

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'GET':
        # в случае гет запроса нам надо отрисовать форму для логина если сессия пустая или вывести теймплейт что пользователь залогинен
        if session.get('username'):
            return render_template('index.html', username=session.get('username'))
        else:
            return render_template('login.html')
    elif request.method == 'POST':
        # берем с пост запроса юзернейм
        username = request.form['username']
        # здесь сохраняем юзернейм в сессию тут мы будем знать что юзер залогинен
        session['username'] = username
        return make_response(render_template('index.html', username=session['username']))

# @app.route('/cookies')
# def cokie_page():
#     log = ""
#     if request.cookies.get('logged'):
#         log = request.cookies.get('logged')
#     response = make_response(f"Form auth: {log}")
#     response.set_cookie("logged", "yes")
#     return response

@app.route('/logout')
def logout():
    response = make_response("<p> User was logout </p>")
    response.set_cookie("logged", "", 0)
    return response

if __name__ == '__main__':
    app.run(debug=True, port=5001)
