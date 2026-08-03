# 🟩 Geometry Dash Trivia Bot (GD_Quiz)

A Discord bot that features a set of multiple-choice questions stored in an asynchronous database. These questions are posted to a Discord channel every day to challenge the players. It includes a leveling system, various commands, and in the future, a trivia mode similar to "Who Wants to Be a Millionaire?".

> **⚠️ Note on Language:** The source code (variables, functions, and comments) is written in **English**. However, the bot's interface, UI messages, and the default trivia database are entirely in **Spanish**.

---

## ✨ Main Features

* **Daily Questions System:** In one channel, every day a new question is printed, available for users to try answering, this system guarantees that the same question won't appear between a 20 day gap (20 day *cooldown*).
* **Level and Experience** By answering questions, the players earn xp and can potentially level up, the command `/level` allows all users to see their progress, for now there are not extra functionalities besides visual gratification.
* **Safe DataBase Architecture:** The public data (`questions.db`) contains the questions stored in your bot, and the private data (`users.db`) contains the level, experience and other info of users that have played, the second one is created automatically when running the code for the first time.
* **Customization from server** You can easily modify the data stored in the database using developer intended commands in your server (create, modify, delete questions, and modify xp/level and delete users). You can only use them on the allowed dev channels defined inside `credentials.env` and you need administrator permissions.

---

## 🛠️ Requirements And Instructions

### Requirements
For running this bot you will need to install the following:

* Python 3.10 or higher
* `discord.py` (Discord's API wrapper).
* `aiosqlite` (asynchronous SQlite)

Both libraries can be installed using pip.

### Instructions
1. After cloning the repository, first you will need to fill the parameters inside `credentials.env.example` with your corresponding tokens (you can obtain them with Discord Developer Portal and in your Discord guild/server). Once ready, change the name to `credentials.env` to make it work correctly.

2. You can also change parameters of how the bot behaves inside `config.py`. However, some configurations depends on how the questions of the database are written, so they must be changed with caution because they could break the code's functionality.

3. Then you can start the bot by running the `main.py` file inside your desired terminal (with all the requirements).

**⚠️ Important Note:** Currently, the bot is designed to support only one server at a time. Making your Discord application public could allow outside users to affect the data in both `questions.db` and `users.db`, so it is highly recommended to keep it private.