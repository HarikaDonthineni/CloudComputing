import sqlite3

from flask import Flask, request, g, render_template, send_file

DATABASE = '/var/www/html/flaskapp/mydata.db'

app = Flask(__name__)
app.config.from_object(__name__)

def connect_to_database():
    return sqlite3.connect(app.config['DATABASE'])

def get_db():
    db = getattr(g, 'db', None)
    if db is None:
        db = g.db = connect_to_database()
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

def execute_query(query, args=()):
    cur = get_db().execute(query, args)
    rows = cur.fetchall()
    cur.close()
    return rows

def commit():
    get_db().commit()

@app.route("/")
def hello():
        execute_query("DROP TABLE IF EXISTS users")
        execute_query("CREATE TABLE users (Username text,Password text,firstname text, lastname text, email text, count integer)")
        return render_template('login.html')

@app.route('/registration', methods =['GET', 'POST'])
def registration():
    msg = ''
    if request.method == 'POST' and str(request.form['username']) !="" and str(request.form['password']) !="" and str(request.form['firstname']) !="" and str(request.form['lastname']) !="" and str(request.form['email']) !="":
        username = str(request.form['username'])
        password = str(request.form['password'])
        firstname = str(request.form['firstname'])
        lastname = str(request.form['lastname'])
        email = str(request.form['email'])
        
        res = execute_query("""SELECT *  FROM users WHERE Username  = (?)""", (username, ))
        if res:
            msg = 'User has already registered!'
        else:
            sq1 = execute_query("""INSERT INTO users (username, password, firstname, lastname, email) values (?, ?, ?, ?, ? )""", (username, password, firstname, lastname, email, ))
            commit()
            sq2 = execute_query("""SELECT firstname,lastname,email,count  FROM users WHERE Username  = (?) AND Password = (?)""", (username, password ))
            if sq2:
                for row in sq2:
                    return renderPage(row[0], row[1], row[2])
    elif request.method == 'POST':
        msg = 'Some of the fields are missing!'
    return render_template('registration.html', message = msg)

@app.route('/login', methods =['POST', 'GET'])
def login():
    msg = ''
    if request.method == 'POST' and str(request.form['username']) !="" and str(request.form['password']) != "":
        username = str(request.form['username'])
        password = str(request.form['password'])
        sq = execute_query("""SELECT firstname,lastname,email  FROM users WHERE Username  = (?) AND Password = (?)""", (username, password ))
        if sq:
            for row in sq:
                return renderPage(row[0], row[1], row[2])
        else:
            msg = 'Invalid Credentials !'
    elif request.method == 'POST':
        msg = 'Please enter Credentials'
    return render_template('login.html', message = msg)

def renderPage(firstname, lastname, email):
    return """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8" />
            <title>User Details</title>
            <style>
                body {{
                    color: #333;
                    background-color: #f9f9f9;
                    font-family: Arial, Verdana, sans-serif;
                    font-size: 14px;
                    margin: 0;
                    padding: 0;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                }}

                div {{
                    font-size: 16px;
                    padding: 20px;
                    border: 2px solid #333;
                    width: 400px;
                    text-align: center;
                    border-radius: 8px;
                    background-color: rgba(255, 255, 255, 0.9);
                    margin-top: 50px;
                }}

                h1 {{
                    background-color: #00796b;
                    color: white;
                    padding: 10px;
                    margin-bottom: 10px;
                    border-radius: 6px;
                }}
            </style>
        </head>
        <body>
            <div>
                <h1>User Details</h1>
                Name: {}<br>
                Surname: {}<br>
                Email: {}
            </div>
        </body>
        </html>
    """.format(str(firstname), str(lastname), str(email))

if __name__ == '__main__':
  app.run()