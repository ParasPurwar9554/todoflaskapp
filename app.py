from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Create a SQLAlchemy instance
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    datetime_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"{self.sno} - {self.title}"


@app.route('/',methods =['GET','POST'])
def home():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo(title=title,desc=desc)
        # Add the user to the session
        db.session.add(todo)
         # Commit the session to save the changes
        db.session.commit()
         #print("User added successfully!")
    allTodos = Todo.query.all()
    return render_template('index.html',allTodos= allTodos)

@app.route('/show')
def products():
    allTodos = Todo.query.all()
    print(allTodos)
    return "Hello, Products"    

@app.route('/delete/<int:sno>')
def delete(sno):
    record_to_delete = Todo.query.filter_by(sno=sno).first()
    #record_to_delete = db.session.query(Todo).filter_by(sno=sno)
    db.session.delete(record_to_delete)
    db.session.commit()  # Save changes
    print("Record deleted successfully!")   
    return redirect('/')   

@app.route('/update/<int:sno>',methods =['GET','POST'])
def update(sno):
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo.query.filter_by(sno=sno).first()
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect('/')
    todo = Todo.query.filter_by(sno=sno).first()    
    return render_template('update.html',todo = todo)

if __name__ == '__main__':
     with app.app_context():
        try:
            db.create_all()
            print("Database and tables created successfully!")
        except Exception as e:
            print(f"Error: {e}")
        app.run(debug=True,port = 8000)
    
