# need to install
from discord import ui
import discord as dc
import config as cg
from gd_data import QuestionGD, User, diff_to_xp, update_player
from random import shuffle
import aiosqlite as sq
import os

class QuestionButton(ui.Button):

    def __init__(self, label: str, correct: bool, question: QuestionGD):
        super().__init__(label=label, style=dc.ButtonStyle.secondary)
        self.correct = correct
        self.question = question
    
    async def callback(self, interaction: dc.Interaction):
        response = interaction.response
        if self.correct:
            xp = diff_to_xp(self.question)
            await response.send_message(f"Respuesta Correcta :D | xp Añadida: {xp}", ephemeral=True)
            await update_player(interaction, xp)
        else:
            await response.send_message("Respuesta incorrecta :(", ephemeral=True)

class QuestionButtonsView(ui.View):

    def __init__(self, question: QuestionGD, extra: bool=False):
        super().__init__(timeout=None)
        correct_id = question.correct
        shuffled = question.shuffled_alternatives
        len_shuffled = len(shuffled)
        correct = question.alternatives[correct_id]
        button_list = [QuestionButton(label=chr(65 + i), correct=shuffled[i]==correct, question=question) for i in range(len_shuffled)]
        self.answered_users = set()
        self.button_list = button_list

        for button in button_list:
            self.add_item(button)

    async def interaction_check(self, interaction: dc.Interaction):
        user_id = interaction.user.id
        if user_id in self.answered_users:
            await interaction.response.send_message("No puedes volver a responder esta pregunta!", ephemeral=True, delete_after=10)
            return False
        else:
            self.answered_users.add(user_id)
            return True

async def disable_question(message: dc.Message, view: QuestionButtonsView):
    buttons = view.button_list
    for button in buttons:
        button.disabled = True
    await message.edit(view=view)

def question_embed(question: QuestionGD, daily: bool=True, number: int=0) -> dc.Embed:
    desc = question.desc + ".\n\n"
    difficulty = question.difficulty
    question_amount = len(question.alternatives)
    total_alternatives = question.alternatives.copy()
    if question.is_extra is True:
        question_amount += len(question.ext_alternatives)
        total_alternatives += question.ext_alternatives
    
    # Randomize alternatives order
    shuffle(total_alternatives)
    question.shuffled_alternatives = total_alternatives
    # This part create the alternatives description
    for i in range(question_amount):
        desc += f"**{chr(65 + i)}**" + ": " + total_alternatives[i] + ".\n"
    if daily:
        title = "Pregunta Diaria"
    else:
        title = f"Pregunta {number}/{cg.TOTAL_QUESTIONS}"

    if difficulty == "Muy fácil":
        color = dc.Color.blue()
    elif difficulty == "Fácil":
        color = dc.Color.green()
    elif difficulty == "Intermedia":
        color = dc.Color.yellow()
    elif difficulty == "Difícil":
        color = dc.Color.red()
    elif difficulty == "Imposible":
        color = dc.Color.purple()
    else:
        color = dc.Color.light_gray()
    embed_question = dc.Embed(title=title,
                                  description=desc,
                                  color=color)
        
    embed_question.add_field(name="Dificultad", value=difficulty, inline=True)
    # Se debe cambiar el parámetro de tiempo según la config.
    if daily:
        embed_question.add_field(name="Límite de tiempo", value="14:59 hrs (Chile)", inline=True)
    return embed_question

def user_embed(user: User) -> dc.Embed:
    title = user.user.display_name
    desc = f"Nivel: {user.level}\n"
    desc += f"XP actual: {user.lvl_xp}\n"
    xp_new = cg.XP_FUNCTION(user.level + 1)
    xp_need =  xp_new - (user.total_xp - user.lvl_xp)
    desc += f"XP siguiente nivel: {xp_need}\n"
    desc += f"XP acumulada: {user.total_xp}"
    color = user.color
    embed_user = dc.Embed(title=title, description=desc, color=color)
    embed_user.set_thumbnail(url=user.user.display_avatar.url)
    progress = min(user.lvl_xp / xp_need, 1.0)
    filled_blocks = int(cg.XP_BAR_LENGTH * progress)
    empty_blocks = cg.XP_BAR_LENGTH - filled_blocks

    exp_bar = ("🟦" * filled_blocks) + ("⬛" * empty_blocks)
    embed_user.add_field(name="Progreso", value=exp_bar, inline=False)
    return embed_user

# Clase hecha con IA
class QuestionsPagination(dc.ui.View):
    def __init__(self):
        super().__init__(timeout=180) # La vista se desactiva tras 3 minutos
        self.page = 1
        self.per_page = cg.OBTAIN_QUESTIONS_PAGE_LIMIT

    async def obtener_datos_pagina(self):
        saltos = (self.page - 1) * self.per_page
        path = os.path.join("database", "questions.db")
        
        async with sq.connect(path) as db:
            db.row_factory = sq.Row
            # Obtenemos las 5 preguntas de esta página
            async with db.execute("SELECT id, description, difficulty FROM questions LIMIT ? OFFSET ?", (self.per_page, saltos)) as cursor:
                filas = await cursor.fetchall()
            
            # Contamos el total para saber cuándo desactivar el botón de "Siguiente"
            async with db.execute("SELECT COUNT(id) FROM questions") as cursor:
                total_preguntas = await cursor.fetchone()
                self.total_items = total_preguntas[0]
                
        return filas

    async def construir_embed(self):
        filas = await self.obtener_datos_pagina()
        
        embed = dc.Embed(
            title="📚 Lista de preguntas", 
            color=dc.Color.teal()
        )
        
        if not filas:
            embed.description = "No hay preguntas en esta página."
        else:
            for fila in filas:
                embed.add_field(
                    name=f"ID: {fila['id']} | Dificultad: {fila['difficulty']}", 
                    value=fila['description'], 
                    inline=False
                )
                
        # Calculamos el total de páginas
        total_paginas = (self.total_items + self.per_page - 1) // self.per_page
        embed.set_footer(text=f"Página {self.page} de {total_paginas} | Total: {self.total_items} preguntas")
        
        return embed, total_paginas

    async def actualizar_botones(self, total_pages):
        # Desactiva "Anterior" si estamos en la página 1
        self.btn_anterior.disabled = self.page == 1
        # Desactiva "Siguiente" si llegamos a la última página
        self.btn_siguiente.disabled = self.page >= total_pages

    @dc.ui.button(label="◀️ Anterior", style=dc.ButtonStyle.secondary, custom_id="btn_ant", disabled=True)
    async def btn_anterior(self, interaction: dc.Interaction, button: dc.ui.Button):
        self.page -= 1
        embed, total_pages = await self.construir_embed()
        await self.actualizar_botones(total_pages)
        await interaction.response.edit_message(embed=embed, view=self)

    @dc.ui.button(label="Siguiente ▶️", style=dc.ButtonStyle.primary, custom_id="btn_sig")
    async def btn_siguiente(self, interaction: dc.Interaction, button: dc.ui.Button):
        self.page += 1
        embed, total_pages = await self.construir_embed()
        await self.actualizar_botones(total_pages)
        await interaction.response.edit_message(embed=embed, view=self)
