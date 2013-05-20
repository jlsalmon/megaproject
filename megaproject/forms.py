from flask.ext.wtf import Form, TextField, BooleanField
from flask.ext.wtf import Required


class LoginForm(Form):
    openid = TextField('openid', validators=[Required()])
    remember_me = BooleanField('remember_me', default=False)


class CreateProjectForm(Form):
    project_name = TextField('project_name', validators=[Required()])
    start_date = TextField('start_date', validators=[Required()])
    end_date = TextField('end_date', validators=[Required()])
    info = TextField('info')
    team = TextField('team', validators=[Required()])
