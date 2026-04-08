import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from forms import Finance_Data

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your_secret_key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('POSTGRES_URL', 'sqlite:///finance_data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class financeData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String, nullable=False)
    remarks = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f'<financeData {self.id}>'

@app.before_request
def create_tables():
    db.create_all()
    
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/expenses', methods=['GET', 'POST'])
def expenses():
    form = Finance_Data()
    if form.validate_on_submit():
        # Create a new finance data entry
        new_data = financeData(
            date=form.date.data,
            amount = form.amount.data,
            category = form.category.data,
            remarks = form.remarks.data
        )
        # Add the new data to the database
        db.session.add(new_data)
        db.session.commit()
        # Redirect to the dashboard
        return redirect(url_for('dashboard'))
    return render_template('expenses.html', form=form)

@app.route('/dashboard')
def dashboard():
    # Retrieve all health data from the database
    all_data = financeData.query.all()
        # Prepare data for charts
    dates = [data.date.strftime("%Y-%m-%d") for data in all_data]
    amount_data = [data.amount for data in all_data]
    category_count = {}
    for data in all_data:
        if data.category in category_count:
            category_count[data.category] += data.amount
        else:
            category_count[data.category] = data.amount

    category_labels = list(category_count.keys())
    category_values = list(category_count.values())
    remarks = [data.remarks for data in all_data]

    return render_template('dashboard.html', dates=dates, amount_data=amount_data, category_labels=category_labels,category_values=category_values, remarks=remarks)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)