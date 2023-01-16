
from ast import Try
from cmath import e
from dumpObject import dobj
import os
import glob
import random
import re
import math


# this function returns token, typecount and type set ( unique word list) from a  text file file
def readTxtData(path: str) -> dobj:
        
        if(type(path) is not str):
             raise Exception("Some paths in lists are not valid path. Path should be string")

        if path is None or not os.path.exists(path):
            raise Exception("Please provide a valid path.")

        wordSet = dobj()
        wordSet.totalWordCount = 0
        wordSet.uniqueWordCount = 0
        uniqueWordSet = set()
        # Open file
        with open(path, "r") as file1:

            # Read and extract into a set
            for line in file1:
                #word_list_from_line = re.split(r'\s+', line.lower().strip("\n").strip())
                #wordSet.totalWordCount += len(word_list_from_line)
                word_list_from_line = line.translate(str.maketrans('','',string.punctuation))
                word_list_from_line=word_list_from_line.lower()
                word_list_from_line=word_list_from_line.split()
                uniqueWordSet.update(word_list_from_line)

        wordSet.uniqueWordCount = len(uniqueWordSet)
        wordSet.uniqueWordSet = uniqueWordSet
        # Return the set
        return wordSet

# this function gets all the .txt files inside a given folder
def getAllBookPath(pathOfFolder: str) -> list:
        if pathOfFolder is None or not os.path.exists(pathOfFolder):
            raise Exception("Please provide a valid path.")

        # Load a random file from the folder.

        files = glob.glob(pathOfFolder + "/*.txt")
        poolOfFiles = []
        # loop through list of files
        for f in files:
            poolOfFiles.append(f)

        return poolOfFiles


# this function takes a list of txt files and samples it.
def SampleConversation(paths : list) -> dobj:
        # read all the files and sample them

        subSample = []

        for path in paths:
            subSample.append(readTxtData(path))

        #Now subsample contains word count and unique word count ( number of token and types)
        #We can caluclate average or whatever from this data.

        finalsample = dobj()
        finalsample.uniqueWordSet = {}
        finalsample.totalWordCount = 0
        
        for elem in subSample:
            finalsample.totalWordCount += elem.totalWordCount
            finalsample.uniqueWordSet = set().union(finalsample.uniqueWordSet).union(elem.uniqueWordSet)

        finalsample.uniqueWordCount = len(finalsample.uniqueWordSet)

        return finalsample


    #This function can be called to sample a folder for x days with newBooks new books each day.
def sampleGroupForXXXXXXdaysOLD(xdays: int, folderPath: str, newBooks: int):
    
    listofFiles = getAllBookPath(folderPath)
    random.shuffle(listofFiles)
    lastSample = None
    graphData = []
    day = 1
    listLen = len(listofFiles)
    filePointer = 0
    
    if listLen == 0:
        raise("there are no content to sample. the folder does not contains any text files.")

    while day <= xdays:
        #Do the sampling.
        if filePointer == listLen:
            break

        newList = []
        tempNewBooks = newBooks
        while tempNewBooks > 0:
            newList.append(listofFiles[filePointer])
            filePointer += 1
            tempNewBooks -= 1
            if filePointer == listLen:
                print('Not enought content to sample, sampling whatever content is left')
                break
        
        newSampling = SampleConversation(newList)

        # Sample yesterday sampling and todays sampling
        finalSampling = sampleTwoSamplings(newSampling, lastSample)

        # this is daily data required for graphing
        graphObj = dobj()
        graphObj.day = day
        graphObj.totalWordCount = finalSampling.totalWordCount
        graphObj.uniqueWordCount = finalSampling.uniqueWordCount
        graphObj.averaged = False

        #print("day is: " + str(graphObj.day) + " totalWordCount : " + str(graphObj.totalWordCount) + " unique word count : " + str(graphObj.uniqueWordCount))

        graphData.append(graphObj)

        lastSample = finalSampling
        day += 1

    return graphData

def sampleGroupForXdays(xdays: int, bookFolderPath: str, newBooks: int, convoFolderPath:str, newConvo: int):
    
    listofBooks = getAllBookPath(bookFolderPath)
    listofConvo = getAllBookPath(convoFolderPath)

    random.shuffle(listofBooks)
    random.shuffle(listofConvo)

    lastSample = None
    graphData = []
    day = 1

    bookLen = len(listofBooks)
    convoLen = len(listofConvo)

    bookPointer = 0
    convoPointer = 0
    
    if bookLen == 0 or convoLen == 0:
        raise("there are no enough content to sample. one of the given folder is empty.")

    totalRequiredBooks = xdays * newBooks
    totalRequiredConvo = xdays * newConvo

    if totalRequiredBooks > bookLen:
        print(str(totalRequiredBooks) + " books are necessary for sampling but only availabe books are: " + str(bookLen) +
       ". Warning, sampling will be done by whatever available. ")

    if totalRequiredConvo > convoLen:
       print(str(totalRequiredConvo) + " conversations are necessary for sampling but only availabe conversations are: " + str(convoLen) +
       ". Warning, sampling will be done by whatever available. ")

    while day <= xdays:
        #Do the sampling.
        if bookPointer == bookLen or convoPointer == convoLen:
            break

        newList = []
        tempNewBooks = newBooks
        tempNewConvo = newConvo

        while tempNewConvo > 0:
            newList.append(listofConvo[convoPointer])
            convoPointer += 1
            tempNewConvo -=1
            if convoPointer == convoLen:
                print('Not enought conversation to sample, sampling whatever content was left')
                break

        while tempNewBooks > 0:
            newList.append(listofBooks[bookPointer])
            bookPointer += 1
            tempNewBooks -= 1
            if bookPointer == bookLen:
                print('Not enought book to sample, sampling whatever content is left')
                break
        
        newSampling = SampleConversation(newList)

        # Sample yesterday sampling and todays sampling
        finalSampling = sampleTwoSamplings(newSampling, lastSample)

        # this is daily data required for graphing
        graphObj = dobj()
        graphObj.day = day
        graphObj.totalWordCount = finalSampling.totalWordCount
        graphObj.uniqueWordCount = finalSampling.uniqueWordCount
        graphObj.averaged = False

        #print("day is: " + str(graphObj.day) + " totalWordCount : " + str(graphObj.totalWordCount) + " unique word count : " + str(graphObj.uniqueWordCount))

        graphData.append(graphObj)

        lastSample = finalSampling
        day += 1

    return graphData

def sampleTwoSamplings(sample1, sample2):

    if sample1 is None:
        return sample2

    if sample2 is None:
        return sample1
        
    finalsample = dobj()
    
    finalsample.totalWordCount = sample1.totalWordCount + sample2.totalWordCount
    finalsample.uniqueWordSet = set().union(sample1.uniqueWordSet).union(sample2.uniqueWordSet)
    finalsample.uniqueWordCount = len(finalsample.uniqueWordSet)

    return finalsample

def sampleGroupForXdaysNTimes(xdays: int, bookFolderPath: str, newBooks: int, convoFolderPath:str, newConvo:int, nTimes: int):
    if nTimes <= 0:
        raise("N times should be greater than 0")

    #[[day1, day2,day3 ...dayn], [day1, day2,day3 ...dayn], [day1, day2,day3 ...dayn]]
    iterations = []
    
    while nTimes > 0:
        oneIteration = sampleGroupForXdays(xdays, bookFolderPath, newBooks, convoFolderPath, newConvo)
        print(str(nTimes) + " th iteration done.")
        iterations.append(oneIteration)
        nTimes -=1

    graphObj = dobj()
    graphObj.day = xdays
    graphObj.totalWordCount = 0
    graphObj.uniqueWordCount = 0
    graphObj.averaged = True
    divisor = len(iterations)
    #now average the data
    print('calculating the average ....')
    counter = 0
    while counter < xdays:
        for item in iterations:
            graphObj.totalWordCount += item[counter].totalWordCount
            graphObj.uniqueWordCount += item[counter].uniqueWordCount

        graphObj.totalWordCount = math.ceil(graphObj.totalWordCount/divisor)
        graphObj.uniqueWordCount = math.ceil(graphObj.uniqueWordCount/divisor)
        print("day is: " + str(counter+1) + " avg totalWordCount : " + str(graphObj.totalWordCount) + " avg unique word count : " + str(graphObj.uniqueWordCount))

        counter +=1


    return graphObj



def SampleLowGroup ( bookFolder: str):
    finalResultList = sampleGroupForXdays(365, bookFolder, 5)
    # Now graph it maybe

def SampleMiddleGroup( bookFolder: str):
    finalResultList = sampleGroupForXdays(365, bookFolder, 10)
    # Now graph it.

def SampleHighGroup( bookFolder: str):
    finalResultList = sampleGroupForXdays(365, bookFolder, 17)
    # Now graph it.
