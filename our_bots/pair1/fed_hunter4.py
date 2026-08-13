# This bot tries to catch is the hunterbot with some upgrades:
# The bot prioritizes enemies in its territory, even unseen ones
# When at the border, the bot tries to bait enemis
# 

import networkx
from barier_module import is_ally_close_to_entrances

TEAM_NAME = 'Fed hunters'

# The bot saves its stuff here
def init_hunt_state():
    return {
            # specifies which personality we are: "gatherer" or "hunter"
            "personality": None,
            "previous_kills": 0,     # recently implemented
            "time_since_kill": 0, # recently implemented
            "hunter_target": None,
            "hunter_path": None,
        }

def move(bot, state):
    if state == {}:
        state[0] = init_hunt_state()
        state[1] = init_hunt_state()

    turn = bot.turn

    # USEFUL ABREVIATIONS
    max_killtime = 15
    total_kills = bot.other.kills + bot.kills
    enemy1 = bot.enemy[turn]
    enemy2 = bot.enemy[turn-1]    
    enemy1_pos_is_known = enemy1.has_exact_position
    enemy2_pos_is_known = enemy2.has_exact_position
    enemy1_in_homezone = enemy1.position in bot.homezone
    enemy2_in_homezone = enemy2.position in bot.homezone
    path_to_enemy1 = networkx.shortest_path(bot.graph, bot.position, enemy1.position)
    path_to_enemy2 = networkx.shortest_path(bot.graph, bot.position, enemy2.position)


    # ROLE SWITCHING LOGIC

    #bot.say(state[bot.other.turn]["time_since_kill"])

    # Time-between-kills count
	# Only increase if it has been activated and below the max_killtime
    if (state[bot.turn]["time_since_kill"] > 0) and (state[bot.turn]["time_since_kill"] < max_killtime) :
        state[bot.turn]["time_since_kill"] += 1
        state[bot.other.turn]["time_since_kill"] += 1
    else:
        state[bot.turn]["time_since_kill"] = 0
        state[bot.other.turn]["time_since_kill"] = 0

    # If the timer was 0 when we killed a bot, start the countdown.
    # If the timer was already running when we killed a bot, switch roles.
    if total_kills > state[bot.turn]["previous_kills"]:
        if state[bot.turn]["time_since_kill"] == 0:
            state[bot.turn]["time_since_kill"] = 1
            state[bot.other.turn]["time_since_kill"] = 1
        else:
            # Switch to gather.
            if is_ally_close_to_entrances(bot,threshold=3):
                bot.say("Gather")
                state[bot.turn]["personality"] = "gatherer"
            pass

    # Keep tabs of the kills
    state[bot.turn]["previous_kills"] = total_kills
    state[bot.other.turn]["previous_kills"] = total_kills


    # Prioritize enemies in our territory that we can locate
    if  enemy1_pos_is_known and enemy1_in_homezone:
        target = enemy1.position

    elif enemy2_pos_is_known and enemy2_in_homezone:
        target = enemy2.position

    # Then, chase enemies in our territory
    elif enemy1_in_homezone:
        target = enemy1.position

    elif enemy2_in_homezone:
        target = enemy2.position

    # If we are stuck at the border, try to bait the enemy
    elif enemy1_pos_is_known and not enemy1_in_homezone and len(path_to_enemy1) == 2:
        target = bot.random.choice(bot.legal_positions)

    elif enemy2_pos_is_known and not enemy2_in_homezone and len(path_to_enemy2) == 2:
        target = bot.random.choice(bot.legal_positions)

    # Barring that, go for whichever enemy is visible
    elif enemy1_pos_is_known:
        target = enemy1.position

    elif enemy2_pos_is_known:
        target = enemy2.position

    # if both enemies are far away just the rough position of the enemy
    else:
        target = enemy1.position

    # get the next position along the shortest path to our target enemy bot
    if target != bot.position:
        next_pos = networkx.shortest_path(bot.graph, bot.position, target)[1]
    else:
        next_pos = bot.position
    # we save the current target in our state dictionary
    state[bot.turn]["hunter_target"] = target

    # let's check that we don't go into the enemy homezone, i.e. stop at the
    # border
    if next_pos in enemy1.homezone:
        next_pos = bot.position

    return next_pos
