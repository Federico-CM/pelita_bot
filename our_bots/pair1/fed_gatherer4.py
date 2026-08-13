# This bot selects a food pellet at random, then goes and tries to get it by
# following the shortest path to it.
# It tries on the way to avoid being killed by the enemy: if the next move
# to get to the food would put it on a ghost, then it chooses a random safe
# position

import networkx

TEAM_NAME = 'Fed gatherers'

def init_gather_state():
    return {
            "gatherer_target": None,
            "gatherer_path": None,
        }

def find_nearest_food(bot, food_list):
    min_dist = float("inf")
    best_target = None
    for test_target in food_list:
        test_path = networkx.shortest_path(bot.graph, bot.position, test_target)
        len_test_path = len(test_path)
        if len_test_path < min_dist:
            min_dist = len_test_path
            best_target = test_target
    return(best_target)

def move(bot, state):
    # The state dictionary is initially empty
    if state == {}:
        # Initialize the state dictionary.
        # Each bot needs its own state dictionary to keep track of the
        # food targets.
        state[0] = init_gather_state()
        state[1] = init_gather_state()

    # define a few variables for less typing
    enemy = bot.enemy

    target = state[bot.turn]["gatherer_target"]
    path = state[bot.turn]["gatherer_path"]

    # choose a target food pellet if we still don't have one or
    # if the old target is not there anymore. This can happen for
    # two different reasons:
    #   - the old target has been eaten in the last turn
    #   - the old target has been relocated because of the opponent's defender
    #     sitting near it for too long
    if (target is None) or (target not in enemy[0].food):
        # position of the target food pellet
        target = find_nearest_food(bot, enemy[0].food)
        #target = bot.random.choice(enemy[0].food)
        # use networkx to get the shortest path from here to the target
        # we do not use the first position, which is always equal to bot_position
        path = networkx.shortest_path(bot.graph, bot.position, target)[1:]
        state[bot.turn]["gatherer_path"] = path
        state[bot.turn]["gatherer_target"] = target

    # get the next position along the shortest path to reach our target
    next_pos = path.pop(0)
    # if we are not in our homezone we should check if it is safe to proceed
    # remember enemy = bot.enemy

#XXXXXXXXXXXXXXXXXXXXXXXXXXX
# This is my basic enemy avoidance code
# 

    # always check for danger!
    safe_positions = []
    #path_to_enemy1 = []
    #path_to_enemy2 = []
    unsafe_positions = []

    turn = bot.turn
    if bot.enemy[turn].has_exact_position == True:
        path_to_enemy1 = networkx.shortest_path(bot.graph, bot.position, bot.enemy[0].position)
        if len(path_to_enemy1) <= 4:
            bot.say("O_O")
            unsafe_positions.extend(path_to_enemy1)

    if bot.enemy[turn-1].has_exact_position == True:
        path_to_enemy2 = networkx.shortest_path(bot.graph, bot.position, bot.enemy[1].position)
        if len(path_to_enemy2) <= 4:
            bot.say("T_T")
            unsafe_positions.extend(path_to_enemy2)

    for pos in bot.legal_positions:
        if (
            pos != enemy[0].position
            and pos != enemy[1].position
            and pos not in unsafe_positions
        ):
            safe_positions.append(pos)

    if next_pos not in safe_positions:
        state[bot.turn]["gatherer_target"] = None
        state[bot.turn]["gatherer_path"] = None
        if len(safe_positions) >= 1:
            next_pos = bot.random.choice(safe_positions)
            # if there is no safe option, continue and hope for the best
#XXXXXXXXXXXXXXXXXXXXXXXXXXX

    return next_pos
