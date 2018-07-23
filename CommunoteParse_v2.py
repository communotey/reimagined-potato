#Spaghetti code by: David Cleave

import re #REEEEEEEEEEEEEEEEEEEEEEE

def main():
    f = open('output1.txt', 'r')
    #f = open('shortTextFile.txt', 'r')
    #f = open('testFile1.txt', 'r')
    content = f.readlines()


    for line in content:
        lineList = re.split("\t", line)
        index = lineList[0]
        facilty = lineList[1]
        courseCode = lineList[3]
        originalTitle = lineList[4]
        fileURL = lineList[6]
        
        typeTags = getMatType(originalTitle)
        year = getYear(originalTitle)
        isPDF = checkIfPDF(originalTitle)

        #Just printing the files
        if (isPDF):
            print str(typeTags) + "\t"*(3-len(typeTags)) + year + "\t" + originalTitle
            
        
def checkIfPDF(originalTitle):
    if ((re.search('pdf?$', originalTitle, re.IGNORECASE)) is not None):
        return True
    else:
        return False

def getMatType(originalTitle):
    allTypeTags = []
    #FindAll to cover straight forward types that have consistent spelling
    typeTagsRaw = re.findall('quiz|tutorial|assignment', originalTitle, re.IGNORECASE)
    for tag in typeTagsRaw:
        allTypeTags.append(tag.upper())

    #Tags as EXAM. FindAll exam would find 'example' and marks as EXAM
    examTag = re.search('exam', originalTitle, re.IGNORECASE)
    if (examTag is not None):
        allTypeTags.append("EXAM")

    #Tags as TEST. #Has cases where tags midterm practice questions as TEST
    testTag = re.search('test|midterm', originalTitle, re.IGNORECASE)
    if (testTag is not None):
        allTypeTags.append("TEST")
    
    #Tags as a NOTE
    noteTag = re.search('note|lecture|review', originalTitle, re.IGNORECASE)
    if (noteTag is not None):
        allTypeTags.append("NOTE")

    #Tags as NOTE if contains 'chapter' but isn't already tagged as a QUIZ
    chapterNoteTag = re.search('chapter|chap', originalTitle, re.IGNORECASE)
    if ((chapterNoteTag is not None) and not('QUIZ' in allTypeTags) and not('NOTE' in allTypeTags)):
        allTypeTags.append("NOTE")

    #Tags as a CHEATSHEET
    noteTag = re.search('cheat|crib|summary|formula', originalTitle, re.IGNORECASE)
    if (noteTag is not None):
        allTypeTags.append("NOTE")
    
    
    #Tags as a SOLUTION
    solutionTag = re.search('solution|soln|answer', originalTitle, re.IGNORECASE)
    if (solutionTag is not None):
        allTypeTags.append("SOLUTION")
        
    return allTypeTags


def getYear(originalTitle):
    yearSearch = re.search('[0-9]{4}', originalTitle)
    if (yearSearch is not None):
        return yearSearch.group()
    else:
        return ""

main()
    
        
