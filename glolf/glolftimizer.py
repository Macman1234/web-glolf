from data import playerstlats
import random
import tqdm
import itertools

def makePlayerName(names):
    firstname = names[random.randrange(0,len(names))].strip().capitalize()
    lastname = names[random.randrange(0,len(names))].strip().capitalize()
    return firstname + " " + lastname

if __name__ == '__main__':

    optimize_for_bad = True

    stlats_to_max = ["ritualism","owlishness","softness","finesse","needlethreadableness","estimation","left_handedness","musclitude", "tofu", "wiggle","marbles","churliness","earliness","twirliness","polkadottedness"]
    optimize_moons = True
    moons_to_max = ["Precision"]

    name_count = 30229200
    
    with open('eff_large_wordlist_no_indexes.txt', 'r',encoding="utf-8") as file:
        names = [line for line in file]

    print('Names loaded from file!')
    
    names = [name.strip().capitalize() for name in names]
    
    glolfer_names_count = len(names)^2
    
    print('Names fixed and capitalized!')
    
    glolfer_names_tuples = itertools.product(names,names)

    print('Name product object created. Clear the blast radius.')

    current_max_sum = 0
    if optimize_for_bad: current_max_sum = 9999
    current_max_name = ""
    
    pbar = tqdm.trange(pow(len(names),2))
    for i in pbar:
        n_tup = next(glolfer_names_tuples)
        n = str(n_tup[0]) + " " + str(n_tup[1])
        sample = playerstlats.generate_random_stlats_from_name(str(n))
        if optimize_moons:
            moon_sum = 0
            
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

            if "Driving" in moons_to_max: 
                moon_sum += (sample.musclitude + sample.tofu)*5/2
            if "Precision" in moons_to_max: 
                moon_sum += ((1-sample.needlethreadableness)*0.5 + sample.finesse + sample.estimation*0.2) * 5/(1+0.2+0.5) - abs(sample.left_handedness)
            if "Aerodynamics" in moons_to_max:
                moon_sum += (sample.ritualism + sample.owlishness + sample.softness) * 5/3 #unused for now, need more stlats
            if "Self Awareness" in moons_to_max:
                moon_sum += (sample.wiggle*0.5 + (sample.marbles-2)/2 + unpredictability*0.8) * 5/(0.5+1+0.8) + sample.polkadottedness * 5 #means nothing for now
            if (moon_sum > current_max_sum) and not optimize_for_bad:
                current_max_sum = moon_sum
                current_max_name = str(n)
            if (moon_sum < current_max_sum) and optimize_for_bad:
                current_max_sum = moon_sum
                current_max_name = str(n)
                #print(str(n) + ": " + str(moon_sum))
                pbar.set_description(str(n) + ": " + str(moon_sum))
        else:
            stlat_sum = 0
            for stlat in stlats_to_max:
                stlat_value = sample.__getattribute__(stlat)
                if stlat == "capitalism": stlat_value = -stlat_value
                if stlat == "left_handedness": stlat_value = 1- abs(stlat_value)
                if stlat == "needlethreadableness": stlat_value = 1- abs(stlat_value)
                stlat_sum += stlat_value
            if stlat_sum > current_max_sum:
                current_max_sum = stlat_sum
                current_max_name = str(n)


if optimize_moons: print(f"found name {current_max_name} with moon sum {current_max_sum}")
else: print(f"found name {current_max_name} with stat sum {current_max_sum}")