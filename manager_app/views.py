from flask import Flask, render_template
from manager_app.forms import RegistrationForm

app = Flask(__name__)
app.secret_key = 'development key'

@app.route('/')
def index():
    try:
        return render_template('index.html')
    except Exception as e:
        return "Error - " + str(e)


@app.route('/signin')
def sign_in():
    try:
        return render_template('signin.html')
    except Exception as e:
        return "Error - " + str(e)


@app.route('/users')
def users():
    try:
        form = RegistrationForm()
        return render_template('users.html', form=form)
    except Exception as e:
        return "Error - " + str(e)

if __name__ == '__main__':
    app.run()
