from typing import List

import json
from sqlalchemy.sql.expression import update
from app.game.models import Answer, Session, User
from bot.helpers.gameHelper import GameHelper, GameState
from app.store.database.models import db
import asyncio
import random

from aiohttp import web


class PostgresAccessor:
    def __init__(self) -> None:
        from app.game import models

        self.models = models
        self.db = None

    async def create_session(self) -> None:
        from app.store.database.models import db
        await db.set_bind(
            "postgresql://postgres:1234@localhost/postgres"
        )
        self.db = db

    async def stop_session(self) -> None:
        if self.db is not None:
            await self.db.pop_bind().close()


async def do():

    random.seed(None)

    pg = PostgresAccessor()
    await pg.create_session()

    await pg.db.gino.create_all()

    game = GameHelper(chat_id=-135, db=pg.db)
    await game.update_data()

    state = await game.GetState() 
    print (state)
    if state == GameState.not_active:
        print("no_active -> startt")
        await game.createSession()
    
    round = await game.GetRound()

    if not round:
        print("no round -> creating")
        round = await game.startRound()
        
    themes = await game.GetThemes()
    print('id=', round.id, 'num=', round.number, "status=", round.status)
    print(list(map(lambda x: x.title, themes)))

    for theme in themes:
        for i in range(1, 6):
            r = random.random() > 0.6
            if r:
                question, rq = await game.createRoundQuestion(score=i, theme_id=theme.id)
                print(question.content, question.correct_answer)

                print(await game.GetState())
                question, rq = await game.getQuestion()
                print(rq.id, await game.GetState())

                answer = await game.answerQuestion(user_id=10001, answer="otvet 1")
                print(answer.status, await game.GetState())

                answer = await game.answerQuestion(user_id=10002, answer="otvet 2")
                print(answer.status, await game.GetState())

                user_c = random.randint(10001, 10005)
                answer = await game.answerQuestion(user_id=user_c, answer=question.correct_answer)
                print("user_c=", user_c, answer.status, await game.GetState())

                print("Choosing=", await game.choosingUser())

    questions = await game.getRoundQuestions()
    for question in questions:
        print(question.id, question.theme_id, question.content)

    print(await game.table())
    # print(json.dumps(await game.table()))
    await game.startRound()
    await pg.stop_session()

asyncio.get_event_loop().run_until_complete(do())
