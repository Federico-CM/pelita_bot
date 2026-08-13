
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

def get_entrances(bot):
    """
    SUMMARY: function that gives a list of coordinates of OUR entrances

    Parameters
    ----------
    bot : as is

    Returns
    -------
    list of tuples
        DESCRIPTION: list of tuples (coordinates (x,y)) there our entrances are        
    """
    if bot.is_blue:
        barrier_at_x = bot.shape[0]/2 - 1 # if we are blue, the barrier is at left
    else: # if we are red, the barrier is at right
        barrier_at_x = bot.shape[0]/2
    barrier = [coord for coord in bot.walls if coord[0] == barrier_at_x]
    entrances = [(barrier_at_x, y) for y in range(bot.shape[1])]
    entrances = list(set(entrances) - set(barrier))
    return entrances


def is_enemy_close_to_barrier(bot, enemy_number, threshold=2):
    """
    SUMMARY: function to determine whether an enemy[num] is near a barrier
    !!! CAUTION: THE DISTANCE CAN BE ACCURATE OR NOT

    Parameters
    ----------
    bot : as is
    enemy_number: 0, 1 bot number, the bot you want to acces
    threshold : positive int, optional
        DESCRIPTION: the radius of detection

    Returns
    -------
    bool: True if the position of current bot is less or equal to threshold from
    the entrances (manhattan)
    """
    barrier = get_barrier(bot)
    enemy_y, enemy_x = bot.enemy[enemy_number].position
    is_near = any( abs(enemy_y - y) + abs(enemy_x - x) <= threshold for y, x in barrier)
    return is_near


def is_ally_close_to_barrier(bot, current=True, threshold=2):
    """
    SUMMARY: function to determine whether an ally is near a barrier

    Parameters
    ----------
    bot : as is
    threshold : positive int, optional
        DESCRIPTION: the radius of detection
    current : bool, optional
        DESCRIPTION: sets the bot to current (True) or the other (False)
    Returns
    -------
    bool: True if the position of current bot is less or equal to threshold from
    the entrances (manhattan)
    """
    barrier = get_barrier(bot)
    if current:
        ally_y, ally_x = bot.position
    else:
        ally_y, ally_x = bot.other.position
    is_near = any( abs(ally_y - y) + abs(ally_x - x) <= threshold for y, x in barrier)
    return is_near


def is_enemy_close_to_entrances(bot, enemy_number, threshold=2):
    """
    SUMMARY: function to determine whether an enemy[num] is near an entrance
    !!! CAUTION: THE DISTANCE CAN BE ACCURATE OR NOT

    Parameters
    ----------
    bot : as is
    enemy_number: 0, 1 bot number, the bot you want to acces
    threshold : positive int, optional
        DESCRIPTION: the radius of detection

    Returns
    -------
    bool: True if the position of current bot is less or equal to threshold from
    the entrances (manhattan)
    """
    entrances = get_entrances(bot)
    enemy_y, enemy_x = bot.enemy[enemy_number].position
    is_near = any( abs(enemy_y - y) + abs(enemy_x - x) <= threshold for y, x in entrances)
    return is_near


def is_ally_close_to_entrances(bot, current=True, threshold=2):
    """
    SUMMARY: function to determine whether an ally is near an entrance

    Parameters
    ----------
    bot : as is
    threshold : positive int, optional
        DESCRIPTION: the radius of detection
    current : bool, optional
        DESCRIPTION: sets the bot to current (True) or the other (False)

    Returns
    -------
    bool: True if the position of current bot is less or equal to threshold from
    the entrances (manhattan)
    """
    entrances = get_entrances(bot)
    if current:
        ally_y, ally_x = bot.position
    else:
        ally_y, ally_x = bot.other.position
    is_near = any( abs(ally_y - y) + abs(ally_x - x) <= threshold for y, x in entrances)
    return is_near
