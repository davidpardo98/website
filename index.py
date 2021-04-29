from flask import Flask
from flask import render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors

app = Flask(__name__)
app.secret_key= '12345'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'S3gc0v1d2021'
app.config['MYSQL_DB'] = 'basesegmtd'
mysql = MySQL(app)


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/pagina')
def about():
    return render_template('pagina.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login', methods =['GET', 'POST'])
def valida():
	if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
		email = request.form['email']
		password = request.form['password']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM usuarios WHERE email = % s AND password = % s', (email, password, ))
		account = cursor.fetchone()
		if account:
			session['loggedin'] = True
			session['nombre'] = account['nombre']
			cur = mysql.connection.cursor()
			cur.execute('SELECT tipdocpac, numdocpac, nombrespaciente FROM basemtdcall limit 1000')
			datos = cur.fetchall()
			return render_template('sesion.html', datos=datos)
		else:
			msg = 'Incorrect username / password !'
	return render_template('home.html')

@app.route('/registro')
def registro():
    return render_template('registro.html')

@app.route('/add', methods=['POST'])
def add():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        nombre = request.form['nombre']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO usuarios (email, password, nombre) VALUES (%s, %s, %s)',
        (email, password, nombre))
        mysql.connection.commit()
        return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
