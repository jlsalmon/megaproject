from flask import render_template, flash, redirect, session, url_for, g, request
from flask.ext.login import login_user, current_user, login_required, logout_user
from megaproject import app, lm, oid, db
from forms import LoginForm, CreateProjectForm

from models import User, ROLE_USER


@app.route('/')
@app.route('/index')
@login_required
def index():
    user = g.user
    return render_template('index.html', title='Index', user=user)


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.before_request
def before_request():
    g.user = current_user


@app.route('/login', methods=['GET', 'POST'])
@oid.loginhandler
def login():
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        session['remember_me'] = form.remember_me.data
        return oid.try_login(form.openid.data, ask_for=['nickname', 'email'])
    return render_template('login.html',
                           title='Sign In',
                           form=form,
                           providers=app.config['OPENID_PROVIDERS'])


@oid.after_login
def after_login(resp):
    if resp.email is None or resp.email == "":
        flash('Invalid login. Please try again.')
        redirect(url_for('login'))
    user = User.query.filter_by(email=resp.email).first()
    if user is None:
        nickname = resp.nickname
        if nickname is None or nickname == "":
            nickname = resp.email.split('@')[0]
        user = User(nickname=nickname, email=resp.email, role=ROLE_USER)
        db.session.add(user)
        db.session.commit()
    remember_me = False
    if 'remember_me' in session:
        remember_me = session['remember_me']
        session.pop('remember_me', None)
    login_user(user, remember=remember_me)
    return redirect(request.args.get('next') or url_for('index'))


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/create-project', methods=['GET', 'POST'])
@login_required
def create_project():
    user = g.user
    form = CreateProjectForm()

    if form.validate_on_submit():
        return 'ok'

    return render_template('create_project.html', title='Create Project', user=user, form=form)


