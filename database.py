import aiosqlite

DB_NAME = 'quiz_bot.db'


async def create_table():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('''CREATE TABLE IF NOT EXISTS quiz_state
                            (
                                user_id
                                INTEGER
                                PRIMARY
                                KEY,
                                question_index
                                INTEGER,
                                score
                                INTEGER
                                DEFAULT
                                0,
                                last_answers
                                TEXT
                            )''')
        await db.commit()


async def get_quiz_index(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute('SELECT question_index FROM quiz_state WHERE user_id = ?', (user_id,)) as cursor:
            result = await cursor.fetchone()
            return result[0] if result else 0


async def get_user_score(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute('SELECT score FROM quiz_state WHERE user_id = ?', (user_id,)) as cursor:
            result = await cursor.fetchone()
            return result[0] if result else 0


async def get_user_answers(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute('SELECT last_answers FROM quiz_state WHERE user_id = ?', (user_id,)) as cursor:
            result = await cursor.fetchone()
            return result[0] if result else ""


async def update_quiz_index(user_id, index, score=None, answer=None):
    async with aiosqlite.connect(DB_NAME) as db:
        current_answers = await get_user_answers(user_id)
        if answer:
            current_answers = (current_answers + f";{answer}" if current_answers else answer)

        if score is not None:
            await db.execute(
                'INSERT OR REPLACE INTO quiz_state (user_id, question_index, score, last_answers) VALUES (?, ?, ?, ?)',
                (user_id, index, score, current_answers))
        else:
            await db.execute(
                'INSERT OR REPLACE INTO quiz_state (user_id, question_index, last_answers) VALUES (?, ?, ?)',
                (user_id, index, current_answers))
        await db.commit()


async def get_statistics():
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute('SELECT user_id, score FROM quiz_state WHERE score > 0') as cursor:
            return await cursor.fetchall()