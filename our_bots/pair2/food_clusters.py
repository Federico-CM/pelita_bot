import networkx as nx
def is_there_a_big_cluster(bot, in_homezone=True, radius=2, min_food=4):
    """
    SUMMARY: a function that detects clusters of food in the maze given some params

    Parameters
    ----------
    bot : as is, default
    in_homezone : bool (True, False) optional
        DESCRIPTION. detect cluster in OUR homezone or not
    radius : int positive, optional
        DESCRIPTION. Radius of detection
    min_food : int postivie, optional
        DESCRIPTION. minimum number of food that has to be in the "cicle" of 
                    radius 

    Returns
    -------
    bool
        DESCRIPTION. True if a cluster of min food or more is in a cirlce or radius
        in a zone (enemy or ally) of the maze
    """
    food = bot.food if in_homezone else bot.enemy[0].food

    G = nx.Graph()
    G.add_nodes_from(food)

    for i, p1 in enumerate(food):
        for p2 in food[i+1:]:
            if abs(p1[0] - p2[0]) + abs(p1[1] - p2[1]) <= radius:
                G.add_edge(p1, p2)
    return any(len(c) >= min_food for c in nx.connected_components(G))


# def is_there_a_big_cluster(bot, in_homezone=True, radius=2, min_food=4):
#     food = bot.food if in_homezone else bot.enemy[0].food

#     for y1, x1 in food:
#         count = 0
#         for y2, x2 in food:
#             if abs(y1 - y2) + abs(x1 - x2) <= radius:
#                 count += 1
#         if count >= min_food:
#             return True
#     return False