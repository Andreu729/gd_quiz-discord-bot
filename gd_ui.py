# need to install
from discord import ui
import discord as dc
import config as cg
from gd_data import QuestionGD
from random import shuffle

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

class QuestionButtonsView(ui.View):

    def __init__(self, question: QuestionGD, extra: bool=False):
        super().__init__(timeout=None)
        correct_id = question.correct
        alternatives = question.alternatives
        button_list = [QuestionButton(label=alternatives[i], correct=i==correct_id) for i in range(len(alternatives))]
        if extra is True:
            ext_alternatives = question.ext_alternatives
            button_list += [QuestionButton(label=ext_alternatives[i], correct=False) for i in range(len(ext_alternatives))]
        
        shuffle(button_list)
        for button in button_list:
            self.add_item(button)

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
