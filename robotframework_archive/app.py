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
    return render_template('home.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/hshome')
def historic_home():
    return render_template('hshome.html')

@app.route('/sphome')
def sp_historic_home():
    return render_template('sphome.html')

@app.route('/sfhome')
def sf_historic_home():
    return render_template('sfhome.html')

@app.route('/redirect')
def redirect_url():
    return render_template('redirect.html')

##### Historic Report Start ####

@app.route('/hsnew', methods=['GET', 'POST'])
def hs_add_new():
    if request.method == "POST":
        db_name = request.form['dbname']
        db_desc = request.form['dbdesc']
        cursor = mysql.connection.cursor()

        try:
            # update created database info in robothistoric.project table
            cursor.execute("INSERT INTO rfarchive.project ( pid, name, description, created, updated, total, percentage) VALUES (0, '%s', '%s', NOW(), NOW(), 0, 0);" % (db_name, db_desc))
            mysql.connection.commit()
        except Exception as e:
            print(str(e))

        finally:
            return redirect(url_for('hshome'))
    else:
        return render_template('hsnew.html')

##### Historic Report End ####

####  Snow Report Start ####

@app.route('/spnew', methods=['GET', 'POST'])
def sp_add_new():
    if request.method == "POST":
        db_name = request.form['dbname']
        db_desc = request.form['dbdesc']
        cursor = mysql.connection.cursor()

        try:
            # update created database info in robothistoric.project table
            cursor.execute("INSERT INTO rfarchive.project ( pid, name, description, created, updated, total) VALUES (0, '%s', '%s', NOW(), NOW(), 0);" % (db_name, db_desc))
            mysql.connection.commit()
        except Exception as e:
            print(str(e))

        finally:
            return redirect(url_for('sphome'))
    else:
        return render_template('spnew.html')

#### Snow Report End ####

#### SF Report Start ####

@app.route('/sfnew', methods=['GET', 'POST'])
def sf_add_new():
    if request.method == "POST":
        db_name = request.form['dbname']
        db_desc = request.form['dbdesc']
        cursor = mysql.connection.cursor()

        try:
            # update created database info in robothistoric.project table
            cursor.execute("INSERT INTO rfarchive.project ( pid, name, description, created, updated, total) VALUES (0, '%s', '%s', NOW(), NOW(), 0);" % (db_name, db_desc))
            mysql.connection.commit()
        except Exception as e:
            print(str(e))

        finally:
            return redirect(url_for('sfhome'))
    else:
        return render_template('sfnew.html')

#### SF Report End ####

def main():
    args = parse_options()
    app.config['MYSQL_HOST'] = args.sqlhost
    app.config['MYSQL_USER'] = args.username
    app.config['MYSQL_PASSWORD'] = args.password
    app.config['auth_plugin'] = 'mysql_native_password'
    app.run(host=args.apphost, port=args.appport)