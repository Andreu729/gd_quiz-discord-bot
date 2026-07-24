from zoneinfo import ZoneInfo
# Format: [H, M, S]
DAILY_QUESTION_TIME = [15, 0, 0]
TIMEZONE = ZoneInfo("America/Santiago")

'''
Dev parameters (for avoid spamming in both consoles and chat)
'''
OBTAIN_QUESTIONS_LIMIT = 50

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