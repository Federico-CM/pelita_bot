# This bot does not ever move (useful for testing)

TEAM_NAME = 'StoppingBots'

def is_barrier_wide(bot, treshold=3):
    #returns a True is the barrier has a wide oppening
    # just run it once, the layout never changes
    barrier = get_barrier(bot)
    # Extract and sort the y coordinates
    x_values = [x for y, x in barrier]
    # Look for a gap larger than threshold
    for x1, x2 in zip(x_values, x_values[1:]):
        if x2 - x1 >= treshold:
            barrier_is_wide =  True
            break
        else:
            barrier_is_wide = False

    return barrier_is_wide


def get_barrier(bot):
    # returns a True is the barrier has a wide oppening
    # just run it once, the layout never changes
    # get the barrier shape:
    if bot.is_blue:
        barrier_at_x = bot.shape[0]/2 - 1 # if we are blue, the barrier is at left
    else: # if we are red, the barrier is at right
        barrier_at_x = bot.shape[0]/2
    barrier = [coord for coord in bot.walls if coord[0] == barrier_at_x]
    return barrier



def is_enemy_close_to_barrier(bot, enemy_number, threshold=2):
    # function that checks if a enemy bot is near OUR border
    # inputs: bot (as is), enemy number: 0, 1, threshold: value that defines
    # what close (near) mean
    
    # return True, False
    # usage:
        
    # state["is enemy near border?"] = []
    # state["is enemy near border?"].append(is_enemy_close_to_barrier(bot, enemy_number, threshold=2))
    # this initializes the array and you can append to this every turn, to save the states.
    barrier = get_barrier(bot)
    enemy_x = bot.enemy[enemy_number].position[0]
    return any(abs(enemy_x - x) <= threshold for x, _ in barrier)


def is_ally_close_to_barrier(bot, threshold=2):
    # function that checks if a ally bot is near OUR border
    # inputs: bot (as is), threshold: value that defines
    # what close (near) mean
    
    # return True OR False
    # usage:
        
    # state["am i near border?"] = []
    # state["am i near border?"].append(is_ally_close_to_barrier(bot, threshold=2))
    # this initializes the array and you can append to this every turn, to save the states.
    barrier = get_barrier(bot)
    ally_x = bot.position[0]
    return any(abs(ally_x - x) <= threshold for x, _ in barrier)



# def is_there_a_big_cluster(bot, in_homezone=True, threshold=3):
#     if in_homezone: #food in OUR base
#         loc = bot.food
#     else:
#         loc = bot.enemy[0].food
#         # loc =[(17, 8), (24, 8), (17, 7)]
#     mean_food_density = len(loc) / (bot.shape[1]-2)**2
    

import networkx as nx
def is_there_a_big_cluster(bot, in_homezone=True, radius=2, min_food=4):
    food = bot.food if in_homezone else bot.enemy[0].food

    G = nx.Graph()
    G.add_nodes_from(food)

    for i, p1 in enumerate(food):
        for p2 in food[i+1:]:
            if abs(p1[0] - p2[0]) + abs(p1[1] - p2[1]) <= radius:
                G.add_edge(p1, p2)
    return any(len(c) >= min_food for c in nx.connected_components(G))




 function that ve la position dado un bool si double kill y regresa un bool dado
 que tienen cercania a la barrera
def move(bot, state):
    #state["is_barrier_wide"] = is_barrier_wide(bot,4)
    #bot.say(str(state["is_barrier_wide"]))
    
    #bot.say(str(is_enemy_y_close_to_barrier(bot, 0, threshold=)))
    
    # bot.say(str(get_barrier(bot)))
    # print(str(get_barrier(bot)))
    
    bot.say(str(is_there_a_big_cluster(bot, in_homezone=True, radius=2, min_food=8)))
    # do not move at all
    return bot.position
