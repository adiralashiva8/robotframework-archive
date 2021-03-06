import os
import mysql.connector
import logging
import math
import time
import pandas as pd
import numpy as np
import datetime
from datetime import timedelta

def sfhistoric_parser(opts):

    if opts.ignoreresult == "True":
        print("Ignoring execution results...")
        return

    # Read output.xml file
    print("Capturing execution results, This may take few minutes...")

    # connect to database
    rootdb = connect_to_mysql_db(opts.host, opts.username, opts.password, 'rfarchive')

    # insert test results info into db
    df = pd.read_csv(opts.output)
    table = pd.pivot_table(df, index=["test_case_name","date_time"], values=["ept_time"])
    
    for line in table.to_csv(header=False, index=True).split('\n'):
        if line:
            values = line.split(',')
            result_id = insert_into_execution_table(rootdb, opts.projectid, str(values[1]))
            break

    for line in table.to_csv(header=False, index=True).split('\n'):
        if line:
            values = line.split(',')
            insert_into_test_table(rootdb, result_id, opts.projectid, str(values[0]), float(values[2]))

    print("INFO: Writing execution results to tables")
    commit_and_close_db(rootdb)

# other useful methods
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

def insert_into_execution_table(con, pid, description):
    cursorObj = con.cursor()
    sql = "INSERT INTO rfarchive.sfexecution (eid, pid, description, time) VALUES (%s, %s, %s, now());"
    val = (0, pid, description)
    cursorObj.execute(sql, val)
    con.commit()
    cursorObj.execute("SELECT eid FROM rfarchive.sfexecution WHERE pid='%s' ORDER BY eid DESC LIMIT 1;" % (pid))
    rows = cursorObj.fetchone()
    cursorObj.execute("SELECT COUNT(*) FROM rfarchive.sfexecution WHERE pid='%s';" % (pid))
    execution_rows = cursorObj.fetchone()
    cursorObj.execute("UPDATE rfarchive.sfproject SET updated=now(), total=%s WHERE pid='%s';" % (execution_rows[0], pid))
    con.commit()
    return str(rows[0])

def insert_into_test_table(con, eid, pid, table_name, ept_time):
    cursorObj = con.cursor()
    sql = "INSERT INTO rfarchive.sftest (tid, eid, pid, name, ept_time) VALUES (%s, %s, %s, %s, %s)"
    val = (0, eid, pid, table_name, ept_time)
    cursorObj.execute(sql, val)

def commit_and_close_db(db):
    db.commit()