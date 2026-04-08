from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField, DateField, StringField, SelectField
from wtforms.validators import  DataRequired

class Finance_Data(FlaskForm):
    date = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()])
    amount = IntegerField('Amount', validators=[DataRequired()])
    category = SelectField(
        'Category',
    choices=[
        ('rent', 'Rent'),
        ('food', 'Food'),
        ('health', 'Health'),
        ('luxury', 'Luxury'),
        ('travel', 'Travel'),
        ('extra', 'Extra')
    ],
    validators=[DataRequired()]
)
    remarks = StringField('Remarks', validators=[DataRequired()])
    submit = SubmitField('Submit')
