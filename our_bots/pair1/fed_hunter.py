# This bot tries to catch an enemy bot. It will stop at the border of its
# homezone if the enemy still did not cross the border.
# As long as the enemies are far away (their position is noisy), the bot
# tries to get near to the bot in the enemy team which has the same turn.
# As soon as an enemy bot is not noisy anymore, i.e. it has come near, the
# bot goes after it and leaves the other enemy alone

import networkx

TEAM_NAME = 'Fed hunters'

def init_hunt_state():
    return {
            "hunter_target": None,
            "hunter_path": None,
        }

def move(bot, state):
    if state == {}:
        state[0] = init_hunt_state()
        state[1] = init_hunt_state()

    turn = bot.turn

# If the position of an enemy bot is known and the enemy is in its teritory
	# If distance is 1 (we are locked)
		# move randomly to valid place
		# prioritize enemies in out territory

    # short variables... too many? is this smelly?
		# perhaps place all short variable names on their own file?
    enemy1 = bot.enemy[turn]
    enemy2 = bot.enemy[turn-1]	
    enemy1_pos_is_known = enemy1.has_exact_position
    enemy2_pos_is_known = enemy2.has_exact_position
    enemy1_in_homezone = enemy1.position in bot.homezone
    enemy2_in_homezone = enemy2.position in bot.homezone
    path_to_enemy1 = networkx.shortest_path(bot.graph, bot.position, enemy1.position)
    path_to_enemy2 = networkx.shortest_path(bot.graph, bot.position, enemy2.position)

	# there is a lot of if statements... this might be smelly
		# we are doing the same check for bot 1 and 2
		# perhaps moving those checks into a single function?
		# it might be a good idea to move some of those functions to tother scripts

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
