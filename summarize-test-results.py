import json
import argparse
from pathlib import Path
import sys

parser = argparse.ArgumentParser(description='MongoDB Test Summarizer')
parser.add_argument('--directory',required=True,type=str,help='directory containing test results')
args = parser.parse_args()

p = Path(args.directory)

totalNumPass = 0
totalNumFail = 0
totalNumCC = 0

print("{: <20} | {: <6} | {: <6} | {: <6} | {: <6} | {: <6}".format('test name','  pass','  fail','pass %','num cc','  cc %'))
print("{: <20} | {: <6} | {: <6} | {: <6} | {: <6} | {: <6}".format('--------------------','------','------','------','------','------'))
    
for thisResultFile in sorted(p.glob("*.json")):
    # load JSON results to dictionary
    with open(thisResultFile,'r') as inFh:
    	myDict = json.load(inFh)
    numFail = 0
    numPass = 0
    numCC = 0
    for thisResult in myDict['results']:
        if thisResult['status'] == 'pass':
            numPass += 1
        elif thisResult['status'] == 'fail':
            numFail += 1
        else:
            print("ERROR - found unknown status in {}".format(myDict))
            sys.exit(1)
            
    totalNumPass += numPass
    totalNumFail += numFail
            
    if (numPass + numFail) == 0:
        percentPass = 0.0
    else:
        percentPass = (numPass / (numPass + numFail)) * 100.0
        
    stemmedFileName = thisResultFile.stem
    stemmedFileNameMinusDbaas = stemmedFileName.split('_',1)[1]
    
    # get count of 'causal consistency' errors
    seenDictionary = {}
    with open(args.directory+"/stdout_"+stemmedFileNameMinusDbaas+".log", "r") as inFile:
        for fileLine in inFile:
            if "causal consistency" in fileLine:
                testName = fileLine.split(']')[0]
                if testName not in seenDictionary:
                    numCC += 1
                    seenDictionary[testName] = 1
        
    totalNumCC += numCC

    if (numFail) == 0:
        ccPercent = 0.0
    else:
        ccPercent = (numCC / numFail) * 100.0
    
    print("{: <20} | {:6d} | {:6d} | {:6.2f} | {:6d} | {:6.2f}".format(stemmedFileNameMinusDbaas,numPass,numFail,percentPass,numCC,ccPercent))
    
if (totalNumPass + totalNumFail) == 0:
    totalPercentPass = 0.0
else:
    totalPercentPass = (totalNumPass / (totalNumPass + totalNumFail)) * 100.0

if (totalNumFail) == 0:
    totalCCPercent = 0.0
else:
    totalCCPercent = (totalNumCC / totalNumFail) * 100.0
    
print("{: <20} | {: <6} | {: <6} | {: <6} | {: <6} | {: <6}".format('--------------------','------','------','------','------','------'))
print("{: <20} | {:6d} | {:6d} | {:6.2f} | {:6d} | {:6.2f}".format("TOTAL",totalNumPass,totalNumFail,totalPercentPass,totalNumCC,totalCCPercent))
