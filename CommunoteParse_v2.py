#Spaghetti code by: David Cleave

import re
import json
import urllib

def main():
    f = open('input.txt', 'r')
    #f = open('shortTextFile.txt', 'r')
    content = f.readlines()
    
    outfile = open('output.txt', 'w')
    
    for line in content:
        data = parseInput(line)
        writeToFile(outfile, data)
       
    outfile.close     
        
def getFormat(filename, fileID):
    filenameArr = filename.split('.')
    if (len(filenameArr) > 1): #if had at least one '.' and last part after the last '.' isn't longer than 4 char
        extension = filenameArr[-1].lower()
 
    else:
        #extension = scrapeMetaData(fileID)
        extension = 'unknown'
        
    return extension
    
#not being used
def scrapeMetaData(fileID): #google doc docs don't have a mimeType
    page = urllib.urlopen('https://drive.google.com/file/d/' + fileID)
    html = page.read()
    chunked = re.match(r'(mimeType)',html)
    mimeType = re.search(r'([a-z]{1,}\\/[a-z]{1,})', chunked, re.IGNORECASE).group()
    print mimeType
    

def getMatType(filename):
    #FindAll to cover straight forward types that have consistent spelling
    typeTagsRaw = re.findall('quiz|tutorial|assignment', filename, re.IGNORECASE)
    for tag in typeTagsRaw:
        return tag.lower()

    #Tags as a NOTE
    noteTag = re.search('note|lecture|review', filename, re.IGNORECASE)
    if (noteTag is not None):
        return "note"

    #Tags as NOTE if contains 'chapter' but isn't already tagged as a QUIZ
    chapterNoteTag = re.search('chapter|chap', filename, re.IGNORECASE)
    if (chapterNoteTag is not None):
        return "note"

    #Tags as a CHEATSHEET
    noteTag = re.search('cheat|crib|summary|formula', filename, re.IGNORECASE)
    if (noteTag is not None):
        return "cheatsheet"
    
    #Tags as EXAM. FindAll exam would find 'example' and marks as EXAM
    examTag = re.search('exam', filename, re.IGNORECASE)
    if (examTag is not None):
        return "exam"

    #Tags as TEST. #Has cases where tags midterm practice questions as TEST
    testTag = re.search('test|midterm', filename, re.IGNORECASE)
    if (testTag is not None):
        return "test"
    
    # default is note
    return "note"


def getSol(filename):
    # Tags as a SOLUTION
    solutionTag = re.search('solution|soln|answer', filename, re.IGNORECASE)
    if (solutionTag is not None):
        return True
    else:
        return False


def getYear(filename):
    yearSearch = re.search('[0-9]{4}', filename)
    if (yearSearch is not None):
        return yearSearch.group()
    else:
        return ""

def getSemester(filename):
    #FindAll to cover straight forward types that have consistent spelling
    tags = re.findall('winter|spring|summer|fall', filename, re.IGNORECASE)
    for tag in tags:
        if (tag == "winter"):
            return 0
        elif (tag == "spring"):
            return 1
        elif (tag == "summer"):
            return 2
        elif (tag == "fall"):
            return 3
        
    return 0

def getVersion(filename):
    tags = re.findAll('v([A-Z]+|\d+)', filename) #vA, v3, etc.

def getDriveMetaData():
    file_id = '0BwwA4oUTeiV1UVNwOHItT0xfa2M'
    request = drive_service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print "Download %d%%." % int(status.progress() * 100)
    # TODO: get mimetype
    # TODO: if drive file, use open office standards
    return {}

def uploadS3():
    print 'boom'

def parseInput(input):
    output = {}

    lineList = re.split("\t", input)
    index = lineList[0]
    text = lineList[4]
    fileID = lineList[6].split('?id=')[1]

    output['facilty'] = lineList[1]
    
    output['code'] = lineList[3]

    output['format'] = getFormat(text, fileID)
    
    output['description'] = text

    output['solution'] = getSol(text)
    
    # TODO: change tests depending on the type
    output['type'] = getMatType(text)
    
    output['year'] = getYear(text)
    
    output['semesterId'] = getSemester(text)
        
    output['S3OrginalLink'] = lineList[6].replace('\n','')
    
    return output

def writeToFile(outfile, data):
    outfile.write(json.dumps(data)+'\n'*2)

main()
