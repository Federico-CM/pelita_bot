# This bot does not ever move (useful for testing)

TEAM_NAME = 'StoppingBots'


def get_barrier(bot):
    # returns a True is the barrier has a wide oppening
    # just run it once, the layout never changes
    # state["is_barrier_wide"] = False
    #get the barrier shape:
    if bot.is_blue:
        barrier_at_x = bot.shape[0]/2 - 1 # if we are blue, the barrier is at left
    else: # if we are red, the barrier is at right
        barrier_at_x = bot.shape[0]/2
    barrier = [coord for coord in bot.walls if coord[0] == barrier_at_x]
    
    for idx in range(len(barrier)-1):
        if (barrier[idx+1][0] - barrier[idx][0] -1) > 2:
            is_barrier_wide = True
        else:
            is_barrier_wide = False

    return is_barrier_wide



def move(bot, state):
    state["is_barrier_wide"] = get_barrier(bot)
    bot.say(str(state["is_barrier_wide"]))
    #bot.say(bot.homezone)
    #str(state["is_barrier_wide"])
    # do not move at all
    return bot.position
