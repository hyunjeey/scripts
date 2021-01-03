# This script is designed for the following steps of data curation: 
# 1. Create concatFile1 by concatenating two source files
# 2. Create dedupedFile1 by removing exact duplicates
# 2. Create random_variant_original.txt by concatenating 80 entries from dedupedFile1 and 20 entries from variantFile.txt
# 3. Create concatGoldFile.txt by concatenating random_variant_original.txt and GoldFile.txt
# 4. Create finalDedupedFile by removing duplicates from concatGold.txt
# 5. Generates stats of each of the above-listed output files

# Author: Hyunjee Yoon
# Date: 01/01/2020
# Usage: python3 codes_for_dataCuration.py <sourceFile1Path> <sourceFile2Path> --goldFile = <goldFilePath> --variantFile = <variantFilePath>
# Example: python3 codes_for_dataCuration.py sourceFile1.txt sourceFile2.txt --goldFile = goldFile.txt --variantFile = variantFile.txt

import argparse
import math
import random
import os

parser = argparse.ArgumentParser()
parser.add_argument("sourceFile1Path", help="Path to the sourceFile1")
parser.add_argument("sourceFile2Path", help="Path to the sourceFIle2")
parser.add_argument("--goldFile", help="Path to the goldFile")
parser.add_argument("--variantFile", help="Path to the variantFile")
args = parser.parse_args()

# Concatenates two source files (SourceFile1 and SourceFile2)
def concatSourceFiles(sourceFile1Path, sourceFile2Path):
    concatFile1 = open('concatFile1.txt', 'w', newline='')

    if sourceFile1Path:
        with open(sourceFile1Path, "r") as sourceFile1:
            for line in sourceFile1:
                concatFile1.write(line)
            concatFile1.write("\n")

    if sourceFile2Path:
        with open(sourceFile2Path, "r") as sourceFile2:
            for line in sourceFile2:
                concatFile1.write(line)
            concatFile1.write('\n')
                

# Removes exact duplicates
def removeDuplicate(concatFile1Path, concatFile1List, concatFileSet):
    concatFile1_duplicateList = []
    concatFile1_duplicateCount = 0
    dedupedFile1Count = 0

    if concatFile1Path:
        with open(concatFile1Path, "r") as beforeDeduped:
            with open('dedupedFile1.txt', 'w', newline='') as dedupedFile1:
                for line in beforeDeduped:
                    # beforeDedupedEntry = line.strip()
                    if line in concatFile1Set:
                        concatFile1_duplicateList.append(line)
                        concatFile1_duplicateCount += 1
                    concatFile1Set.add(line)
                for line in concatFile1Set:
                    dedupedFile1.write(line)

        with open("dedupedFile1.txt", "r") as dedupedFile1:
            for line in dedupedFile1:
                dedupedFile1Count += 1
         
        print("*** The list of unique entries in the concatenated list of sourceFile1 and sourceFile2: {}".format(concatFile1Set))
        print("*** The number of unique entries in the concatenated list of sourceFile1 and sourceFile2: {}".format(dedupedFile1Count))
        print("*** The list of duplicates in the concatenated list of sourcedFile1 and sourcedFile2: {}".format(concatFile1_duplicateList))
        print("*** The number of duplicates in the concatenated list of sourcedFile1 and sourcedFile2: {}".format(concatFile1_duplicateCount))


# 100 entries in File2 which contains 20 variants and 80 dedupedFile1 entries
def random_variant_original(originalFilePath, variantFilePath):
    if originalFilePath:
        with open(originalFilePath, "r", newline='') as originalFile:
            originalFileList = list(originalFile)
            # print(originalFileList)
        with open("random_variant_original.txt", "w", newline='') as random_variant_original:
            for r in random.sample(originalFileList, 80):
                random_variant_original.write(r)

    if variantFilePath:
        with open(variantFilePath, "r", newline='') as variantFile:
            variantFileList = list(variantFile)
        with open("random_variant_original.txt", 'a', newline='') as random_variant_original:
            for r in random.sample(variantFileList, 20):
                random_variant_original.write(r)


# Concatenates random_variant_original.txt to goldFile.txt
def concatGoldFile(randomVariantOriginalPath, goldPath):
    if randomVariantOriginalPath:
        with open(randomVariantOriginalPath, "r") as randomVariantOriginal:
            concatGoldFile = open('concatGoldFile.txt', 'w', newline='')
            for line in randomVariantOriginal:
                concatGoldFile.write(line)

    if goldPath:
        with open(goldPath, "r") as goldFile:
            with open("concatGoldFile.txt", 'a', newline=''):
                for line in goldFile:
                    concatGoldFile.write(line)


# Removes exact duplicates of concatGoldFile.txt
def removeDuplicate_concatGold(concatGoldFilePath, concatGoldFileList, concatGoldFileSet):
    concatGoldFile_duplicateList = []
    concatGoldFile_duplicateCount = 0
    dedupedConcatGoldFileCount = 0

    if concatGoldFilePath:
        with open(concatGoldFilePath, "r") as beforeDeduped:
            finalDedupedFile = open('finalDedupedFile.txt', 'w', newline='')
            for line in beforeDeduped:
                if line in concatGoldFileSet:
                    concatGold = line.strip()
                    concatGoldFile_duplicateList.append(concatGold)
                    concatGoldFile_duplicateCount += 1
                concatGoldFileSet.add(line)
            for line in concatGoldFileSet:
                finalDedupedFile.write(line)

        print("********** finalDedupedFile.txt is the final output data file**********")
        print("*** The list of unique entries in concatGoldFile (random variants+original+goldFile): {}".format (concatGoldFileSet))
        print("*** The number of unique entries in concatGoldFile (random variants+original+goldFile): {}".format(dedupedConcatGoldFileCount))
        print("*** The list of duplicates in concatGoldFile (random variants+original+goldFile): {}".format(concatGoldFile_duplicateList))
        print("*** The number of duplicates in concatGoldFile (random variants+original+goldFile): {}".format(concatGoldFile_duplicateCount))
           

concatSourceFiles(args.sourceFile1Path, args.sourceFile2Path)

concatFile1List = []
concatFile1Set = set()
removeDuplicate("concatFile1.txt", concatFile1List, concatFile1Set)

random_variant_original("dedupedFile1.txt", "variantFile.txt")

concatGoldFile("random_variant_original.txt", "goldFile.txt" )

concatGoldFileList = []
concatGoldFileSet = set()
removeDuplicate_concatGold("concatGoldFile.txt", concatGoldFileList, concatGoldFileSet)