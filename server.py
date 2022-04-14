#!/usr/bin/env python2.7

"""
Columbia W4111 Intro to databases
Example webserver

To run locally

    python server.py

Go to http://localhost:8111 in your browser


A debugger such as "pdb" may be helpful for debugging.
Read about it online.
"""

import os

from flask import Flask, Response, g, redirect, render_template, request
from sqlalchemy import *
from sqlalchemy.pool import NullPool

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)

DB_USER = "dz2451"
DB_PASSWORD = "7278"

DB_SERVER = "w4111.cisxo09blonu.us-east-1.rds.amazonaws.com"

DATABASEURI = "postgresql://"+DB_USER+":"+DB_PASSWORD+"@"+DB_SERVER+"/proj1part2"
#Don't use /w4111, it needs the permission

#
# This line creates a database engine that knows how to connect to the URI above
#
engine = create_engine(DATABASEURI)


# Here we create a test table and insert some values in it
# engine.execute("""DROP TABLE IF EXISTS test;""")
# engine.execute("""CREATE TABLE IF NOT EXISTS test (
#   id serial,
#   name text
# );""")
# engine.execute("""INSERT INTO test(name) VALUES ('grace hopper'), ('alan turing'), ('ada lovelace');""")



@app.before_request
def before_request():
  """
  This function is run at the beginning of every web request 
  (every time you enter an address in the web browser).
  We use it to setup a database connection that can be used throughout the request

  The variable g is globally accessible
  """
  try:
    g.conn = engine.connect()
  except:
    print ("uh oh, problem connecting to database")
    import traceback; traceback.print_exc()
    g.conn = None

@app.teardown_request
def teardown_request(exception):
  """
  At the end of the web request, this makes sure to close the database connection.
  If you don't the database could run out of memory!
  """
  try:
    g.conn.close()
  except Exception as e:
    pass


#
# @app.route is a decorator around index() that means:
#   run index() whenever the user tries to access the "/" path using a GET request
#
# If you wanted the user to go to e.g., localhost:8111/foobar/ with POST or GET then you could use
#
#       @app.route("/foobar/", methods=["POST", "GET"])
#
# PROTIP: (the trailing / in the path is important)
# 
# see for routing: http://flask.pocoo.org/docs/0.10/quickstart/#routing
# see for decorators: http://simeonfranklin.com/blog/2012/jul/1/python-decorators-in-12-steps/
#
@app.route('/')
def index():
  return render_template("index.html")


@app.route('/another')
def another():
  context = dict(data = [], info_user = [])
  return render_template("another.html", **context)


# Example of adding new data to the database
@app.route('/add', methods=['POST'])
def add():
  name = request.form['name']
  cmd = 'INSERT INTO test(name) VALUES (:name1)';
  g.conn.execute(text(cmd), name1 = name);
  return redirect('/')

@app.route('/add_user', methods=['POST'])
def add_user():
  name = request.form['name']
  user_id = request.form['user_id']
  dof = request.form['dof']
  address = request.form['address']
  zipcode = request.form['zipcode']
  cmd = 'INSERT INTO users VALUES (:user_id, :name, :dof, :address, :zipcode)';
  g.conn.execute(text(cmd), user_id = user_id, name = name, dof = dof, address= address, zipcode = zipcode);
  return redirect('/')

@app.route('/add_appo', methods=['POST'])
def add_appo():
  appoint_id = request.form['appoint_id']
  date = request.form['date']
  time = request.form['time']
  user_id = request.form['appoint_id']
  vaccine_id = request.form['v_type']
  site_id = request.form['site_id']
  cmd = 'INSERT INTO appointment VALUES (:appoint_id, :date, :time, :vaccine_id, :user_id, :site_id)';
  g.conn.execute(text(cmd), appoint_id = appoint_id, date = date, time = time, vaccine_id = vaccine_id, user_id= user_id, site_id = site_id);
  return redirect('/')

@app.route('/search_appid', methods = ['POST'])
def search_appid():
  app_id = request.form['app_id']
  cmd = "SELECT * FROM appointment WHERE appoint_id=%s"
  cursor = g.conn.execute(cmd, app_id)
  info = []
  for result in cursor:
    info.append(result) 
  cursor.close()
  context1 = dict(data = info[0], info_user = [])
  return render_template("another.html", **context1)

@app.route('/search_user', methods = ['POST'])
def search_user():
  user_id = request.form['user_id']
  cmd = "SELECT * FROM users WHERE user_id=%s"
  cursor = g.conn.execute(cmd, user_id)
  info_user = []
  for result in cursor:
    info_user.append(result) 
  cursor.close()
  
  context2 = dict(info_user = info_user[0], data = [])
  return render_template("another.html", **context2)


@app.route('/login')
def login():
    abort(401)
    this_is_never_executed()


if __name__ == "__main__":
  import click

  @click.command()
  @click.option('--debug', is_flag=True)
  @click.option('--threaded', is_flag=True)
  @click.argument('HOST', default='0.0.0.0')
  @click.argument('PORT', default=8111, type=int)
  def run(debug, threaded, host, port):
    """
    This function handles command line parameters.
    Run the server using

        python server.py

    Show the help text using

        python server.py --help

    """

    HOST, PORT = host, port
    print ("running on %s:%d" % (HOST, PORT))
    app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)


  run()
