#!/usr/bin/env python3

"""
Columbia W4111 Intro to databases
Example webserver

To run locally

    python server.py

Go to http://localhost:8111 in your browser


A debugger such as "pdb" may be helpful for debugging.
Read about it online.
"""

import json
import os

from flask import (Flask, Response, flash, g, redirect, render_template,
                   request, session, url_for)
from sqlalchemy import *
from sqlalchemy.pool import NullPool

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'findsites')
app = Flask(__name__, template_folder=tmpl_dir)
# app._static_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
app.secret_key = "27eduCBA09"



# XXX: The Database URI should be in the format of: 
#
#     postgresql://USER:PASSWORD@<IP_OF_POSTGRE_SQL_SERVER>/<DB_NAME>
#
# For example, if you had username ewu2493, password foobar, then the following line would be:
#
#     DATABASEURI = "postgresql://ewu2493:foobar@<IP_OF_POSTGRE_SQL_SERVER>/postgres"
#
# For your convenience, we already set it to the class database

# Use the DB credentials you received by e-mail
DB_USER = "dz2451"
DB_PASSWORD = "7278"

DB_SERVER = "w4111.cisxo09blonu.us-east-1.rds.amazonaws.com"

DATABASEURI = "postgresql://"+DB_USER+":"+DB_PASSWORD+"@"+DB_SERVER+"/proj1part2"  #"/w4111" 


#
# This line creates a database engine that knows how to connect to the URI above
#
engine = create_engine(DATABASEURI)


# # Here we create a test table and insert some values in it
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
    print("uh oh, problem connecting to database")
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
# def index():
#   """
#   request is a special object that Flask provides to access web request information:

#   request.method:   "GET" or "POST"
#   request.form:     if the browser submitted a form, this contains the data in the form
#   request.args:     dictionary of URL arguments e.g., {a:1, b:2} for http://localhost?a=1&b=2

#   See its API: http://flask.pocoo.org/docs/0.10/api/#incoming-request-data
#   """

#   # DEBUG: this is debugging code to see what request looks like
# #   print( request.args )
#   session['new_filter'] = None


#   #
#   # example of a database query
#   #
# #   cursor = g.conn.execute("SELECT zip_code FROM site_located")
# #   names = []
# #   for result in cursor:
# #     names.append(result['zip_code'])  # can also be accessed using result[0]
# #   cursor.close()
# #   print(names)

#   #
#   # Flask uses Jinja templates, which is an extension to HTML where you can
#   # pass data to a template and dynamically generate HTML based on the data
#   # (you can think of it as simple PHP)
#   # documentation: https://realpython.com/blog/python/primer-on-jinja-templating/
#   #
#   # You can see an example template in templates/index.html
#   #
#   # context are the variables that are passed to the template.
#   # for example, "data" key in the context variable defined below will be 
#   # accessible as a variable in index.html:
#   #
#   #     # will print: [u'grace hopper', u'alan turing', u'ada lovelace']
#   #     <div>{{data}}</div>
#   #     
#   #     # creates a <div> tag for each element in data
#   #     # will print: 
#   #     #
#   #     #   <div>grace hopper</div>
#   #     #   <div>alan turing</div>
#   #     #   <div>ada lovelace</div>
#   #     #
#   #     {% for n in data %}
#   #     <div>{{n}}</div>
#   #     {% endfor %}
#   #
# #   context = dict(data = names)


#   #
#   # render_template looks in the templates/ folder for files.
#   # for example, the below file reads template/index.html
#   #
#   return render_template("filter_service.html") # ,**context)

def index():
    session['new_filter'] = None
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template("filter_service.html")

#
# This is an example of a different path.  You can see it at
# 
#     localhost:8111/another
#
# notice that the functio name is another() rather than index()
# the functions for each app.route needs to have different names
#

#Make an appointment
@app.route('/add_appo/<site_id>', methods=['POST'])
def add_appo(site_id):
  date = request.form['date']
  time = request.form['time']
  user_id = session['user_id']
  vaccine_id = request.form['v_type']

  cmd = 'INSERT INTO appointment VALUES ((select max(appoint_id)+1 from appointment),:date, :time, :vaccine_id, :user_id, :site_id)';
  g.conn.execute(text(cmd), date = date, time = time, vaccine_id = vaccine_id, user_id= user_id, site_id = site_id);
  return redirect(url_for('site_detail',site_id=site_id))

def add_comment(site_id):
    ##how to get user info?
    print( request.form )
    comment = request.form['comment']
    service = request.form['service_type']
    star = request.form['star']
    print( comment, service, star )
    
    ##??? how to get user info
    user = 5
    cmd1 = """
        DROP TABLE if EXISTS newid;
        CREATE TABLE newid AS ( SELECT max(comment_id)+1 AS new FROM comments);
        INSERT INTO comments VALUES ((select * from newid), :star,:comment,:service);
        INSERT INTO evaluate VALUES ((select * from newid), :user, :site_id);
    """
    print(cmd1)
    g.conn.execute( text(cmd1), star=star,comment=comment,service=service,user=str(user),site_id=site_id ) 
    return redirect(url_for('site_detail',site_id=site_id))

# Filter the service type for sites
@app.route('/filter_service', methods=['POST'])
def filter_service():
  all = request.form
  print( all )
  
  session['zip'] = all['zip']
  session['service'] = list(all.keys())[1:]
  
  return  redirect('/site_map')


@app.route('/site_map')
def site_map():
    zip = session.get('zip',None)
    new_filter = session.get('new_filter',None)
    print(zip,new_filter)
    
    if new_filter==None:
        serv_id = session.get('service',None)
        if len(serv_id)==0:
            serv_id = ['vacc','test','anti']
        supply = []
        vacc = []
        test = []
        anti = []
    else:
        serv_id = new_filter['serv_id']
        supply = new_filter['supply']
        vacc = new_filter['vacc']
        test = new_filter['test']
        anti = new_filter['anti']
#         supply = ['pfizer','moderna','jj']
#         vacc = ['walk_in','insurance']
#         test = ['rapid','PCR']
#         anti = ['PCR_test','kit_test']
    status = [*serv_id, *supply, *vacc, *test, *anti]
    status2 = json.dumps(status)
    print(status2)
        
    service_table = dict(vacc='vaccination_site',test='testing_site',anti='antibody_testing')
    service_input = ",".join(list(map(lambda x: service_table[x], serv_id)))
    service_query = list(map(lambda x: 'S.site_id = %s.site_id' % service_table[x], serv_id))
    serv_query = " OR ".join(service_query)
    print(serv_query)
    
    ###??? vaccine supply not added yet ####
    
    filter = []
    if "vacc" in serv_id:
        for f in vacc:
            filter.append('vaccination_site.%s = \'T\' ' % f)
    if "test" in serv_id:
        for f in test:
            filter.append('testing_site.%s = \'T\' ' % f)
    if "anti" in serv_id:
        for f in anti:
            filter.append('antibody_testing.%s = \'T\' ' % f)
    
    if len(filter) != 0:
        filter = "AND ".join(filter)
        filter = "AND " + filter
    else:
        filter = ""
    print(filter)

    cmd = """
      SELECT distinct S.site_id, S.name, S.address, S.website, S.call, S.latitude, S.longitude
      FROM site S, site_located SL, %s
      WHERE S.site_id = SL.site_id AND SL.zip_code = '%s' AND (%s) %s
    """

    cursor = g.conn.execute( cmd % (service_input, zip, serv_query, filter) )     #serv=service_input,zip=zip,serv_query=serv_query,filter=filter)
    rows = cursor.mappings().all()
#     rows = []
#     for result in cursor:
#     rows.append(dict(site_id=result['site_id'],
#                      name=result['name'],
#                      address=result['address'],
#                      website=result['website'],
#                      call=result['call']) )
    cursor.close()
    print(rows)

    context = dict(status=status2, zip=zip, service=serv_id, cmd=(cmd % (service_input, zip, serv_query, filter)), rows=rows)
    print(context)
    
    session['new_filter'] = None

    return render_template("site_map.html",**context)


@app.route('/filter_bar', methods=['POST'])
def filter_bar():
    serv_id = request.form.getlist('service')
    supply = request.form.getlist('supply')
    vacc = request.form.getlist('vacc')
    test = request.form.getlist('test')
    anti = request.form.getlist('anti')
    all = dict(serv_id=serv_id, supply=supply, vacc=vacc, test=test, anti=anti)
    print( all )
    
    session['new_filter'] = all

    return  redirect('/site_map')


@app.route('/site_detail/<site_id>')
def site_detail(site_id):
    site_id = int(site_id)
    
#     cmd1 = """
#         SELECT * 
#         FROM ((site S LEFT OUTER JOIN vaccination_site VS ON S.site_id=VS.site_id) 
#                 LEFT OUTER JOIN testing_site TS ON S.site_id=TS.site_id )
#                 LEFT OUTER JOIN antibody_testing AT ON S.site_id=AT.site_id )
#         WHERE S.site_id=%d
#     """
    cmd1 = 'SELECT * FROM site WHERE site_id=%d'
    cursor = g.conn.execute(cmd1 % site_id)
    rows = cursor.mappings().all()
#     for result in cursor:
#         print(result)
#         rows = dict(site_id=result['site_id'],
#                      name=result['name'],
#                      address=result['address'],
#                      website=result['website'],
#                      call=result['call']) 
    cursor.close()
    print(rows)
    
    cmd2 = """
        SELECT distinct *
        FROM vaccine_supply VS, vaccine V
        WHERE VS.vaccine_id = V.vaccine_id AND VS.site_id = %d
    """
    cursor = g.conn.execute(cmd2 % site_id)
    vacc = []
    for result in cursor:
        vacc.append(dict(brand=result['brand'],
                         in_stock = "In Stock" if result['in_stock']==True else "Out Of Stock",
                         updated_date = result['updated_date']) )
    cursor.close()
    print(vacc)
    
    cmd3 = """
        SELECT * FROM open_hour 
        WHERE site_id = %d
        ORDER BY 
          CASE
              WHEN weekday = 'Sunday' THEN 1
              WHEN weekday = 'Monday' THEN 2
              WHEN weekday = 'Tuesday' THEN 3
              WHEN weekday = 'Wednesday' THEN 4
              WHEN weekday = 'Thursday' THEN 5
              WHEN weekday = 'Friday' THEN 6
              WHEN weekday = 'Saturday' THEN 7
         END ASC
        """
    
    cursor = g.conn.execute(cmd3 % site_id)
    hour = []
    for result in cursor:
        hour.append(dict(weekday=result['weekday'],
                         open = result['open_at'],
                         close = result['close_at']) )
    cursor.close()
    print(hour)
    
    cmd4 = 'SELECT * FROM vaccination_site WHERE site_id = %d'
    cursor = g.conn.execute(cmd4 % site_id)
    more1=[]
    for result in cursor:
        more1 = dict(Walkin = "Walkins accepted" if result['walk_in']=="true" else "Walkins NOT accepted",
                     Insurance = "Insurance applicable" if result['insurance']=="true" else "Insurance NOT applicable")
    cursor.close()
    if (more1==[]):
        more1 = [False, "Vaccination not provided"]
    else:
        more1 = [True,more1]
    print(more1)
    
    cmd5 = 'SELECT * FROM testing_site WHERE site_id = %d'
    cursor = g.conn.execute(cmd5 % site_id)
    more2 = []
    for result in cursor:
        more2 = dict(rapid = '√' if result['rapid']=='T' else '×',
                      pcr = '√' if result['pcr']=='T' else '×') 
#     more2 = cursor.mappings().all()
    if (more2==[]):
        more2 = [False, "Covid-19 testing not provided"]
    else:
        more2 = [True, more2]
    cursor.close()
    print(more2)
    
    cmd6 = 'SELECT * FROM antibody_testing WHERE site_id = %d'
    cursor = g.conn.execute(cmd6 % site_id)
    more3 = cursor.mappings().all()
    if (more3==[]):
        more3 = [False, "Antibody testing not provided"]
    else:
        for result in cursor:
            more3 = dict(pcr = '√' if result['pcr_test']=='T' else '×',
                         kit = '√' if result['kit_test']=='T' else '×')
        more3 = [True, more3]
    cursor.close()
    print(more3)
    
    cmd7 = """
        SELECT C.star, C.content, C.service_type, U.name
        FROM evaluate E, comments C, users U
        WHERE E.site_id = %d AND E.comment_id=C.comment_id AND E.user_id=U.user_id
    """
    cursor = g.conn.execute(cmd7 % site_id)
    comment = []
    for result in cursor:
        comment.append(dict(star = result['star'],
                            content = result['content'],
                            service = result['service_type'],
                            rater = result['name']) )
    cursor.close()
    print(comment)
    
    context = dict(site_id=site_id, rows=rows, vacc=vacc, hour=hour, more1=more1, more2=more2, more3=more3,comment=comment)
    print(context)
    
    return render_template("site_detail.html",**context)
    
    
@app.route('/add_comment/<site_id>', methods=['POST'])
def add_comment(site_id):
    ##how to get user info?
    print( request.form )
    comment = request.form['comment']
    service = request.form['service_type']
    star = request.form['star']
    print( comment, service, star )
    
    ##??? how to get user info
    user = 5
    cmd1 = """
        DROP TABLE if EXISTS newid;
        CREATE TABLE newid AS ( SELECT max(comment_id)+1 AS new FROM comments);
        INSERT INTO comments VALUES ((select * from newid), :star,:comment,:service);
        INSERT INTO evaluate VALUES ((select * from newid), :user, :site_id);
    """
    print(cmd1)
    g.conn.execute( text(cmd1), star=star,comment=comment,service=service,user=str(user),site_id=site_id ) 
    return redirect(url_for('site_detail',site_id=site_id))
    

                    
   

# # Example of adding new data to the database
# @app.route('/add', methods=['POST'])
# def add():
#   name = request.form['name']
#   print( name )
#   cmd = 'INSERT INTO test(name) VALUES (:name1), (:name2)';
#   g.conn.execute(text(cmd), name1 = name, name2 = name);
#   return redirect('/')

# @app.route('/login_page')
# def login_page():
#     return render_template("login.html")

@app.route('/login', methods=['POST'])
def login():
    name = request.form['usrname']
    print(name)
    if request.form['psw'] == 'admin' and name == 'admin':
        session['logged_in'] = True
        session['user_id'] = 10086
        
    elif request.form['psw'] == 'user' and name == 'user':
        session['logged_in'] = True
        cmd = """
            SELECT user_id FROM users WHERE name = '%s'
        """
        cursor = g.conn.execute(cmd % str(name))
        print(cmd % name)
        user_id = cursor.mappings().all()
        cursor.close()
        print(user_id)
        session['user_id'] = user_id
    else:
        flash('wrong password!')
    return redirect('/')

@app.route("/logout", methods=['POST'])
def logout():
    session['logged_in'] = False
    flash('Successfully loged out!')
    return redirect('/')

@app.route("/signup")
def signup():
#     cmd = """
#         INSERT INTO users(name)
#     """
    return redirect('/')


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
    print( "running on %s:%d" % (HOST, PORT) )
    app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)


  run()
