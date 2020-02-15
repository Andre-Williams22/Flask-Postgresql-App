from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from send_mail import send_mail

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

app = Flask(__name__)

# When we switch to Heroku we'll have a totally different database
ENV = 'prod'

if ENV == 'dev':
    app.debug=True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:fcd2201@localhost/lexus'
else:
    app.debug=False
    # Our production database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://tzpoyxfmbqoany:a5c5fbb1e9b7965541078b2fd3adb738ab6948d67b7ef4ea2cce4eebfdecff6c@ec2-35-168-54-239.compute-1.amazonaws.com:5432/d4k79366nf75pv'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
# from app import db
# db.create_all()

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

class Feedback(db.Model):
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key=True)
    customer = db.Column(db.String(200), unique=True)
    email = db.Column(db.String(200))
    dealer = db.Column(db.String(200))
    rating = db.Column(db.Integer)
    customer = db.Column(db.Text())

    def __init__(self, customer, email, dealer, rating, comments):
        self.customer = customer
        self.email = email
        self.dealer = dealer 
        self.rating = rating
        self.comments = comments
        

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        customer = request.form['customer']
        email = request.form['email']
        dealer = request.form['dealer']
        rating = request.form['rating']
        comments = request.form['comments']
        #print(customer, dealer, rating, comments)
        if customer == '' or dealer == '' or email == '':
            return render_template('index.html', message='Please enter required fields!!!')

        if db.session.query(Feedback).filter(Feedback.customer == customer).count() == 0: # means customer does not exist
            data = Feedback(customer, email, dealer, rating, comments)
            db.session.add(data)
            db.session.commit() # Adds customer to the database
            send_mail(customer, email, dealer, rating, comments)

            return render_template('success.html')
        return render_template('index.html', message='You have already submitted feedback!!!')



if __name__ == '__main__':
    manager.run()