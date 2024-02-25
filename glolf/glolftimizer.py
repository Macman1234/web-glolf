from data import playerstlats
import random
import tqdm
import itertools
from multiprocessing import Pool
import csv
import os
from functools import partial
from datetime import datetime

def makePlayerName(names):
    firstname = names[random.randrange(0,len(names))].strip().capitalize()
    lastname = names[random.randrange(0,len(names))].strip().capitalize()
    return firstname + " " + lastname

def calculateScore(query,sample):

    score = 0

    weights = [sample.churliness,sample.earliness,sample.twirliness]
    if sample.stance in ("Aggro","Powerful","Hand to Hand","DPS","Explosive","Hardcore","Wibble","Electric"): #offense-boosting stances
        weights[0] += 0.5
    # earliness-boosting stances
    elif sample.stance in ("Tanky","Twitchy","Repose","Reverse","Softcore","Cottagecore","Pomegranate"): # defense-boosting stances
        weights[1] += 0.5
    #twirliness-boosting stances
    if sample.stance in ("Feint","Tricky","Pop-Punk","Flashy","Spicy","Corecore","Wobble","Lefty"): # style-boosting stances
        weights[2] += 0.5

    weights = sorted(weights, reverse=True)

    chanceOfBiggest = weights[0]/sum(weights) #this ranges from highest = 1 to lowest = 1/len(weights)

    minChance = 1/len(weights)

    unpredictability = 1-(chanceOfBiggest-minChance)/(1-minChance)

    drivingval = (sample.musclitude + sample.tofu)*5/2
    precisionval = ((1-sample.needlethreadableness)*0.5 + sample.finesse + sample.estimation*0.2) * 5/(1+0.2+0.5) - abs(sample.left_handedness)
    aerodynamicsval = (sample.ritualism + sample.owlishness + sample.softness) * 5/3 #unused for now, need more stlats
    selfawarenessval = (sample.wiggle*0.5 + (sample.marbles-2)/2 + unpredictability*0.8) * 5/(0.5+1+0.8) + sample.polkadottedness * 5 #means nothing for now

    for stlat in query["stlats"]:
        if stlat["minmax"] == "min": sign = -1
        else: sign = 1
        if stlat["name"] == "driving":
            score += drivingval * sign
        if stlat["name"] == "precision":
            score += precisionval * sign
        if stlat["name"] == "aerodynamics":
            score += aerodynamicsval * sign
        if stlat["name"] == "selfawareness":
            score += selfawarenessval * sign

    return score


def genplayerandreport(queries,n_tup):
    n = str(n_tup[0]) + " " + str(n_tup[1]) # compose name from tuple
    result = {"name":n}
    sample = playerstlats.generate_random_stlats_from_name(str(n))
    for q in queries:
        result[q["queryname"]] = calculateScore(q,sample)
    return result

if __name__ == '__main__':

    queries = []

    querypath = "/home/mac/web-glolf/glolf/queries"

    for filename in os.listdir(querypath):
        with open(os.path.join(querypath, filename)) as csvfile:
            queryreader = csv.reader(csvfile)
            stlats = []
            next(queryreader) # toss out header
            for row in queryreader:
                stlats.append({"name": row[0],"minmax": row[1]})
            queries.append({"queryname": filename, "stlats": stlats})
        
    print('Queries loaded from files!')
    
    with open('eff_large_wordlist_no_indexes.txt', 'r',encoding="utf-8") as file:
        names = [line for line in file]

    print('Names loaded from file!')
    
    names = [name.strip().capitalize() for name in names]
    
    glolfer_names_count = len(names)^2
    
    print('Names fixed and capitalized!')
    
    glolfer_names_tuples = itertools.product(names,names)

    #glolfer_names_tuples = [("test","name"),("Wagon","Chitchat"),("Other","Name")]

    print('Name product object created. Clear the blast radius.')

    with Pool(8) as p:
        worker = partial(genplayerandreport,queries)
        results = list(tqdm.tqdm(p.imap(worker,glolfer_names_tuples), total=pow(len(names),2)))

    with open(f'report.{datetime.now()}.csv', 'w', newline='') as csvfile:
        reportwriter = csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
        reportwriter.writerow(results[0].keys())
        for r in results:
            name = r.pop("name")
            scores = r.values()
            reportwriter.writerow([name] + list(scores))