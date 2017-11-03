__author__ = "Azharuddin Ruhit"

import numpy as np
from math import sqrt


def pearson(prefs, p1, p2):
    si = {}
    for item in prefs[p1]:
        if item in prefs[p2]:
            si[item] = 1
    if len(si) == 0:
        return 0
    n = len(si)
    sum1 = sum([prefs[p1][it] for it in si])
    sum2 = sum([prefs[p2][it] for it in si])
    sum1Sq = sum([pow(prefs[p1][it], 2) for it in si])
    sum2Sq = sum([pow(prefs[p2][it], 2) for it in si])
    pSum = sum([prefs[p1][it] * prefs[p2][it] for it in si])
    num = pSum - sum1 * sum2 / n
    den = sqrt((sum1Sq - pow(sum1, 2) / n) * (sum2Sq - pow(sum2, 2) / n))
    if den == 0:
        return 0
    r = num / den
    return r


def getRecommendations(prefs, user, n=3, similarity=pearson):
    totals = {}
    simSums = {}
    for other in prefs:
        if other == user:
            continue
        sim = similarity(prefs, user, other)
        if sim <= 0:
            continue
        for item in prefs[other]:
            if item not in prefs[user] or prefs[user][item] == 0:
                totals.setdefault(item, 0)
                totals[item] += prefs[other][item] * sim
                simSums.setdefault(item, 0)
                simSums[item] += sim
    rankings = [(round(total / simSums[item]), item)
                for (item, total) in totals.items()]
    rankings.sort()
    rankings.reverse()
    return rankings[0:n]