#Spaghetti code by: David Cleave

import re #REEEEEEEEEEEEEEEEEEEEEEE

def main():
    f = open('output1.txt', 'r')
    #f = open('shortTextFile.txt', 'r')
    #f = open('testFile1.txt', 'r')
    content = f.readlines()


    for line in content:
        data = parseInput(line)
        if (data.format is not None):

    #Just printing the files
            print str(typeTags) + "\t"*(3-len(typeTags)) + data.dateCreated + "\t" + originalTitle
            
        
def getFormat(filename):
    sections = re.split('.')
    extension = sections[len(sections) - 1]

    if (extension is not None):
        return extension
    else:
        return False

def getMatType(filename):
    words = filename.split(' ')
    #FindAll to cover straight forward types that have consistent spelling
    typeTagsRaw = re.findall('quiz|tutorial|assignment', originalTitle, re.IGNORECASE)
    for tag in typeTagsRaw:
        return tag.lower()

    #Tags as EXAM. FindAll exam would find 'example' and marks as EXAM
    examTag = re.search('exam', originalTitle, re.IGNORECASE)
    if (examTag is not None):
        return "exam"

    #Tags as TEST. #Has cases where tags midterm practice questions as TEST
    testTag = re.search('test|midterm', originalTitle, re.IGNORECASE)
    if (testTag is not None):
        return "test"
    
    #Tags as a NOTE
    noteTag = re.search('note|lecture|review', originalTitle, re.IGNORECASE)
    if (noteTag is not None):
        return "note"

    #Tags as NOTE if contains 'chapter' but isn't already tagged as a QUIZ
    chapterNoteTag = re.search('chapter|chap', originalTitle, re.IGNORECASE)
    if ((chapterNoteTag is not None) and not('QUIZ' in allTypeTags) and not('NOTE' in allTypeTags)):
        return "note"

    #Tags as a CHEATSHEET
    noteTag = re.search('cheat|crib|summary|formula', originalTitle, re.IGNORECASE)
    if (noteTag is not None):
        return "cheatsheet"
    
    # default is note
    return "note"

def getSol(filename):
    # Tags as a SOLUTION
    solutionTag = re.search('solution|soln|answer', originalTitle, re.IGNORECASE)
    if (solutionTag is not None):
        return true
    else:
        return false


def getYear(originalTitle):
    yearSearch = re.search('[0-9]{4}', originalTitle)
    if (yearSearch is not None):
        return yearSearch.group()
    else:
        return ""

def getDriveMetaData():
    return {}

def uploadS3():
    print 'boom'

def parseInput(input):
    
    output = {}

    lineList = re.split("\t", input)
    index = lineList[0]

    output['facilty'] = lineList[1]
    output['code'] = lineList[3]

    # TODO: get format from Google Drive API
    # output['format'] = getFormat(lineList[4])
    output['format'] = 'link'
    text = lineList[4].split('.')
    if (len(text)>1):
        text.pop()
    output['description'] = " ".join(text)
    words = text.split(' ')
    output['S3OrginalLink'] = lineList[6]
    
    typeTags = getMatType(originalTitle)
    year = getYear(originalTitle)

    return output

main()
    
        
