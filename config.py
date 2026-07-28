from zoneinfo import ZoneInfo
# Format: [H, M, S]
DAILY_QUESTION_TIME = [15, 0, 0]
TIMEZONE = ZoneInfo("America/Santiago")
# Time in days required between a question's appearance (can be float!)
TIME_DAILY_COOLDOWN = 20.0
# Weights of appearance of each difficulty in the order: very easy -> impossible
DIFF_NAMES = ["Muy Fácil", "Fácil", "Intermedia", "Difícil", "Imposible"]
DIFF_DAILY_WEIGHT = [5, 5, 4, 3, 1]
'''
Dev parameters (for avoid spamming in both consoles and chat)
'''
OBTAIN_QUESTIONS_LIMIT = 50
OBTAIN_QUESTIONS_PAGE_LIMIT = 5

# Params for questions in general
'''
IMPORTANT: If you change the alternatives parametrers you must change the whole questions database
to match correctly those new parameters.

'''

TOTAL_ALTERNATIVES = 4

'''
Params of Who wants to be millionaire minigame
'''
TOTAL_QUESTIONS = 18
# Used for the + answers point_cards
EXTRA_ALTERNATIVES = 2
# Point_cards info
EXTRA_ALTERNATIVES_BONUS = 350
QUICK_WILDCARD_BONUS = 200
MULT_WILDCARD = 2
# Wildcards info


#xp increase
XP_DAILY_VERY_EASY = 10
XP_DAILY_EASY = 12
XP_DAILY_MEDIUM = 15
XP_DAILY_HARD = 18
XP_DAILY_IMPOSSIBLE = 25
