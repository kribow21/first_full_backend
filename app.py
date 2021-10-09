from flask import Flask, request, Response
import mariadb
import json
import dbcreds
import sys


app = Flask(__name__)

@app.route('/api/feed', methods = ['GET', 'POST', 'PATCH', 'DELETE'])
def feed_posts():
    conn= None
    cursor=None
    if request.method == 'GET':
        try:
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
            return Response(json.dumps(post_list, default=str),
                mimetype='application/json',
                status=200)
        except mariadb.DataError: 
            print('Something went wrong with your data')
        except mariadb.OperationalError:
            print('Something wrong with the connection')
        except mariadb.ProgrammingError:
            print('Your query was wrong')
        except mariadb.IntegrityError:
            print('Your query would have broken the database and we stopped it')
        except mariadb.InterfaceError:
            print('Something wrong with database interface')
        except:
            print('Something went wrong')
        finally:
            if(cursor != None):
                cursor.close()
                print('cursor closed')
            else:
                print('no cursor to begin with')
            if(conn != None):   
                conn.rollback()
                conn.close()
                print('connection closed')
            else:
                print('the connection never opened, nothing to close')


    elif request.method == 'POST':
        post_data = request.json
        print(post_data)
        post_username = post_data.get("username")
        post_content = post_data.get("content")
        post_date = post_data.get("time_created")
        if_empty = {
            "message" : "Enter in required data"
        }
        try:
            if (post_username == ''):
                return Response(json.dumps(if_empty),
                                mimetype='application/json',
                                status=409)
            elif (post_content == ''):
                return Response(json.dumps(if_empty),
                                mimetype='application/json',
                                status=409)
            elif (post_date == ''):
                return Response(json.dumps(if_empty),
                                mimetype='application/json',
                                status=409)
            conn = mariadb.connect(user=dbcreds.user,password=dbcreds.password,host=dbcreds.host,port=dbcreds.port,database=dbcreds.database)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO posts(username, content, time_created) VALUES (?,?,?)",[post_username, post_content, post_date])
            if(cursor.rowcount ==1):
                conn.commit()
                return Response("Sucessful post created",
                            mimetype='text/plain',
                            status=200)
            else:
                return Response("Something went wrong, post not created",
                                mimetype="text/plain",
                                status=400)
        except mariadb.DataError: 
            print('Something went wrong with your data')
        except mariadb.OperationalError:
            print('Something wrong with the connection')
        except mariadb.ProgrammingError:
            print('Your query was wrong')
        except mariadb.IntegrityError:
            print('Your query would have broken the database and we stopped it')
        except mariadb.InterfaceError:
            print('Something wrong with database interface')
        except:
            print('Something went wrong')
        finally:
            if(cursor != None):
                cursor.close()
                print('cursor closed')
            else:
                print('no cursor to begin with')
            if(conn != None):   
                conn.rollback()
                conn.close()
                print('connection closed')
            else:
                print('the connection never opened, nothing to close')

    elif request.method == 'PATCH':
        edited_data = request.json
        print(edited_data)
        patched_content = edited_data.get("content")
        post_id = edited_data.get("id")
        wrong_type = {
                    "message" : "id is expecting an integer. try again"
                    }
        sucess_edit = {
                    "message" : "Post is now edited"
                    }
        if(isinstance(post_id, int) == False):
            return Response(json.dumps(wrong_type ,default=str),
                                    mimetype='application/json',
                                    status=409)
        try:
            conn = mariadb.connect(user=dbcreds.user,password=dbcreds.password,host=dbcreds.host,port=dbcreds.port,database=dbcreds.database)
            cursor = conn.cursor()
            cursor.execute("UPDATE posts SET content=? WHERE id=?",[patched_content, post_id])
            conn.commit()
            return Response(json.dumps(sucess_edit, default=str),
                        mimetype='application/json',
                        status=200)
        except mariadb.DataError: 
            print('Something went wrong with your data')
        except mariadb.OperationalError:
            print('Something wrong with the connection')
        except mariadb.ProgrammingError:
            print('Your query was wrong')
        except mariadb.IntegrityError:
            print('Your query would have broken the database and we stopped it')
        except mariadb.InterfaceError:
            print('Something wrong with database interface')
        except:
            print('Something went wrong')
        finally:
            if(cursor != None):
                cursor.close()
                print('cursor closed')
            else:
                print('no cursor to begin with')
            if(conn != None):   
                conn.rollback()
                conn.close()
                print('connection closed')
            else:
                print('the connection never opened, nothing to close')
    elif request.method == 'DELETE':
        remove_data = request.json
        user_id = remove_data.get("id")
        wrong_type = {
                    "message" : "id is expecting an integer. try again"
                    }
        if(isinstance(user_id,int) == False):
            return Response(json.dumps(wrong_type ,default=str),
                                    mimetype='application/json',
                                    status=409)
        sucess_del = {
            "message" : "post now deleted"
        }
        fail_del = {
            "message" : "something went wrong with deleteing the post"
        }
        try:
            conn = mariadb.connect(user=dbcreds.user,password=dbcreds.password,host=dbcreds.host,port=dbcreds.port,database=dbcreds.database)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM posts WHERE id=?",[user_id,])
            if(cursor.rowcount ==1):
                conn.commit()
                return Response(json.dumps(sucess_del, default=str),
                            mimetype='application/json',
                            status=200)
            else:
                return Response(json.dumps(fail_del, default=str),
                                mimetype="application/json",
                                status=409)
        except mariadb.DataError: 
            print('Something went wrong with your data')
        except mariadb.OperationalError:
            print('Something wrong with the connection')
        except mariadb.ProgrammingError:
            print('Your query was wrong')
        except mariadb.IntegrityError:
            print('Your query would have broken the database and we stopped it')
        except mariadb.InterfaceError:
            print('Something wrong with database interface')
        except:
            print('Something went wrong')
        finally:
            if(cursor != None):
                cursor.close()
                print('cursor closed')
            else:
                print('no cursor to begin with')
            if(conn != None):   
                conn.rollback()
                conn.close()
                print('connection closed')
            else:
                print('the connection never opened, nothing to close')

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