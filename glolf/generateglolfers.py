from data import playerstlats
import random
import tqdm
import itertools
from multiprocessing import Pool
import os
from functools import partial
from datetime import datetime
import csv
import sqlite3

def makePlayerName(names):
    firstname = names[random.randrange(0,len(names))].strip().capitalize()
    lastname = names[random.randrange(0,len(names))].strip().capitalize()
    return firstname + " " + lastname

def insertPlayer(name,sample):
    con = sqlite3.connect("players.db")
    cur = con.cursor()

    stlatnames = sample._fields
    stlatvals = [getattr(sample, f) for f in stlatnames]

    stlatvalsformatted = ""
    for s in stlatvals:
        if type(s) is str:
            stlatvalsformatted += f"'{s}', " 
        else:
            stlatvalsformatted += f"{str(s)}, "
    stlatvalsformatted = stlatvalsformatted[:-2] # kill separator

    insertquery = f"""INSERT INTO players VALUES
        ('{name}', {stlatvalsformatted})
        """
    try:
        cur.execute(insertquery)
        con.commit()
    except:
        pass
    con.close()
    return


def genplayerandreport(n_tup):
    n = str(n_tup[0]) + " " + str(n_tup[1]) # compose name from tuple
    sample = playerstlats.generate_random_stlats_from_name(str(n))
    insertPlayer(n,sample)

    return "test"

if __name__ == '__main__':
    
    with open('eff_large_wordlist_no_indexes.txt', 'r',encoding="utf-8") as file:
        names = [line for line in file]

    print('Names loaded from file!')
    
    names = [name.strip().capitalize() for name in names]
    
    glolfer_names_count = len(names)^2
    
    print('Names fixed and capitalized!')
    
    #glolfer_names_tuples = itertools.product(names,names)

    glolfer_names_tuples = [("test","name"),("Wagon","Chitchat"),("Other","Name")]

    print('Name product object created. Clear the blast radius.')

    con = sqlite3.connect("players.db")
    cur = con.cursor()

    placeholder = playerstlats.PlayerStlats()
    stlatvalstring = ', '.join(str(e) for e in placeholder._fields)
    query = f"CREATE TABLE IF NOT EXISTS players (name, {stlatvalstring}, UNIQUE(name))"

    cur.execute(query)
    con.commit()
    con.close()

    with Pool(2) as p:
        results = []
        for n in glolfer_names_tuples:
            results.append(p.apply_async(genplayerandreport, (n,)))

        for r in results: # wait until all workers are done
            r.get()
        print("Done, check the database.")