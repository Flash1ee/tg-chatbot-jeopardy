
class PostgresAccessor:
    def __init__(self) -> None:
        from app.game.models import User, UserSession, Session, Round, RoundQuestion, Question, Theme, ThemeRound


        self.user = User
        self.session = Session

        self.user_session = UserSession
        self.round = Round
        self.round_question = RoundQuestion
        self.question = Question
        self.Theme = Theme
        self.ThemeRound = ThemeRound
