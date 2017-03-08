import random
from bisect import bisect
import settings as s
import csv

def pcm():
    dictExcDemand = {}            
    
    with open(s.DIST_FILE,'r') as distFile:
            reader = csv.DictReader(distFile)
            znDistDict = {}
            for row in reader:
                key = int(row['InputID'])
                tarZone = int(row['TargetID'])
                tarZoneDist = float(row['Distance'])
                zoneList=znDistDict.get(key,[])
                # Distances have been restricted to those less than 25 km from the target zone
                znDistDict[key]=zoneList+[tarZone]
                     
    with open(s.ELEC_FILE,'r') as eFile:
        reader = csv.DictReader(eFile)
        for row in reader:
            znID = int(row['DAUID'])
            znPop = int(row['PERSONS'])
            znEmp = int(row['EMPLOYEES'])
            znDemand = float(row['KWH_2014'])
            genCt = 9*[0]
            genProb = 9*[0]
            if znPop>0:
                for i in range(znPop):
                    p = perGen()
                    genCt[p]+=1.00
                    genProb[p]=genCt[p]/znPop
            else:
                for i in range(znEmp):
                    p = perGen()
                    genCt[p]+=1.00
                    genProb[p]=genCt[p]/znEmp

            znSupply = 0
            currTarList = znDistDict.get(znID,[])
            for zn in currTarList:
                tarSupply=dictExcDemand.get(zn,0)
                znSupply+= tarSupply
            print znSupply    
                
            while znSupply<znDemand:
                g = znGen(genProb)
                currSupply = s.GEN_DICT[g]
                znSupply+=currSupply
                znDemand = znDemand - znSupply
            dictExcDemand[znID]=abs(znDemand)
            print "Calculating generation for zone: ", znID    
            
def znGen(genProb):
    total = 0
    for g in range(len(genProb)):
        total = total + genProb[g]
        genProb[g] = total
    b = bisect(genProb,random.random())

    return s.genList[b]
    
def perGen():
    genProb = 9*[0]
    genProb[0] = 0.40
    genProb[1] = 0.42
    genProb[2] = 0.00
    genProb[3] = 0.01
    genProb[4] = 0.10
    genProb[5] = 0.01
    genProb[6] = 0.05
    genProb[7] = 0.01
    genProb[8] = 0.00
    
    total = 0
    for g in range(len(genProb)):
        total = total + genProb[g]
        genProb[g] = total
    b = bisect(genProb,random.random())

    return b
    
if __name__ == '__main__':
    pcm()
    
 # This should be based on finding a zone in which the majority of residents are willing to accept
 # that type of generation (majority rules!)
# -If a person choices either small-scale option then they automatically generate it on their property.
 # This should then be subtracted from zonal total.
# -I also want to examinine the incentives with a carbon tax so the utility will change based on the cost of generation
# -I also want to examine the cost when a rebate program or some such program is in place (in conjuction with carbon tax so lower income person gets rebate, but not richer?? That'd be cool!)
# -How far are we with current mix from what this would give us all else being equal (to the best of my ability/knowledge of course)?
# -Could we make an assumption about base load sources that are hard to ramp up/down? Don't want to say they have to run at capacity once a zone chooses to use them, but could we test some factor that says "coal is being
# requested in another zone. If it is your 2nd choice then generate. Or, have a constant for utility of generation when already being generated in another zone. Neighbours are using it so we should too."
# -Employment only zones will have generation mix initially determined from residential generation mix within 25km

# Need to separate the generation preference task from the generation location task. Process is:
# 1. Create a synthetic population
# 2. Assign population to zones for residence and employment. People should be assigned to a work zone within 25 km of their residence zone and occupation targets are also defined for each zone so we can use those too.
# 3. Run a choice model of what type people like and keep track of totals by generation type by zone
# 4. Loop through small-scale generation and zones and place in zone immediately until the total number of people requesting it are satisfied. This is an individual vote rather than collective vote because on their private property.
#    Similar process for employment, but we assume some amount is created based on number of employees who request it.
# 5. Loop through generation types and zones. Start with the largest total for zone and search for a zone to build it in. The idea is that for each plant, you cycle through the zones within 25 km and residents vote whether they want it.
#    When you reach a zone with a population+employment density below a threshold, it gets put there if no one wants it in their zone.
# 6. Once everyone is satisfied, we have a map of the location of plants that satisfy demand
