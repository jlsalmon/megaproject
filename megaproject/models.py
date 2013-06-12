from flask.ext.security import RoleMixin, UserMixin
from twisted.python.hashlib import md5
from megaproject import db, Base


class Project(db.Model):
    __tablename__ = 'project'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), index=True)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    info = db.Column(db.String(256))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    tasks = db.relationship('Task')

    def __repr__(self):
        return '<Project %d %s owner %s>' % (self.id, self.name, self.owner_id)


class Task(db.Model):
    __tablename__ = 'task'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), index=True)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    info = db.Column(db.String(256))
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    parent_task = db.Column(db.Integer, db.ForeignKey('task.id'))

    def __repr__(self):
        return '<Task %r>' % self.name


association_table = db.Table('UserTask', Base.metadata,
                             db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                             db.Column('task_id', db.Integer, db.ForeignKey('task.id'))
)

# Define models
roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
                       db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), index=True, unique=True)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

    def avatar(self, size):
        return 'http://www.gravatar.com/avatar/' \
               + md5(self.email).hexdigest() \
               + '?d=identicon&s=' + str(size)

    # children = db.relationship("Task",
    #                            secondary=association_table,
    #                            backref="users")

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    @staticmethod
    def make_unique_nickname(nickname):
        if User.query.filter_by(nickname=nickname).first() is None:
            return nickname
        version = 2
        while True:
            new_nickname = nickname + str(version)
            if User.query.filter_by(nickname=new_nickname).first() is None:
                break
            version += 1
        return new_nickname

    def __repr__(self):
        return '<User %r id=%d email=%s>' % (self.nickname, self.id, self.email)
