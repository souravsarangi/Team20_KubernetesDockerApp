from flask import *
#from redis import Redis
import os

app = Flask(__name__,template_folder='.')
#redis = Redis(host="redis_1", port=6379)

'''@app.route('/add',methods=['GET'])
def hello():
# redis.incr('hits')
#   return 'Hello Docker Training! I have been seen {0} times'.format(redis.get('hits'))
	f=os.open('db','a')
	name=request.args['name']
	rollno=request.args['rollno']
	s=name+' '+rollno+'\n'
	f.write(s)
	f.close()
	return 'fdsfdsf'
'''	
@app.route('/show')

def show():
    f=open('db','r')
    x=f.readlines()
    str1=''
    for i in x:
        j=i.split(' ')
        str1+=j[0]
        for k in range(70-len(j[0])):
  	        str1+='&nbsp;'
        str1+=j[1]+'<br/>'
    print str1+"hoooooo"
    f.close()
    return str1

@app.route('/')
def form():
	print "hello\n"
	return render_template('index.html')
	
@app.route('/fill', methods=['GET'])
def form_post():
    print "vdffdfd"
    name = request.args['name']
    rollno = request.args['rollno']
    f=open('db','a')
    name=request.args['name']
    rollno=request.args['rollno']
    s=name+' '+rollno+'\n'
    print s
    f.write(s)
    f.close()
    return redirect('/')

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
