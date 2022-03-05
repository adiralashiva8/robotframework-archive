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

@app.route('/redirect')
def redirect_url():
    return render_template('redirect.html')

##### Historic Report Start ####

@app.route('/hshome', methods=['GET', 'POST'])
def historic_home():
    if request.method == "POST":
        search = request.form['search']
        cursor = mysql.connection.cursor()
        use_db(cursor, "rfarchive")
        cursor.execute("SELECT * FROM hsproject WHERE name LIKE '%{name}%';".format(name=search))
        data = cursor.fetchall()
        return render_template('hshome.html', data=data)
    else:
        cursor = mysql.connection.cursor()
        use_db(cursor, "rfarchive")
        cursor.execute("SELECT * FROM hsproject;")
        data = cursor.fetchall()
        return render_template('hshome.html', data=data)

@app.route('/hsnew', methods=['GET', 'POST'])
def hs_add_new():
    if request.method == "POST":
        db_name = request.form['dbname']
        db_desc = request.form['dbdesc']
        cursor = mysql.connection.cursor()

        try:
            cursor.execute("INSERT INTO rfarchive.hsproject ( pid, name, description, created, updated, total, percentage) VALUES (0, '%s', '%s', NOW(), NOW(), 0, 0);" % (db_name, db_desc))
            mysql.connection.commit()
        except Exception as e:
            print(str(e))

        finally:
            return redirect(url_for('historic_home'))
    else:
        return render_template('hsnew.html')

@app.route('/<db>/hsdeldbconf', methods=['GET'])
def hs_delete_db_conf(db):
    return render_template('hsdeldbconf.html', db_name = db)

@app.route('/<db>/hsdelete', methods=['GET'])
def hs_delete_db(db):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM rfarchive.hsproject WHERE pid='%s';" % db)
    mysql.connection.commit()
    return redirect(url_for('historic_home'))

##### Historic Report End ####

####  Snow Report Start ####

@app.route('/sphome', methods=['GET', 'POST'])
def sp_historic_home():
    if request.method == "POST":
        search = request.form['search']
        cursor = mysql.connection.cursor()
        use_db(cursor, "rfarchive")
        cursor.execute("SELECT * FROM spproject WHERE name LIKE '%{name}%';".format(name=search))
        data = cursor.fetchall()
        return render_template('sphome.html', data=data)
    else:
        cursor = mysql.connection.cursor()
        use_db(cursor, "rfarchive")
        cursor.execute("SELECT * FROM spproject;")
        data = cursor.fetchall()
        return render_template('sphome.html', data=data)

@app.route('/spnew', methods=['GET', 'POST'])
def sp_add_new():
    if request.method == "POST":
        db_name = request.form['dbname']
        db_desc = request.form['dbdesc']
        cursor = mysql.connection.cursor()

        try:
            cursor.execute("INSERT INTO rfarchive.spproject ( pid, name, description, created, updated, total) VALUES (0, '%s', '%s', NOW(), NOW(), 0);" % (db_name, db_desc))
            mysql.connection.commit()
        except Exception as e:
            print(str(e))

        finally:
            return redirect(url_for('sp_historic_home'))
    else:
        return render_template('spnew.html')

@app.route('/<db>/spdeldbconf', methods=['GET'])
def sp_delete_db_conf(db):
    return render_template('spdeldbconf.html', db_name = db)

@app.route('/<db>/spdelete', methods=['GET'])
def sp_delete_db(db):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM rfarchive.spproject WHERE pid='%s';" % db)
    mysql.connection.commit()
    return redirect(url_for('sp_historic_home'))

#### Snow Report End ####

#### SF Report Start ####

@app.route('/sfhome', methods=['GET', 'POST'])
def sf_historic_home():
    if request.method == "POST":
        search = request.form['search']
        cursor = mysql.connection.cursor()
        use_db(cursor, "rfarchive")
        cursor.execute("SELECT * FROM sfproject WHERE name LIKE '%{name}%';".format(name=search))
        data = cursor.fetchall()
        return render_template('sfhome.html', data=data)
    else:
        cursor = mysql.connection.cursor()
        use_db(cursor, "rfarchive")
        cursor.execute("SELECT * FROM sfproject;")
        data = cursor.fetchall()
        return render_template('sfhome.html', data=data)

@app.route('/sfnew', methods=['GET', 'POST'])
def sf_add_new():
    if request.method == "POST":
        db_name = request.form['dbname']
        db_desc = request.form['dbdesc']
        cursor = mysql.connection.cursor()

        try:
            cursor.execute("INSERT INTO rfarchive.sfproject ( pid, name, description, created, updated, total) VALUES (0, '%s', '%s', NOW(), NOW(), 0);" % (db_name, db_desc))
            mysql.connection.commit()
        except Exception as e:
            print(str(e))

        finally:
            return redirect(url_for('sf_historic_home'))
    else:
        return render_template('sfnew.html')

@app.route('/<db>/sfdeldbconf', methods=['GET'])
def sf_delete_db_conf(db):
    return render_template('sfdeldbconf.html', db_name = db)

@app.route('/<db>/sfdelete', methods=['GET'])
def sf_delete_db(db):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM rfarchive.sfproject WHERE pid='%s';" % db)
    mysql.connection.commit()
    return redirect(url_for('sf_historic_home'))

#### SF Report End ####
def use_db(cursor, db_name):
    cursor.execute("USE %s;" % db_name)

def main():
    args = parse_options()
    app.config['MYSQL_HOST'] = args.sqlhost
    app.config['MYSQL_USER'] = args.username
    app.config['MYSQL_PASSWORD'] = args.password
    app.config['auth_plugin'] = 'mysql_native_password'
    app.run(host=args.apphost, port=args.appport)