from discord import ui
import discord as dc
import config as cg

class QuestionButton(ui.Button):

    def __init__(self, label: str, correct: bool, row: int):
        super().__init__(label=label, style=dc.ButtonStyle.secondary, row=row)
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

        

        self.add_item(QuestionButton(label="Bli", correct=False, row=0))
        self.add_item(QuestionButton(label="Michigun", correct=False, row=1))
        self.add_item(QuestionButton(label="npesta", correct=False, row=2))
        self.add_item(QuestionButton(label="Zobros", correct=True, row=3))

def question_embed(desc: str, difficulty: str, daily: bool=True, number: int=0) -> dc.Embed:
    if daily:
        title = "Pregunta Diaria"
    else:
        title = f"Pregunta {number}/{cg.TOTAL_QUESTIONS}"

    embed_question = dc.Embed(title=title,
                                  description=desc,
                                  color=dc.Color.red())
        
    embed_question.add_field(name="Dificultad", value=difficulty, inline=True)
    # Se debe cambiar el parámetro de tiempo según la config.
    if daily:
        embed_question.add_field(name="Límite de tiempo", value="14:59 hrs (Chile)", inline=True)
    return embed_question
