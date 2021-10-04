from flask import Flask, request, Response
import mariadb
import json
import dbcreds
import sys

app = Flask(__name__)

@app.route('/api/feed', methods = ['GET', 'POST', 'PATCH', 'DELETE'])
def feed_posts():
    conn = mariadb.connect(user=dbcreds.user,password=dbcreds.password,host=dbcreds.host,port=dbcreds.port,database=dbcreds.database)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM posts")
    all_posts = cursor.fetchall()
    cursor.close()
    conn.close()
    return Response(json.dumps(all_posts, default=str),
                                mimetype='application/json',
                                status=200)


if(len(sys.argv) > 1):
    mode = sys.argv[1]
    if(mode == "production"):
        import bjoern
        host = "0.0.0.0"
        port = 5000
        print("server is running in production code")
        bjoern.run(app,host, port )
    elif(mode == "testing"):
        from flask_cors import CORS
        CORS(app)
        print("server is running in testing mode, switch to production when needed")
        app.run(debug=True)
    else:
        print("invalid mode arguments, exiting")
        exit()
else:
    print("There was no argument provided")
    exit()