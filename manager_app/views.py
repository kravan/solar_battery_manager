from flask import Flask, render_template, request, session, redirect, url_for
from manager_app.forms import RegistrationForm, SigninForm
from manager_app.models import db, User

app = Flask(__name__)
app.config.from_object(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///power_manager_db'
app.debug = True
app.secret_key = 'development key'

db.app = app
db.init_app(app)
db.create_all()


# creating default user if no user in DB
is_user_in_db = db.session.query(User).first()
if is_user_in_db is None:
    try:
        new_user = User(
            'adminFirst',
            'adminLast',
            'admin',
            'admin',
            is_admin=True
        )
        db.session.add(new_user)
        db.session.commit()
    except Exception as e:
        pass


@app.route('/')
def index():
    try:
        if 'username' in session:
            user = User.query.filter(User.username == session.get('username')).first()
            return render_template('index.html', request_user=user)
        else:
            return redirect('/signin')
    except Exception as e:
        return "Error - " + str(e)


@app.route('/signin', methods=['GET', 'POST'])
def sign_in():
    try:
        form = SigninForm()
        if request.method == 'POST':
            if not form.validate():
                return render_template('signin.html', form=form)
            else:
                session['username'] = form.username.data
            return redirect('/')
        elif request.method == 'GET':
            return render_template('signin.html', form=form)
        return render_template('signin.html', form=form)
    except Exception as e:
        return "Error - " + str(e)


@app.route('/signout')
def sign_out():
    try:
        if 'username' in session:
            session.pop('username', None)
        return redirect(url_for('sign_in'))
    except Exception as e:
        return "Error - " + str(e)


@app.route('/users', methods=['GET', 'POST'])
def users():
    try:
        user = User.query.filter(User.username == session.get('username')).first()
        form = RegistrationForm()
        if request.method == 'POST':
            if not form.validate():
                return render_template('users.html', form=form)
            else:
                new_user = User(
                    form.first_name.data,
                    form.last_name.data,
                    form.username.data,
                    form.password.data,
                    form.is_admin.data,
                )
                db.session.add(new_user)
                db.session.commit()
                return redirect('/')
        return render_template('users.html', form=form, request_user=user)
    except Exception as e:
        return "Error - " + str(e)

if __name__ == '__main__':
    app.run()
