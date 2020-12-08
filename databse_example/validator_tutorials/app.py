from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField 
from wtforms.validators import DataRequired, Length, ValidationError

app = Flask(__name__)
app.config['SECRET_KEY']='Yolo' 

class UserCheck:
    def __init__(self, banned, message=None):
        self.banned = banned
        if not message:
            message = 'Please choose another username'
        self.message = message

    def __call__(self, form, field):
    # Here we define the method that is ran when the class is called. If the data in our field is in the list of words then raise a ValidationError object with a message.
        if field.data.lower() in (word.lower() for word in self.banned):
            raise ValidationError(self.message)

class myForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(),
        # We call our custom validator here, and pass through a message to override the default one. We pass through the list of banned usernames as a list.
        UserCheck(message="Name unavailable",banned = ['root','admin','sys']),
        Length(min=2,max=15)
        ])
    submit = SubmitField('Sign up')
    def validate_username(self, username):
        un=str(username.data)
        if not un.isalnum():
            raise ValidationError("Invalid username, please choose another")

@app.route('/', methods=['GET','POST'])
def postName():
    form = myForm()
    if form.validate_on_submit():
        username = form.username.data
        return render_template('home.html', form = form, username=username)
    else:
        return render_template('home.html', form = form, username="")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
