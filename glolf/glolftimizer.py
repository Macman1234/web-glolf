from data import playerstlats
import random
import tqdm
import itertools
from multiprocessing import Pool
import csv
import os
from functools import partial

def makePlayerName(names):
    firstname = names[random.randrange(0,len(names))].strip().capitalize()
    lastname = names[random.randrange(0,len(names))].strip().capitalize()
    return firstname + " " + lastname

def calculateScore(query,sample):
    if "Driving" in moons_to_max: 
        moon_sum += (sample.musclitude + sample.tofu)*5/2
    if "Precision" in moons_to_max: 
        moon_sum += ((1-sample.needlethreadableness)*0.5 + sample.finesse + sample.estimation*0.2) * 5/(1+0.2+0.5) - abs(sample.left_handedness)
    if "Aerodynamics" in moons_to_max:
        moon_sum += (sample.ritualism + sample.owlishness + sample.softness) * 5/3 #unused for now, need more stlats
    if "Self Awareness" in moons_to_max:
        moon_sum += (sample.wiggle*0.5 + (sample.marbles-2)/2 + unpredictability*0.8) * 5/(0.5+1+0.8) + sample.polkadottedness * 5 #means nothing for now

def genplayerandreport(queries,n_tup):
    n = str(n_tup[0]) + " " + str(n_tup[1]) # compose name from tuple
    result = {"name":n}
    sample = playerstlats.generate_random_stlats_from_name(str(n))
    for q in queries:
        print(f"query is: {q}")
        score = 0
        result[q["queryname"]] = score
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
        
    print(queries)

    name_count = 30229200
    
    """
    with open('eff_large_wordlist_no_indexes.txt', 'r',encoding="utf-8") as file:
        names = [line for line in file]

    print('Names loaded from file!')
    
    names = [name.strip().capitalize() for name in names]
    
    glolfer_names_count = len(names)^2
    
    print('Names fixed and capitalized!')
    
    #glolfer_names_tuples = itertools.product(names,names)
    """
    glolfer_names_tuples = [("test","name"),("Wagon","Chitchat"),("Other","Name")]

    print('Name product object created. Clear the blast radius.')

    with Pool(1) as p:
        worker = partial(genplayerandreport,queries)
        results = list(tqdm.tqdm(p.imap(worker,glolfer_names_tuples)))

    print(results)