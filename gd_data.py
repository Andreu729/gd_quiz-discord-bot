#need to install
import aiosqlite as sq
import json
import os

# defining the base class for manipulating data.
class QuestionGD:
    def __init__(self, desc: str, 
                 difficulty: str, alternatives: list[str], 
                 correct: int, ext_alternatives: list[str]):
        self.id = -1 # this is modified just after creating a new question
        self.desc = desc
        self.difficulty = difficulty
        self.alternatives = alternatives
        self.correct = correct
        self.ext_alternatives = ext_alternatives

# runs every time you start the bot.
async def configure_database():
    # Se conecta al archivo (si no existe, lo crea al instante)
    path = os.path.join("database", "questions.db")
    async with sq.connect(path) as db:
        
        # 1. CREAR LA TABLA (Defines las columnas y sus tipos)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS questions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                difficulty TEXT,
                description TEXT,
                alternatives TEXT,
                correct INTEGER,
                ext_alternatives TEXT
            )
        """)
        await db.commit()

async def insert_question(question: QuestionGD):
        path = os.path.join("database", "questions.db")
        async with sq.connect(path) as db:
            # json formatted list
            alternatives = json.dumps(question.alternatives)
            ext_alternatives = json.dumps(question.ext_alternatives)
        
            await db.execute(
                "INSERT OR IGNORE INTO questions (difficulty, description, alternatives, correct, ext_alternatives) VALUES (?, ?, ?, ?, ?)",
                (question.difficulty, question.desc, alternatives, question.correct, ext_alternatives)
            )
            await db.commit()
