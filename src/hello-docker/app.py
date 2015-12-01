from flask import Flask, request , jsonify
#from redis import Redis
import os

app = Flask(__name__)
#redis = Redis(host="redis_1", port=6379)

@app.route('/add',methods=['GET'])
def hello():
# redis.incr('hits')
#   return 'Hello Docker Training! I have been seen {0} times'.format(redis.get('hits'))
	f=open('db','a')
	name=request.args['name']
	rollno=request.args['rollno']
	s=name+' '+rollno+'\n'
	f.write(s)
	f.close()
	return 'fdsfdsf'
	
@app.route('/show')

def show():
	f=open('db','r')
	x=f.readlines()
	str1='NAME  ROLLNO<br/>'
	for i in x:
		str1+=i+'<br/>'
	f.close()
	return str1

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
