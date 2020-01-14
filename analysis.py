import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt
import sys

def takeFactorial(n):
    fact = 1
    for i in range(1,n+1):
        fact = fact*i
    return fact

def takeCombination(n,r):
    return takeFactorial(n)/(takeFactorial(n-r)*takeFactorial(r))

def takePermutation(n,r):
    return takeFactorial(n)/takeFactorial(n-r)

def calculateProbability(s,i):
    probabilityValues = []
    probabilityTags = []
    theProbability = (takeCombination(s-1,i-1))/takeCombination(s,i)
    for k in range(0,2):
        if k == 0:
            pass
        else:
            probabilityTags.append(str(k))
            probabilityValues.append(theProbability**k)
    probabilityTags.insert(0,"0")
    probabilityValues.insert(0,1-sum(probabilityValues))
    return probabilityTags,probabilityValues 

def calculateMultiGameProbability(s,i,probabilityValues):
    probabilityMultiPlayValues = []
    probabilityMultiPlayTags = []
    for k in range(0,i+1):
        if k == 0:
            pass
        else:
            probabilityMultiPlayTags.append(str(k))
            probabilityMultiPlayValues.append((probabilityValues[1]**k)*(probabilityValues[0]**(i-k))*takeCombination(i,k))
    probabilityMultiPlayTags.insert(0,"0")
    probabilityMultiPlayValues.insert(0,1-sum(probabilityMultiPlayValues))
    return probabilityMultiPlayTags,probabilityMultiPlayValues 

def plotProbDistribution(tags,values,y_label,x_label,title,figPng):
    fig = plt.figure()
    y_pos = np.arange(len(tags))
    plt.bar(y_pos, values, align='center', alpha=0.5)
    plt.xticks(y_pos, tags)
    plt.ylabel(y_label)
    plt.xlabel(x_label)
    plt.title(title)
    plt.show()
    fig.savefig(figPng)

def calculateExpectedValue(probability,i):
    expectedValue = 0
    for idx,prob in enumerate(probability):
        expectedValue += prob*idx
    return expectedValue

def calculateChi2Statistics(expectedValue,observedData):
    chi2Stat = 0
    for choice,data in observedData.items():
        print((expectedValue-data)**2/expectedValue,"here", expectedValue,"expectedVal",data,"data")
        chi2Stat += (expectedValue-data)**2/expectedValue
    return chi2Stat

if __name__ == "__main__":
    s = int(input("max possible value: "))
    i = int(input("total number: "))
    multi_i = int(input("sample size: "))
    probabilityTags,probabilityValues = calculateProbability(s,i)
    plotProbDistribution(probabilityTags,probabilityValues,"Probability","Number of Occurance","Probability Distribution In Single Game","probabilityDist.png")
    #since the games are independent of each other, their respective probabilities can be multiplied
    probabilityMultiPlayTags,probabilityMultiPlayValues = calculateMultiGameProbability(s,multi_i,probabilityValues)
    expectedValue = calculateExpectedValue(probabilityMultiPlayValues,multi_i)
    #this is the expected value assuming equal distribution of choices. What I suggesting is that, my alternative hypothesis is that, the distributions are 
    #skewed and hence they dont follow an equal distribution of values.
    print(expectedValue,"expectedValue")

    observedData1000Passes = {18:147,3:138,1:137,38:135,47:134,26:134,22:134,21:133,5:133,40:132,17:131,9:131,
    36:130,32:129,41:128,25:127,12:127,42:126,30:126,16:126,23:124,13:124,46:123,29:121,20:120,8:120,2:120,
    49:119,34:119,19:119,15:119,7:119,6:119,48:118,24:118,11:117,4:117,39:116,14:116,44:115,31:115,27:113,
    35:112,10:112,33:110,28:110,45:109,37:107,43:97}

    chi2Stat = calculateChi2Statistics(expectedValue,observedData1000Passes)
    degreeOfFreedom = s-1
    #criticalValue = 60.907 means that getting a 60.907 chi2 value or greater is 10% meaning that 
    #the probability(chi2>=35.596) > %10 hence we fail to reject that the distributions of the number of occurances
    #of the numbers is equal for 1000 sample items with 48 degrees of freedom.
    criticalValue = 60.907
    print(chi2Stat,"chi2stat")
    

    