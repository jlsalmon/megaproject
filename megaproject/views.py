from datetime import datetime
from flask import render_template, flash, redirect, session, url_for, g, request, jsonify, json
from flask.ext.login import login_user, current_user, login_required, logout_user
from megaproject import app, lm, oid, db
from forms import LoginForm, CreateProjectForm, CreateTaskForm

from models import User, ROLE_USER, Project, Task


@app.route('/')
@app.route('/index')
@login_required
def index():
    flash("test flash")
    user = g.user
    projects = Project.query.all()
    meta = db.metadata.tables.keys()

    form = CreateTaskForm()

    return render_template('index.html', title='Index', user=user, projects=projects, meta=meta, form=form)


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
        for project in Project.query.all():
            if project.name == form.name.data:
                flash('project already exists')
                return redirect(url_for('create_project'))
        app.logger.debug('form.validate_on_submit')
        project = Project(name=form.name.data,
                          start_date=form.start_date.data,
                          end_date=form.end_date.data,
                          info=form.info.data)
        print 'team: ' + form.team.data
        db.session.add(project)
        db.session.commit()
        flash('created project %s' % form.name.data)
        return redirect(url_for('index'))

    return render_template('create_project.html', title='Create Project', user=user, form=form)


@app.route('/create-task', methods=['POST'])
@login_required
def create_task():
    user = g.user
    form = CreateTaskForm()

    print 'form:', request.form

    if form.validate_on_submit():
        print 'ok'
        # Check the task doesn't already exist
        task = Task(name=form.name.data,
                    start_date=form.start_date.data,
                    end_date=form.end_date.data,
                    info=form.info.data)
        db.session.add(task)
        db.session.commit()
        flash('created task %s' % form.name.data)
        return redirect(url_for('index'))

    return render_template('index.html', title='Index', user=user, form=form)


@app.route('/overview', methods=['GET', 'POST'])
@login_required
def overview():
    return render_template('views/calendar.html')


@app.route('/events', methods=['GET', 'POST'])
@login_required
def events():
    event1 = {'title': 'Task 1', 'start': '2013-05-05 12:30:00',
              'end': '%s' % datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'color': '#ddd'}
    event2 = {'title': 'Task 2', 'start': '2013-05-06 12:30:00',
              'end': '%s' % datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'color': '#eee'}

    events = [event1, event2]

    for event in Task.query.all():
        ev = event.__dict__
        del ev['_sa_instance_state']
        ev['title'] = ev['name']
        ev['start'] = ev['start_date'].strftime('%Y-%m-%d')
        del ev['start_date']
        ev['end'] = ev['end_date'].strftime('%Y-%m-%d')
        del ev['end_date']
        events.append(ev)
        print 'events: ', events

    return json.dumps(events)


@app.route('/todo', methods=['GET', 'POST'])
@login_required
def todo():
    return "todo"


@app.route('/team', methods=['GET', 'POST'])
@login_required
def team():
    return "team"


@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    return "settings"


@app.route('/typeahead', methods=['GET', 'POST'])
@login_required
def typeahead():
    # users = User.query.all()
    # usernames = list()
    #
    # for user in users:
    #     usernames.append()

    response = jsonify(options=[user.nickname for user in User.query.all()])
    return response


@app.route('/task-overview', methods=['GET', 'POST'])
@login_required
def task_overview():
    print 'lol ', request.form
    return render_template('views/task_overview.html', task=request.form)
