#need to install
import aiosqlite as sq
import json
import os
import config as cg
from datetime import datetime, timedelta
import random as rn
import discord as dc

# defining the base class for manipulating data.
class QuestionGD:
    def __init__(self, desc: str, 
                 difficulty: str, alternatives: list[str], 
                 correct: int, ext_alternatives: list[str]):
        self.desc = desc
        self.difficulty = difficulty
        self.alternatives = alternatives
        self.correct = correct
        self.ext_alternatives = ext_alternatives
        self.is_extra = False
        self.shuffled_alternatives = []

class User:
    def __init__(self, user: dc.User, level: int, total_xp: int, lvl_xp: int, 
                 color: dc.Color = dc.Color.light_gray()):
        self.user = user
        self.level = level
        self.total_xp = total_xp
        self.lvl_xp = lvl_xp
        self.color = color

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
                score INTEGER DEFAULT 0,
                color INTEGER DEFAULT 0
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

async def obtain_user(user_id: int) -> int:
    path = os.path.join("database", "users.db")
    async with sq.connect(path) as db:
        db.row_factory = sq.Row

        async with db.execute("SELECT * FROM users WHERE id = ?",(user_id,)) as cursor:

            row = await cursor.fetchone()
            return dict(row)

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
    new_lvl = get_level_from_xp(new_xp)
    color_id = lvl_to_color_id(new_lvl)
    async with sq.connect(path) as db:
        await db.execute(
                """
                INSERT INTO users (id, xp, level, color)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(id) DO UPDATE SET xp = excluded.xp, 
                level = excluded.level, color = excluded.color
                """,
                (user_id, new_xp, new_lvl, color_id)
            )
        await db.commit()            
        print(f"La xp del usuario={user_id} ha sido actualizada a xp={new_xp} y lvl={new_lvl} con éxito.")


async def remove_user(user_id: int):
    path = os.path.join("database", "users.db")
    async with sq.connect(path) as db:
            
        await db.execute(
            "DELETE FROM users WHERE id = ?", 
            (user_id,)
        )
            
        await db.commit()
            
        print(f"Usuario de id={user_id} se eliminó de la base de datos")

async def get_daily_question() -> QuestionGD:
    diff_list = cg.DIFF_NAMES
    weights = cg.DIFF_DAILY_WEIGHT
    diff = rn.choices(diff_list, weights=weights, k=1)[0]
    path = os.path.join("database", "questions.db")
    date_now = datetime.now()
    date_limit = datetime.now() - timedelta(days=cg.TIME_DAILY_COOLDOWN)
    async with sq.connect(path) as db:
        db.row_factory = sq.Row
        string_petition = """
            SELECT * FROM questions
            WHERE difficulty = ?
            AND (fecha_ultimo_uso IS NULL OR fecha_ultimo_uso < ?)
            ORDER BY RANDOM()
            LIMIT 1
        """
        cursor = await db.execute(string_petition, (diff, date_limit))
        question = await cursor.fetchone()

        if question is None:
            print(f"No quedan más preguntas de dificultad {diff} lanzadas hace más de {cg.DAILY_QUESTION_TIME}, pregunta diaria saltada...")
            return None
        question = dict(question)
        await db.execute(f"""
            UPDATE questions
            SET fecha_ultimo_uso = ?
            WHERE id = {question["id"]}
        """,(date_now,))
        await db.commit()
        await cursor.close()
        difficulty = question["difficulty"]
        description = question["description"]
        correct = question["correct"]
        alternatives = json.loads(question["alternatives"])
        ext_alternatives = json.loads(question["ext_alternatives"])
        question = QuestionGD(description, difficulty, alternatives, correct, ext_alternatives)
        return question

def get_level_from_xp(xp: int) -> int:
    level = 1
    while True:
        xp_need = cg.XP_FUNCTION(level + 1)
        if xp >= xp_need:
            level += 1
        else:
            break
    return level

async def lvl_up(prev_lvl: int, new_lvl: int, interaction: dc.Interaction):
    if prev_lvl == new_lvl:
        return
    username = interaction.user.display_name
    await interaction.channel.send(f"{username} ha subido de nivel! {prev_lvl} -> {new_lvl}")

async def update_level(user: User):
    new_level = get_level_from_xp(user.total_xp)
    if new_level == user.level:
        return new_level
    path = os.path.join("database", "users.db")
    user_id = user.user.id
    color_id = lvl_to_color_id(new_level)
    async with sq.connect(path) as db:
        await db.execute(
                f"""
                UPDATE users 
                SET level = ?,
                color = ?
                WHERE id = ?
                """,
                (new_level, color_id, user_id)
            )
        await db.commit()            
        print(f"El lvl del usuario={user_id} ha sido actualizada a lvl={new_level} con éxito.")
        return new_level

# The whole process of updating xp and level of a player
async def update_player(interaction: dc.Interaction, added_xp: int):
    user_dc = interaction.user
    user_id = user_dc.id
    await add_user_xp(user_id, added_xp)
    user_db = await obtain_user(user_id)
    xp_update = user_db["xp"]
    lvl_old = user_db["level"]
    # lvl_xp parameter doesn't matter here
    user = User(user=user_dc, level=lvl_old, total_xp=xp_update, lvl_xp=0)
    # important functions
    lvl_new = await update_level(user)
    await lvl_up(lvl_old, lvl_new, interaction)
    print(f"Actualización de xp y lvl del usuario {user_id} realizada")

def lvl_to_color_id(lvl: int) -> int:
    if lvl < 10:
        id = 0
    elif lvl < 25:
        id = 1
    elif lvl >= 250:
        id = 10
    else:
        id = (lvl // 25) + 1
    return id

def color_id_to_color(id: int) -> dc.Color:
    colors = [dc.Color.light_gray(), dc.Color.green(), dc.Color.blue(), dc.Color.purple(),
              dc.Color.gold(), dc.Color.dark_red(), dc.Color.dark_grey(), dc.Color.dark_green(),
              dc.Color.dark_blue(), dc.Color.magenta(), dc.Color.yellow()]
    return colors[id]
