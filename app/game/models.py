from app.store.database.models import db

class User(db.Model):
    __tablename__ = "user"
    user_id = db.Column(db.Integer, primary_key = True, unique = True)

class UserSession(db.Model):
    __tablename__ = "user_session"
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    session_id = db.Column(db.Integer, db.ForeignKey('session.id'))
    score = db.Column(db.Integer)

class Session(db.Model):
    __tablename__ = "session"
    id = db.Column(db.Integer, primary_key = True)
    chat_id = db.Column(db.Integer)
    status = db.Column(db.Integer)

class Round(db.Model):
    __tablename__ = "round"
    id = db.Column(db.Integer, primary_key = True, unique = True)
    session_id = db.Column(db.Integer, db.ForeignKey('session.id'))
    number = db.Column(db.Integer)
    status = db.Column(db.Integer)

class RoundQuestion(db.Model):
    __tablename__ = "round_question"
    id = db.Column(db.Integer, primary_key = True, unique = True)
    status = db.Column(db.Integer)
    round_id = db.Column(db.Integer, db.ForeignKey('round.id'))
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    created_at = db.Column(db.DateTime) 

class Question(db.Model):
    __tablename__ = "question"
    id = db.Column(db.Integer, primary_key = True, unique = True)
    content = db.Column(db.String)
    correct_answer = db.Column(db.String)
    score = db.Column(db.Integer)
    theme_id = db.Column(db.Integer, db.ForeignKey('theme.id'))

class Theme(db.Model):
    __tablename__ = "theme"
    id = db.Column(db.Integer, primary_key = True, unique = True)
    title = db.Column(db.String)

class ThemeRound(db.Model):
    __tablename__ = "theme_round"
    theme_id = db.Column(db.Integer, db.ForeignKey('theme.id'))
    round_id = db.Column(db.Integer, db.ForeignKey('round.id'))


    



    










