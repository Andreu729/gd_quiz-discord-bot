# need to install
from discord import ui
import discord as dc
import config as cg

class QuestionButton(ui.Button):

    def __init__(self, label: str, correct: bool):
        super().__init__(label=label, style=dc.ButtonStyle.secondary)
        self.correct = correct
    
    async def callback(self, interaction: dc.Interaction):
        response = interaction.response
        if self.correct:
            await response.send_message("Respuesta Correcta :D", ephemeral=True)
        else:
            await response.send_message("Respuesta incorrecta :(", ephemeral=True)

class QuestionExample(ui.View):

    def __init__(self):
        super().__init__(timeout=None)

        self.add_item(QuestionButton(label="Spawn Trigger", correct=False))
        self.add_item(QuestionButton(label="Touch Trigger", correct=False))
        self.add_item(QuestionButton(label="On Restart Trigger", correct=True))
        self.add_item(QuestionButton(label="Random Trigger", correct=False))

def question_embed(desc: str, difficulty: str, daily: bool=True, number: int=0) -> dc.Embed:
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
