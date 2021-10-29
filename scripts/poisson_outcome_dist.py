
import pandas as pd
import numpy as np
import math

def proba_goals(num_goals, xG):
    """
        Calculates the probability of a given number of goals
    """
    a = math.pow(np.exp(1), -xG)
    b = math.pow(xG, num_goals)
    c = (a*b)/math.factorial(num_goals)
    return c

def prob_outcome(xG_home, xG_away):
    """
        Calculates outcome probability of a match
    """

    prob_home = 0
    prob_draw = 0
    prob_away = 0
    num_goals = 6
    for i in range(num_goals):
        for j in range(num_goals):
            if i > j:
                prob_home += proba_goals(i, xG_home) * proba_goals(j, xG_away)
            if i == j:
                prob_draw += proba_goals(i, xG_home) * proba_goals(j, xG_away)
            if i < j:
                prob_away += proba_goals(i, xG_home) * proba_goals(j, xG_away)
    return {"HomeProb":round(prob_home, 4), "DrawProb":round(prob_draw, 4), "AwayProb":round(prob_away, 4)}
    
