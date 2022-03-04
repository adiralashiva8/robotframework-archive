import mysql.connector
import logging

def rfarchive_setup(opts):

    # connect to database
    print("INFO: Connecting to dB")
    mydb = connect_to_mysql(opts.host, opts.username, opts.password)

    # create new user
    obj = mydb.cursor()
 
    print("INFO: Creating rfarchive dB")
    try:
        obj.execute("CREATE DATABASE IF NOT EXISTS rfarchive;")
    except Exception as e:
        print(str(e))

    print("INFO: Creating required tables")
    rfdb = connect_to_mysql_db(opts.host, opts.username, opts.password, "rfarchive")
    try:
        rfobj = rfdb.cursor()
        rfobj.execute("CREATE TABLE IF NOT EXISTS project ( pid INT NOT NULL auto_increment primary key, name TEXT, image TEXT, created DATETIME, updated DATETIME, total INT, percentage FLOAT);")
        rfobj.execute("CREATE TABLE IF NOT EXISTS execution ( eid INT NOT NULL auto_increment primary key, pid INT, description TEXT, time DATETIME, total INT, pass INT, fail INT, skip INT, etime TEXT);")
        rfobj.execute("CREATE TABLE IF NOT EXISTS test ( tid INT NOT NULL auto_increment primary key, eid INT, pid INT, name TEXT, status TEXT, time TEXT, error TEXT, comment TEXT, assigned TEXT, eta TEXT, review TEXT, type TEXT, tag TEXT, updated DATETIME);")
    except Exception as e:
        print(str(e))

    commit_and_close_db(mydb)

def connect_to_mysql(host, user, pwd):
    try:
        mydb = mysql.connector.connect(
            host=host,
            user=user,
            passwd=pwd
        )
        return mydb
    except Exception as e:
        print(e)

def connect_to_mysql_db(host, user, pwd, db):
    try:
        mydb = mysql.connector.connect(
            host=host,
            user=user,
            passwd=pwd,
            database=db
        )
        return mydb
    except Exception as e:
        print(e)

def commit_and_close_db(db):
    db.commit()
    db.close()