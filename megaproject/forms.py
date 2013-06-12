from flask_security.forms import ConfirmRegisterForm
from flask.ext.wtf import Form, TextField, BooleanField, DateField, TextAreaField, HiddenField, SubmitField, PasswordField
from flask.ext.wtf import Required


class LoginForm(Form):
    openid      = TextField   ('openid',
                               validators=[Required()])
    email       = TextField   ('Email',
                               validators=[Required()])
    password    = PasswordField('Password',
                               validators=[Required()])
    remember    = BooleanField('Remember Me',
                               default=False)
    next        = HiddenField ('next')
    submit      = SubmitField ('submit')


class ExtendedRegisterForm(ConfirmRegisterForm):
    first_name = TextField('First Name', [Required()])
    last_name = TextField('Last Name', [Required()])


class CreateTaskForm(Form):
    name       = TextField    ('Task Name',
                               description='Enter a unique and descriptive name for this task',
                               validators=[Required()])
    info       = TextAreaField('Description',
                               description='Enter a detailed description of this project')
    start_date = DateField    ('Start Date',
                               description='Enter the date when this project will start',
                               validators=[Required()],
                               format='%d-%m-%Y')
    end_date   = DateField    ('End Date',
                               description='Enter the date when this project will end',
                               validators=[Required()],
                               format='%d-%m-%Y')
    team       = TextField    ('Team',
                               description='Begin typing names of the people who will be involved with this project',
                               validators=[Required()])


class CreateProjectForm(CreateTaskForm):
    name       = TextField    ('Project Name',
                               description='Enter a unique and descriptive name for this project',
                               validators=[Required()])


