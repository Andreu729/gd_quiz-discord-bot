#need to install
import aiosqlite as sq
import json
import os
import config as cg

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
        self.is_extra = False
        self.shuffled_alternatives = []
# runs every time you start the bot.
async def configure_database():
    # Se conecta al archivo (si no existe, lo crea al instante)
    path = os.path.join("database", "questions.db")
    async with sq.connect(path) as db:
        
        # 1. QUESTIONS TABLE DEFINITION
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

async def configure_users():
    path = os.path.join("database", "users.db")
    async with sq.connect(path) as db:
            
        # 1. USERS TABLE DEFINITION
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                xp INTEGER DEFAULT 0,
                level INTEGER DEFAULT 1,
                score INTEGER DEFAULT 0
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

async def delete_question(question_id: int):
    path = os.path.join("database", "questions.db")
    async with sq.connect(path) as db:
        
        await db.execute(
            "DELETE FROM questions WHERE id = ?", 
            (question_id,)
        )
        
        await db.commit()
        
        print(f"Pregunta con ID {question_id} ha sido borrada.")


async def modify_question(question_id: int, parameter: str, new_value):
    valid_params = ["difficulty", "description", "alternatives", "correct", "ext_alternatives"]
    if not parameter in valid_params:
        print("Parametro sugerido no es válido, debes poner alguno de estos : 'difficulty', 'description', 'alternatives', 'correct', 'ext_alternatives'")
        return
    path = os.path.join("database", "questions.db")
    async with sq.connect(path) as db:

        if parameter in ("alternatives", "ext_alternatives"):
            new_value = new_value.split(",")
            new_value = [al.strip() for al in new_value]
            new_value = json.dumps(new_value)
        
        await db.execute(
            f"""
            UPDATE questions 
            SET {parameter} = ?
            WHERE id = ?
            """,
            (new_value, question_id)
        )
        
        await db.commit()
        
        print(f"La pregunta {question_id} ha sido actualizada con éxito.")
        return True

async def obtain_questions(limit: int=-1):
    path = os.path.join("database", "questions.db")
    async with sq.connect(path) as db:
        db.row_factory = sq.Row

        async with db.execute("SELECT id, description, alternatives, ext_alternatives FROM questions") as cursor:
            if limit < 0:
                rows = await cursor.fetchall()
            else:
                rows = await cursor.fetchmany(limit)

            data_list = []
            for row in rows:
                question_id = row["id"]
                description = row["description"]
                alternatives = json.loads(row["alternatives"])
                ext_alternatives = json.loads(row["ext_alternatives"])
                data_list.append({"id": question_id, "description": description})
                print(f"ID: {question_id}, | Enunciado: {description}")
                print(f"Alternativas: {alternatives} | Alternativas Carta: {ext_alternatives}")
            return data_list

async def obtain_single_question(id: int) -> QuestionGD:
    path = os.path.join("database", "questions.db")
    async with sq.connect(path) as db:
        db.row_factory = sq.Row

        async with db.execute("SELECT * FROM questions WHERE id = ?",(id,)) as cursor:

            row = await cursor.fetchone()
            row = dict(row)
            difficulty = row["difficulty"]
            description = row["description"]
            correct = row["correct"]
            alternatives = json.loads(row["alternatives"])
            ext_alternatives = json.loads(row["ext_alternatives"])
            question = QuestionGD(description, difficulty, alternatives, correct, ext_alternatives)
            print(f"obtenida la pregunta con id {id}")
            return question

# SCORE DATA MANAGEMENT
def diff_to_xp(quesion: QuestionGD) -> int:
    diff = quesion.difficulty
    if diff == "Muy Fácil":
        return cg.XP_DAILY_VERY_EASY
    if diff == "Fácil":
        return cg.XP_DAILY_EASY
    if diff == "Intermedia":
        return cg.XP_DAILY_MEDIUM
    if diff == "Difícil":
        return cg.XP_DAILY_HARD
    if diff == "Imposible":
        return cg.XP_DAILY_IMPOSSIBLE
    else:
         return 0

async def obtain_user_xp(user_id: int) -> int:
    path = os.path.join("database", "users.db")
    async with sq.connect(path) as db:
        db.row_factory = sq.Row

        async with db.execute("SELECT xp FROM users WHERE id = ?",(user_id,)) as cursor:

            row = await cursor.fetchone()
            if row is None:
                return 0
            xp = int(row[0])
            print(f"obtenida la xp {xp} del usuario: {user_id}")
            return xp

async def add_user_xp(user_id: int, xp: int):
    path = os.path.join("database", "users.db")
    async with sq.connect(path) as db:
        db.row_factory = sq.Row

        string_petition = """
            INSERT INTO users (id, xp)
            VALUES (?, ?)
            ON CONFLICT(id) DO UPDATE SET xp = xp + excluded.xp
        """
        await db.execute(string_petition, (user_id, xp))
        await db.commit()
        print(f"Usuario con id: {user_id} obtuvo un total de {xp} xp")

async def modify_user_xp(user_id: int, new_xp: int):
    path = os.path.join("database", "users.db")
    async with sq.connect(path) as db:
        await db.execute(
                f"""
                UPDATE users 
                SET xp = ?
                WHERE id = ?
                """,
                (new_xp, user_id)
            )
        await db.commit()            
        print(f"La xp del usuario={user_id} ha sido actualizada a xp={new_xp} con éxito.")


async def remove_user(user_id: int):
    path = os.path.join("database", "users.db")
    async with sq.connect(path) as db:
            
        await db.execute(
            "DELETE FROM users WHERE id = ?", 
            (user_id,)
        )
            
        await db.commit()
            
        print(f"Usuario de id={user_id} se eliminó de la base de datos")
