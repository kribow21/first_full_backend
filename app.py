from flask import Flask, request, Response
import mariadb
import json
import dbcreds
import sys
app = Flask(__name__)

@app.route('/api/feed', methods = ['GET', 'POST', 'PATCH', 'DELETE'])
def feed_posts():
    if request.method == 'GET':
        conn = mariadb.connect(user=dbcreds.user,password=dbcreds.password,host=dbcreds.host,port=dbcreds.port,database=dbcreds.database)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM posts")
        all_posts = cursor.fetchall()
        post_list = []
        for post in all_posts:
            postDict = {
                "username" : post[0],
                "id" : post[1],
                "content" : post[2],
                "time_created" : post[3]
            }
            post_list.append(postDict)

        cursor.close()
        conn.close()
        return Response(json.dumps(post_list, default=str),
                                    mimetype='application/json',
                                    status=200)
    elif request.method == 'POST':
        post_data = request.json
        print(post_data)
        post_username = post_data.get("username")
        post_content = post_data.get("content")
        post_date = post_data.get("time_created")
        conn = mariadb.connect(user=dbcreds.user,password=dbcreds.password,host=dbcreds.host,port=dbcreds.port,database=dbcreds.database)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO posts(username, content, time_created) VALUES (?,?,?)",[post_username, post_content, post_date])
        if(cursor.rowcount ==1):
            conn.commit()
            cursor.close()
            conn.close()
            return Response("Sucessful post created",
                        mimetype='text/plain',
                        status=200)
        else:
            return Response("Something went wrong, post not created",
                            mimetype="text/plain",
                            status=400)


    elif request.method == 'PATCH':
        edited_data = request.json
        print(edited_data)
        patched_content = edited_data.get("content")
        post_id = edited_data.get("id")
        conn = mariadb.connect(user=dbcreds.user,password=dbcreds.password,host=dbcreds.host,port=dbcreds.port,database=dbcreds.database)
        cursor = conn.cursor()
        cursor.execute("UPDATE posts SET content=? WHERE id=?",[patched_content, post_id])
        conn.commit()
        cursor.close()
        conn.close()
        return Response("Edit sucessful",
                        mimetype='text/plain',
                        status=200)
    elif request.method == 'DELETE':
        remove_data = request.json
        user_id = remove_data.get("id")
        conn = mariadb.connect(user=dbcreds.user,password=dbcreds.password,host=dbcreds.host,port=dbcreds.port,database=dbcreds.database)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM posts WHERE id=?",[user_id,])
        conn.commit()
        cursor.close()
        conn.close()
        return Response("Post deleted",
                        mimetype='text/plain',
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