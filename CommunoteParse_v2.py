#Spaghetti code by: David Cleave

#*unknowns are actually google docs and odt marked are docs with no "." while i wanted it to be the other way around

import re
import json
import urllib

def main():
    f = open('input.txt', 'r')
    #f = open('shortTextFile.txt', 'r')
    content = f.readlines()
    
    outfile = open('output.txt', 'w')
    
    for line in content:
        line = line.rstrip() #remove trailing whitespace
        data = parseInput(line)
        writeToFile(outfile, data)
       
    outfile.close     
    print "Done!"
        
def getFormatAndDesc(filename, fileID):
    filenameArr = filename.split('.')
    if (len(filenameArr) > 1): #if had at least one '.' and last part after the last '.' isn't longer than 4 char
        extension = filenameArr.pop(-1).lower()
        description = '-'.join(filenameArr)
 
    else:
        extension = scrapeGDocType(fileID) #TODO: there are some .doc files that don't have a '.' in the desc so thinks its a gdoc when its not
        print "No dot for fileID: " + fileID + "\t marked as format: " + extension
        description = filename
        
        
    return description, extension
    

def scrapeGDocType(fileID):
    page = urllib.urlopen('https://docs.google.com/document/d/' + fileID)
    html = page.read()
    
    odtTag = re.search(r'(itemtype=\"http://schema.org/CreativeWork/DocumentObject\")', html)
    if (odtTag is not None):
        return "odt"

    odpTag = re.search(r'(itemtype=\"http://schema.org/CreativeWork/PresentationObject\")', html)
    if (odpTag is not None):
        return "odp"

    odsTag = re.search(r'(itemtype=\"http://schema.org/CreativeWork/SpreadsheetObject\")', html)
    if (odsTag is not None):
        return "ods"

    return "unknown"
        
    
    

def getMatType(filename):
    #FindAll to cover straight forward types that have consistent spelling
    typeTagsRaw = re.findall('quiz|tutorial|assignment', filename, re.IGNORECASE)
    for tag in typeTagsRaw:
        return tag.lower()

    #Tags as a NOTE
    noteTag = re.search('note|lecture|review|chapter|chap', filename, re.IGNORECASE)
    if (noteTag is not None):
        return "note"

    #Tags as a CHEATSHEET
    cheatTag = re.search('cheat|crib|summary|formula', filename, re.IGNORECASE)
    if (cheatTag is not None):
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
        tag = tag.lower()
        if (tag == "winter"):
            return 0
        elif (tag == "spring"):
            return 1
        elif (tag == "summer"):
            return 2
        elif (tag == "fall"):
            return 3
    return ""

def getVersion(filename):
    tags = re.findall('v([A-Z]|\d+)', filename) #vA, v3, etc.
    for tag in tags:
        if (tag is not None):
            return tag
    return ""

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
    
    output['code'] = lineList[1] + ' ' + lineList[3]

    output['description'], output['format'] = getFormatAndDesc(text, fileID)

    output['solution'] = getSol(text)
    
    # TODO: change tests depending on the type #what does this mean?
    output['type'] = getMatType(text)
    
    output['year'] = getYear(text)
    
    output['semesterId'] = getSemester(text)

    output['version'] = getVersion(text)
        
    output['fileID'] = fileID
    
    return output

def writeToFile(outfile, data):
    outfile.write(json.dumps(data))
    outfile.write('\n')

main()
