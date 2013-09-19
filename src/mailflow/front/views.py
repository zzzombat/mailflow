from flask import render_template, redirect, session, url_for

from mailflow.front import app, db, models, lm
from forms import LoginForm, RegistrationForm

from flask.ext.login import login_user, logout_user, current_user, login_required

lm.login_view = 'index'


@app.route('/', methods=['GET', 'POST'])
def index():
    if current_user.is_authenticated():
        return redirect(url_for('dashboard'))

    form = LoginForm()
    if form.validate_on_submit():
        user = models.User.query.filter_by(email=form.email.data).first()
        session['remember_me'] = form.remember_me.data
        login_user(user, remember=session['remember_me'])
        return redirect(url_for('dashboard'))
    return render_template('index.html', form=form)


@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')


@app.route('/reg', methods=['GET', 'POST'])
def reg():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = models.User(email=form.email.data, password=form.password.data, active=True)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('dashboard'))
    return render_template('reg.html', form=form)


@lm.user_loader
def load_user(cookie):
    try:
        user_id = int(cookie)
    except ValueError:
        return None
    return models.User.query.get(user_id)


@app.context_processor
def inject_user():
    return dict(user=current_user)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for("index"))
