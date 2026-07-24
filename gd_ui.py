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
        shuffled = question.shuffled_alternatives
        len_shuffled = len(shuffled)
        correct = question.alternatives[correct_id]
        #alt_len = len(question.alternatives)
        button_list = [QuestionButton(label=chr(65 + i), correct=shuffled[i]==correct) for i in range(len_shuffled)]
        #if extra is True:
        #    ext_len = len(question.ext_alternatives)
        #    button_list += [QuestionButton(label=chr(65 + i + alt_len), correct=False) for i in range(ext_len)]
        
        #shuffle(button_list)
        for button in button_list:
            self.add_item(button)

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
