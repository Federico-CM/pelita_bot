# This bot does not ever move (useful for testing)

TEAM_NAME = 'StoppingBots'


def is_barrier_wide(bot, treshold=3):
    #returns a True is the barrier has a wide oppening
    # just run it once, the layout never changes
    
    #get the barrier shape:
    if bot.is_blue:
        barrier_at_x = bot.shape[0]/2 - 1 # if we are blue, the barrier is at left
    else: # if we are red, the barrier is at right
        barrier_at_x = bot.shape[0]/2
    barrier = [coord for coord in bot.walls if coord[0] == barrier_at_x]
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
    #returns a True is the barrier has a wide oppening
    # just run it once, the layout never changes
    #get the barrier shape:
    if bot.is_blue:
        barrier_at_x = bot.shape[0]/2 - 1 # if we are blue, the barrier is at left
    else: # if we are red, the barrier is at right
        barrier_at_x = bot.shape[0]/2
    barrier = [coord for coord in bot.walls if coord[0] == barrier_at_x]
    return barrier





def move(bot, state):

    bot.say(bot.other.deaths+bot.other)
    state["is_barrier_wide"] = is_barrier_wide(bot,4)
    bot.say(str(state["is_barrier_wide"]))
    #bot.say(str(get_barrier(bot)))
    # do not move at all
    return bot.position
