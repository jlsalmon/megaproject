from flask.ext.wtf import Form, TextField, BooleanField, DateField
from flask.ext.wtf import Required


class LoginForm(Form):
    openid = TextField('openid', validators=[Required()])
    remember_me = BooleanField('remember_me', default=False)


class CreateTaskForm(Form):
    name = TextField('Task Name', validators=[Required()])
    info = TextField('Info')
    start_date = DateField('Start Date', validators=[Required()], format='%d-%m-%Y')
    end_date = DateField('End Date', validators=[Required()], format='%d-%m-%Y')
    team = TextField('Team', validators=[Required()])


class CreateProjectForm(CreateTaskForm):
    name = TextField('Project Name', validators=[Required()])


