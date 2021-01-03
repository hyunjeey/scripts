# This script is designed for the following QA checks:
# - GoldFile coverage
# - Modalities
# - Duplicates
# - Accuracy for punctuation
# - Accuracy for spacing

# Author: Hyunjee Yoon
# Date: 01/01/2020
# Usage: python3 codes_for_QAchecks.py <inputDataFilePath> <goldDataFilePath>
# Example: python3 codes_for_QAchecks.py inputFile.txt --goldFilePath=goldFile.txt

import argparse
import magic
import math
import csv
import sys
import re

parser = argparse.ArgumentParser()
parser.add_argument("inputFilePath", help="Path to the txt file to QA")
parser.add_argument("--goldFilePath", help="Path to the txt file of goldFile")
args = parser.parse_args()

def inputFiles(inputFilePath, goldFilePath):
    inputEntryCount = 0
    inputEntryList = []
    goldEntryCount = 0
    goldEntryList = []


    if inputFilePath:
        with open(inputFilePath, "r") as inputFile:
            for line in inputFile:
                input_entry = line.strip()
                inputEntryList.append(input_entry)
                inputEntryCount += 1
            inputFileSet = set(inputEntryList)
            inputFileSetCount = len(inputFileSet)

            print("********** InputFile **********")
            print("*** The list of deduped entries in inputFile: {}".format(inputFileSet))
            print("*** The number of deduped inputFile: {}".format(inputFileSetCount))
      
            print("*** The list of inputEntry (non-deduped): {}".format(inputEntryList))
            print("*** The number of inputEntry (non-deduped): {}".format(inputEntryCount))

    if goldFilePath:
        with open(goldFilePath, "r") as goldFile:
            for line in goldFile:
                gold_entry = line.strip()
                goldEntryList.append(gold_entry)
                goldEntryCount += 1
                # goldFileSet = set(goldFile)
            # print("*** The list of goldFileSet: {}".format(goldFileSet))
            print("********** GoldFile **********")
            print("*** The list of goldEntry (duplicates not removed): {}".format(goldEntryList))
            print("*** The number of goldEntry (duplicates not removed): {}".format(goldEntryCount))
    

def DuplicateCheck(inputFilePath, goldFilePath, inputEntry, inputEntrySet, goldEntryList, goldEntrySet):
    inputFile_duplicateList = []
    inputFile_duplicateCount = 0
    goldFile_duplicateList = []
    goldFile_duplicateCount = 0
    
    if inputFilePath:
        with open(inputFilePath, "r") as inputFile:
            for line in inputFile:
                input_entry = line.strip()
                if input_entry in inputEntrySet:
                    inputFile_duplicateList.append(input_entry)
                    inputFile_duplicateCount += 1
                inputEntrySet.add(input_entry)
            print("********** InputFile_DuplicateCheck  **********")
            print("*** The number of duplicates in inputFile is {}".format(inputFile_duplicateCount))
            print("*** The list of duplicates in inputFile is {}".format(inputFile_duplicateList))
        
    if goldFilePath:
        with open(goldFilePath, "r") as goldFile:
            for line in goldFile:
                gold_entry = line.strip()
                if gold_entry in goldEntrySet:
                    goldFile_duplicateList.append(gold_entry)
                    goldFile_duplicateCount += 1
                goldEntrySet.add(gold_entry)
            print("********** GoldFile_DuplicateCheck **********")
            print("*** The number of duplicates in goldFile is {}".format(goldFile_duplicateCount))
            print("*** The list of duplicates in goldFile is {}".format(goldFile_duplicateList))
               

def punctuationAccuracyCheck(inputFilePath, goldFilePath):
    acceptedPunctuation = [".", "&", "-"]
    NonAcceptedPunctuation = ["?", ",", "!", "@", "#", "$", "%", "^", "*", "(", ")", "+", "~", ":", ";"]
    inputFile_acceptedPunctuationCount = 0
    inputFile_acceptedPunctuationList = []
    inputFile_nonAcceptedPunctuationCount = 0
    inputFile_nonAcceptedPunctuationList = []
    goldFile_acceptedPunctuationCount = 0
    goldFile_acceptedPunctuationList = []
    goldFile_nonAcceptedPunctuationCount = 0
    goldFile_nonAcceptedPunctuationList = []

    if inputFilePath: 
        with open(inputFilePath, "r") as inputFile:
            for line in inputFile:
                for punctuation in acceptedPunctuation:
                    if punctuation in line:
                        inputFile_acceptedPunctuationCount += 1
                        inputFile_acceptedPunctuationList.append(punctuation)
                for punctuation in NonAcceptedPunctuation:
                    if punctuation in line:
                        inputFile_nonAcceptedPunctuationCount += 1
                        inputFile_nonAcceptedPunctuationList.append(punctuation)
            print("********** Punctuation Accuracy Check *********")
            print("*** The number of accepted punctuations in inputFile: {}".format(inputFile_acceptedPunctuationCount))
            print("*** The list of accepted punctuations in inputFile: {}".format(inputFile_acceptedPunctuationList))
            print("*** The number of non-accepted punctuations in inputFile: {}".format(inputFile_nonAcceptedPunctuationCount))
            print("*** The list of non-accepted punctuations in inputFile: {}".format(inputFile_nonAcceptedPunctuationList))
                                   
    if goldFilePath:
        with open(goldFilePath, "r") as goldFile:
            for line in goldFile:
                ### Punctuation accuracy check
                for accepted_punctuation in acceptedPunctuation:
                    if accepted_punctuation in line:
                        goldFile_acceptedPunctuationCount += 1
                        goldFile_acceptedPunctuationList.append(accepted_punctuation)
                for nonAccepted_punctuation in NonAcceptedPunctuation:
                    if nonAccepted_punctuation in line:
                        goldFile_nonAcceptedPunctuationCount += 1
                        goldFile_nonAcceptedPunctuationList.append(nonAccepted_punctuation)
        
            print("*** The number of accepted punctuations in goldFile: {}".format(goldFile_acceptedPunctuationCount))
            print("*** The list of accepted punctuations in goldFile: {}".format(goldFile_acceptedPunctuationList))
            print("*** The number of non-accepted punctuations in goldFile: {}".format(goldFile_nonAcceptedPunctuationCount))
            print("*** The list of non-accepted punctuations in goldFile: {}".format(goldFile_nonAcceptedPunctuationList))


def spacingAccuracyCheck(inputFilePath, goldFilePath):
    inputFile_incorrectSpacingCount = 0
    inputFile_incorrectSpacingList = []
    goldFile_incorrectSpacingCount = 0
    goldFile_incorrectSpacingList = []

    if inputFilePath:
        with open(inputFilePath, "r") as inputFile:
            for line in inputFile:
                line = line.strip()
                match = re.search(r"  ", line)
                if match:
                    inputFile_incorrectSpacingCount += 1
                    inputFile_incorrectSpacingList.append(line)
            print("********** IncorrectSpacing **********")
            print("*** The number of incorrect Spacing in inputFile: {}".format(inputFile_incorrectSpacingCount))
            print("*** The list of incorrect Spacing in inputFile: {}".format(inputFile_incorrectSpacingList))
    if goldFilePath:
        with open(goldFilePath, "r") as goldFile:
            for line in goldFile:
                line = line.strip()
                match = re.search(r"  ", line)
                if match:
                    goldFile_incorrectSpacingCount += 1
                    goldFile_incorrectSpacingList.append(line)
            print("*** The number of incorrect Spacing in goldFile: {}".format(goldFile_incorrectSpacingCount))
            print("*** The list of incorrect Spacing in goldFile: {}".format(goldFile_incorrectSpacingList))


def coverageCheck(inputFilePath, goldFilePath):
    missingGoldFileList = []
    missingGoldFileCount = 0
    goldListInInputFileList = []
    goldListInInputFileCount = 0

    if inputFilePath and goldFilePath:
        inputFileSet = set()
        with open(inputFilePath, "r") as inputFile:
            for line in inputFile:
                inputFileSet.add(line.strip())

        with open(goldFilePath, "r") as goldFile:
            for goldFile_line in goldFile:
                goldFile_line = goldFile_line.strip()

                if goldFile_line in inputFileSet:
                    goldListInInputFileList.append(goldFile_line)
                    goldListInInputFileCount += 1
                else:
                    missingGoldFileList.append(goldFile_line)
                    missingGoldFileCount += 1
                            
            print("********** GoldFile_CoverageCheck **********")
            print("*** The number of goldFile entries in inputFile: {}".format(goldListInInputFileCount))
            print("*** The list of goldFile entries in inputFile: {}".format(goldListInInputFileList))
            print("*** The number of missing GoldFile entries: {}".format(missingGoldFileCount))
            print("*** The list of missing GoldFile entries: {}".format(missingGoldFileList))


def modalityCheck(inputFilePath, goldFilePath):
    inputFile_WrittenOnlyList = []
    inputFile_WrittenOnlyCount = 0
    inputFile_SpokenandWrittenList = []
    inputFile_SpokenandWrittenCount = 0
    inputFile_SpokenOnlyList = []
    inputFile_SpokenOnlyCount = 0
    
    goldFile_WrittenOnlyList = []
    goldFile_WrittenOnlyCount = 0
    goldFile_SpokenandWrittenList = []
    goldFile_SpokenandWrittenCount = 0
    goldFile_SpokenOnlyList = []
    goldFile_SpokenOnlyCount = 0

    spokenOnlyList = ["fabook"]

    if inputFilePath:
        with open(inputFilePath, "r") as inputFile:
            for line in inputFile:
                line = line.strip()
                match_digits = re.findall(r"\d", line)
                match_uppers = re.findall(r"[A-Z]", line)
                match_punctuations = re.findall(r"[~`!@$%^&*()_+=`{}:;\?/><\[\]\"]", line)
                if match_digits:
                    inputFile_WrittenOnlyList.append(line)
                    inputFile_WrittenOnlyCount += 1
                elif match_uppers:
                    inputFile_WrittenOnlyList.append(line)
                    inputFile_WrittenOnlyCount += 1
                elif match_punctuations:
                    inputFile_WrittenOnlyList.append(line)
                    inputFile_WrittenOnlyCount += 1
                elif line in spokenOnlyList:
                    inputFile_SpokenOnlyList.append(line)
                    inputFile_SpokenOnlyCount += 1
                else:
                    inputFile_SpokenandWrittenList.append(line)
                    inputFile_SpokenandWrittenCount += 1

    if goldFilePath:
        with open(goldFilePath, "r") as goldFile:
            for line in goldFile:
                line = line.strip()
                match_digits = re.findall(r"\d", line)
                match_uppers = re.findall(r"[A-Z]", line)
                match_punctuations = re.findall(r"[~`!@$%^&*()_+=`{}:;\?/><\[\]\"]", line)
                if match_digits:
                    goldFile_WrittenOnlyList.append(line)
                    goldFile_WrittenOnlyCount += 1
                elif match_uppers:
                    goldFile_WrittenOnlyList.append(line)
                    goldFile_WrittenOnlyCount += 1
                elif match_punctuations:
                    goldFile_WrittenOnlyList.append(line)
                    goldFile_WrittenOnlyCount += 1
                elif line in spokenOnlyList:
                    goldFile_SpokenOnlyList.append(line)
                    goldFile_SpokenOnlyCount += 1
                else:
                    goldFile_SpokenandWrittenList.append(line)
                    goldFile_SpokenandWrittenCount += 1
        
            print("********** Modality Check **********")
            print("*** The list of WrittenOnly in inputFile: {}".format(inputFile_WrittenOnlyList))
            print("*** The number of WrittenOnly in inputFile: {}".format(inputFile_WrittenOnlyCount))
            print("*** The list of SpokenandWritten in inputFile: {}".format(inputFile_SpokenandWrittenList))
            print("*** The number of SpokenandWritten in inputFile: {}".format(inputFile_SpokenandWrittenCount))
            print("*** The list of SpokenOnly in inputFile: {}".format(inputFile_SpokenOnlyList))
            print("*** The number of SpokenOnly in inputFile: {}".format(inputFile_SpokenOnlyCount))

            print("*** The list of WrittenOnly in goldFile: {}".format(goldFile_WrittenOnlyList))
            print("*** The number of WrittenOnly in goldFile: {}".format(goldFile_WrittenOnlyCount))
            print("*** The list of SpokenandWritten in goldFile: {}".format(goldFile_SpokenandWrittenList))
            print("*** The number of SpokenandWritten in goldFile: {}".format(goldFile_SpokenandWrittenCount))
            print("*** The list of SpokenOnly in goldFile: {}".format(goldFile_SpokenOnlyList))
            print("*** The number of SpokenOnly in goldFile: {}".format(goldFile_SpokenOnlyCount))


inputFiles(args.inputFilePath, args.goldFilePath)
punctuationAccuracyCheck(args.inputFilePath, args.goldFilePath)

inputEntryList = []
inputEntrySet = set()
goldEntryList = []
goldEntrySet = set()
DuplicateCheck(args.inputFilePath, args.goldFilePath, inputEntryList, inputEntrySet, goldEntryList, goldEntrySet)

spacingAccuracyCheck(args.inputFilePath, args.goldFilePath)
coverageCheck(args.inputFilePath, args.goldFilePath)
modalityCheck(args.inputFilePath, args.goldFilePath)