

import networkx

def switch_behaviour(state):
    if state["behaviour"] == "hunter":
            mode = "hunter"

    elif state["behaviour"] == "gatherer":
        mode = "gatherer"

    elif state["behaviour"] == "flee":
        mode = "flee"

    return mode



def switch_behaviour_conditions(bot, state):
    if bot.round < 5: # start as a hunter
        state["behaviour"] = "hunter"
    elif (bot.enemy[0] in bot.homezone) or (bot.enemy[1]  in bot.homezone): # any of the enemies in our homezone
        state["behaviour"] = "hunter"
    elif is_barrirer_wide:
        state["behaviour"] = "hunter"





def get_barrier(bot):
    #returns a True is the barrier has a wide oppening
    # just run it once, the layout never changes
    
    #get the barrier shape:
    if bot.is_blue:
        barrier_at_x = bot.shape[0]/2 - 1 # if we are blue, the barrier is at left
    else: # if we are red, the barrier is at right
        barrier_at_x = bot.shape[0]/2
    barrier = [coord for coord in bot.walls if coord[0] == barrier_at_x]
    
    for idx in range(len(barrier)-1):
        if (barrier[idx+1][0] - barrier[idx][0] -1) > 3:
            barrier_is_wide = True
        else:
            barrier_is_wide = False

    return barrier_is_wide

is_barrirer_wide = get_barrier(bot)
        
    
    
    





    return {
        # specifies which personality we are: "gatherer" or "hunter"
        "personality": personality,

        # entries prefixed with "gatherer_" are used by the move_gatherer function
        "gatherer_target": None,
        "gatherer_path": None,

        # entries prefixed with "hunter_" are used by the move_hunter function
        "hunter_target": None,
        "hunter_path": None,
    }

def move(bot, state):
    # Our state consists of two “substates”, one for each bot.
    # In order for the substates to work properly with the imported
    # `move_gatherer` and `move_hunter` functions, we need to be sure
    # that the relevant attributes in the state are properly prefixed
    # (and each of the functions only works with “their” prefixed version).

    if state == {}:
        # here each bot has its own state dictionary (0 and 1)
        state[0] = init_state("gatherer")
        state[1] = init_state("hunter")

    # Only the gatherer can go into the enemy zone and be killed. Therefore
    # we only need to switch roles from the perspective of the hunter.
    if bot.other.was_killed:
        state[bot.turn]["personality"] = "gatherer"
        state[bot.other.turn]["personality"] = "hunter"

    if state[bot.turn]["personality"] == "gatherer":
        next_pos = move_gatherer(bot, state)
        bot.say('gatherer')
    else:
        next_pos = move_hunter(bot, state)
        bot.say('hunter')
    return next_pos
