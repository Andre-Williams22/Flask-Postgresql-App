from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# When we switch to Heroku we'll have a totally different database
ENV = 'dev'

if ENV == 'dev':
    app.debug=True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:fcd2201@localhost/lexus'
else:
    app.debug=False
    # Our production database
    app.config['SQLALCHEMY_DATABASE_URI'] = ''
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Feedback(db.Model):
    def __init__(self, customer, dealer, rating, comments):
        self.customer = customer
        self.dealer = dealer 
        self.rating = rating
        self.comments = comments

    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key=True)
    customer = db.Column(db.String(200), unique=True)
    dealer = db.Column(db.String(200))
    rating = db.Column(db.Integer)
    customer = db.Column(db.Text())

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        customer = request.form['customer']
        dealer = request.form['dealer']
        rating = request.form['rating']
        comments = request.form['comments']
        #print(customer, dealer, rating, comments)
        if customer == '' or dealer == '':
            return render_template('index.html', message='Please enter required fields!!!')

        if db.session.query(Feedback).filter(Feedback.customer == customer).count() == 0: # means customer does not exist
            data = Feedback(customer, dealer, rating, comments)
            db.session.add(data)
            db.session.commit() # Adds customer to the database

            return render_template('success.html')
        return render_template('index.html', message='You have already submitted feedback!!!')



if __name__ == '__main__':
    app.debug=True
    app.run()