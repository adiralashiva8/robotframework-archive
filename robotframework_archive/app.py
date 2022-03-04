from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
import config
from .args import parse_options

app = Flask (__name__,
            static_url_path='', 
            static_folder='templates',
            template_folder='templates')

mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/historic')
def historic_home():
    return render_template('historic/home.html')

@app.route('/sp_historic')
def sp_historic_home():
    return render_template('sp_historic/home.html')

@app.route('/sf_historic')
def sf_historic_home():
    return render_template('sf_historic/home.html')

@app.route('/redirect')
def redirect_url():
    return render_template('redirect.html')

@app.route('/hsnew', methods=['GET', 'POST'])
def hs_add_new():
    if request.method == "POST":
        db_name = request.form['dbname']
        cursor = mysql.connection.cursor()

        try:
            # update created database info in robothistoric.project table
            cursor.execute("INSERT INTO rfarchive.project ( pid, name, image, created, updated, total, percentage) VALUES (0, '%s', '%s', NOW(), NOW(), 0, 0);" % (db_name, db_image))
            mysql.connection.commit()
        except Exception as e:
            print(str(e))

        finally:
            return redirect(url_for('home'))
    else:
        return render_template('hsnew.html')

def main():
    args = parse_options()
    app.config['MYSQL_HOST'] = args.sqlhost
    app.config['MYSQL_USER'] = args.username
    app.config['MYSQL_PASSWORD'] = args.password
    app.config['auth_plugin'] = 'mysql_native_password'
    app.run(host=args.apphost, port=args.appport)