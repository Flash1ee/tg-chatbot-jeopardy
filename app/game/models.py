from app.store.database.models import db
import enum
import datetime


class User(db.Model):
    __tablename__ = "user"
    user_id = db.Column(db.Integer, primary_key=True)


class UserSession(db.Model):
    __tablename__ = "user_session"
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"))
    session_id = db.Column(db.Integer, db.ForeignKey("session.id"))
    score = db.Column(db.Integer)


class SessionStatus(enum.Enum):
    active = 0
    finished = 1


class Session(db.Model):
    __tablename__ = "session"
    id = db.Column(db.Integer, primary_key=True)
    chat_id = db.Column(db.Integer)
    status = db.Column(
        db.Enum(SessionStatus),
        nullable=False,
        default=SessionStatus.active,
    )


class RoundStatus(enum.Enum):
    active = 0
    finished = 1


class Round(db.Model):
    __tablename__ = "round"
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey("session.id"))
    number = db.Column(db.Integer)
    status = db.Column(
        db.Enum(RoundStatus),
        nullable=False,
        default=RoundStatus.active,
    )


class RoundQuestionStatus(enum.Enum):
    active = 0
    answered = 1
    failed = 2
    timeout = 3


class RoundQuestion(db.Model):
    __tablename__ = "round_question"
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(
        db.Enum(RoundQuestionStatus),
        nullable=False,
        default=RoundQuestionStatus.active,
    )
    round_id = db.Column(db.Integer, db.ForeignKey("round.id"))
    question_id = db.Column(db.Integer, db.ForeignKey("question.id"))
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)


class AnswerStatus(enum.Enum):
    correct = 0
    incorrect = 1


class Answer(db.Model):
    __tablename__ = "answer"
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(
        db.Enum(AnswerStatus),
        nullable=False,
        default=AnswerStatus.correct,
    )
    rq_id = db.Column(db.Integer, db.ForeignKey(RoundQuestion.id))
    user_id = db.Column(db.Integer, db.ForeignKey(User.user_id))
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)


class Question(db.Model):
    __tablename__ = "question"
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String)
    correct_answer = db.Column(db.String)
    score = db.Column(db.Integer)
    theme_id = db.Column(db.Integer, db.ForeignKey("theme.id"))


class Theme(db.Model):
    __tablename__ = "theme"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)


class ThemeRound(db.Model):
    __tablename__ = "theme_round"
    theme_id = db.Column(db.Integer, db.ForeignKey("theme.id"))
    round_id = db.Column(db.Integer, db.ForeignKey("round.id"))
