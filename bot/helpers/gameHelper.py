from typing import List, Tuple
import gino
import enum

import app.game.models as m
from sqlalchemy import func


class GameState(enum.Enum):
    not_active = 0
    active = 1
    wait_question = 2
    wait_answer = 3
    error = 4


class GameHelper:

    #  Config
    themes_count = 3
    question_scores = range(1, 6)

    # init values
    chat_id: int = 0
    db: gino = None

    # game models
    session: m.Session = None
    round: m.Round = None
    rq: m.RoundQuestion = None
    q: m.Question = None

    themes: List[m.Theme] = None
    round_questions: List[m.RoundQuestion] = None

    last_rq: m.RoundQuestion = None
    last_answer: m.Answer = None

    loaded_all = False

    def __init__(self, chat_id: int, db: gino) -> None:
        self.chat_id = chat_id
        self.db = db

    async def update_data(self):
        self.loaded_all = True
        self.session, self.round, self.rq, self.q, self.round_questions = None, None, None, None, None
        await self.GetSession()
        if not self.session:
            return
        await self.GetRound()
        if not self.session:
            return

        await self.getRoundQuestion()
        if not self.rq:
            return

        await self.getQuestion()
        if not self.question:
            return

    async def GetState(self) -> GameState:
        if not self.loaded_all:
            await self.update_data()

        if not self.session:
            return GameState.not_active
        if not self.round:
            return GameState.error
        if self.rq and self.rq.status == m.RoundQuestionStatus.active:
            return GameState.wait_answer
        return GameState.wait_question

    async def GetSession(self) -> m.Session:
        self.session = (
            await m.Session.query.where(m.Session.chat_id == self.chat_id)
            .where(m.Session.status == m.SessionStatus.active)
            .gino.first()
        )
        return self.session

    async def GetRound(self) -> m.Round:
        if not self.session:
            await self.GetSession()

        self.round = (
            await m.Round.query.where(m.Round.session_id == self.session.id)
            .where(m.Round.status == m.RoundStatus.active)
            .gino.first()
        )
        return self.round

    async def getRoundQuestion(self) -> m.RoundQuestion:
        if not self.round:
            self.GetRound()

        self.rq = (
            await m.RoundQuestion.query.where(m.RoundQuestion.round_id == self.round.id)
            .where(m.RoundQuestion.status == m.RoundQuestionStatus.active)
            .gino.first()
        )
        return self.rq

    async def getQuestion(self) -> Tuple[m.Question, m.RoundQuestion]:
        if not self.rq:
            await self.getRoundQuestion()
        self.question = await m.Question.query.where(m.Question.id == self.rq.question_id).gino.first()
        return (self.question, self.rq)

    async def GetThemes(self) -> List[m.Theme]:
        if not self.round:
            self.round = await self.GetRound()

        self.themes = (
            await m.Theme.query.select_from(
                m.Theme.join(m.ThemeRound, m.Theme.id == m.ThemeRound.theme_id)
            )
            .where(m.ThemeRound.round_id == self.round.id)
            .gino.all()
        )

        return self.themes

    async def GetRandomThemes(self) -> List[m.Theme]:
        return (
            await m.Theme.query.order_by(func.random())
            .limit(self.themes_count)
            .gino.all()
        )

    async def GetRandomQuestion(self, score: int, theme_id: int) -> m.Question:
        return (
            await m.Question.query.where(m.Question.theme_id == theme_id)
            .where(m.Question.score == score)
            .order_by(func.random())
            .gino.first()
        )

    async def SetRandomThemes(self) -> List[m.Theme]:
        if not self.round:
            await self.GetRound()
        themes = await self.GetRandomThemes()
        for theme in themes:
            await m.ThemeRound.create(
                round_id=self.round.id,
                theme_id=theme.id,
            )
        return themes

    async def startRound(self) -> m.Round:
        if not self.session:
            await self.GetSession()
        if not self.round:
            await self.GetRound()

        number = 1
        if self.round:
            number += self.round.number
            await self.round.update(
                status=m.RoundStatus.finished,
            ).apply()

        return await self.createRound(number)

    async def createRound(self, number) -> m.Round:
        if not self.session:
            await self.GetSession()

        self.round = await m.Round.create(
            session_id=self.session.id,
            number=number,
            status=m.RoundStatus.active,
        )
        await self.SetRandomThemes()
        return self.round

    async def createRoundQuestion(
        self, score: int, theme_id: int
    ) -> Tuple[m.Question, m.RoundQuestion]:
        if not self.round:
            await self.GetRound()

        self.question = await self.GetRandomQuestion(score=score, theme_id=theme_id)
        self.rq = await m.RoundQuestion.create(
            question_id=self.question.id,
            round_id=self.round.id,
            status=m.RoundQuestionStatus.active,
        )

        return self.question, self.rq

    async def check_answer(self, answer: str, corect: str) -> m.AnswerStatus:
        # @todo: use mystem3
        if " ".join(answer.lower().split()) == " ".join(
            corect.lower().split()
        ):
            return m.AnswerStatus.correct
        return m.AnswerStatus.incorrect

    async def answerQuestion(
            self, answer: str, user_id: int) -> m.Answer:
        if not self.question:
            await self.getQuestion()

        is_correct = await self.check_answer(answer, self.question.correct_answer)

        self.last_answer = await m.Answer.create(
            status=is_correct,
            rq_id=self.rq.id,
            user_id=user_id,
        )

        if is_correct == is_correct.correct:
            await self.rq.update(status=m.RoundQuestionStatus.answered).apply()
            self.last_rq  = self.rq
            self.rq = None
            # @todo: add score
        return self.last_answer

    async def createSession(self) -> m.Session:
        self.session = await m.Session.create(
            chat_id=self.chat_id,
            status=m.SessionStatus.active
        )
        return self.session

    async def getRoundQuestions(self) -> List[m.Question]:
        if not self.round:
            await self.GetRound()

        self.round_questions = (
            await m.Question.query.select_from(
                m.Question.join(
                    m.RoundQuestion,
                    m.RoundQuestion.question_id == m.Question.id)
            )
            .where(m.RoundQuestion.round_id == self.round.id)
            .where(m.RoundQuestion.status == m.RoundQuestionStatus.answered)
            .gino.all()
        )

        return self.round_questions

    async def table(self, round: m.Round = None):
        if not round:
            await self.GetRound()

        await self.GetThemes()
        await self.getRoundQuestions()

        table = dict()

        for theme in self.themes:
            table[theme.id] = {
                "title": theme.title,
                "id": theme.id,
                "answers": dict()
            }
            for score in self.question_scores:
                table[theme.id]["answers"][score] = False
            for question in self.round_questions:
                score = question.score
                table[theme.id]["answers"][score] = True

        return table

    async def getLastQuestion(self) -> m.Question:
        if self.last_rq:
            return self.last_rq
        if not self.round:
            await self.GetRound()

        self.last_rq = (
            await m.RoundQuestion.query
            .where(m.RoundQuestion.round_id == self.round.id)
            .order_by(m.RoundQuestion.id.desc())
            .gino.first()
        )
        return self.last_rq

    async def getLastAnswer(self) -> m.Question:
        if self.last_answer:
            return self.last_answer

        await self.getLastQuestion()

        self.last_answer = (
            await m.Answer.query.where(m.Answer.rq_id == self.last_rq.id)
            .order_by(m.Answer.id.desc())
            .gino.first()
        )

        return self.last_answer

    async def choosingUser(self) -> int:
        if not self.last_rq:
            await self.getLastQuestion()
        if not self.last_rq:
            #  @todo choose random user
            return None
        if self.last_rq.status == m.RoundQuestionStatus.answered:
            if not self.last_answer:
                await self.getLastAnswer()
            return self.last_answer.user_id
        else:
            #  @todo choose with lowerest rating
            return None
    