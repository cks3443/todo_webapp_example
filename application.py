import datetime
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/Real_G4/Desktop/todo_app_0/db.sqlite'

db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job = db.Column(db.String(500), nullable=False)
    at_created = db.Column(db.DateTime, default=datetime.datetime.utcnow() )
    active = db.Column(db.Boolean)


@app.route('/', methods=['GET', 'POST', 'DELETE', 'PUT'])
def index():

    dat = {}
    dat['tasks'] = Task.query.all()

    if request.method == 'GET' :
        return render_template('index.html', **dat)
    
    elif request.method == 'POST':
        pjob = request.form['job']

        if pjob == '':
            return redirect(url_for('index'))

        t = Task(job=pjob, active=True)
        db.session.add(t)
        db.session.commit()

        return redirect(url_for('index'))
    
    elif request.method == 'DELETE':
        id = request.form['id']
        tid = Task.query.get(id)
        db.session.delete(tid)
        db.session.commit()
    
        resp = jsonify(success=True)
        return resp 
    
    elif request.method == 'PUT':
        id = request.form['id']
        tid = Task.query.get(id)

        tid.active = False if tid.active == True else True
        
        db.session.commit()
    
        resp = jsonify(success=True)
        return resp 


if __name__ == '__main__':
    app.run(debug=True, port=5000)