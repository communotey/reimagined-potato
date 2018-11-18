#Spaghetti code by: David Cleave

#*unknowns are actually google docs and odt marked are docs with no "." while i wanted it to be the other way around

import re
import json
import urllib2

import requests
from google.oauth2 import service_account
from apiclient import errors
from apiclient.discovery import build


def main():
    SCOPES = ['https://www.googleapis.com/auth/drive']
    SERVICE_ACCOUNT_FILE = 'G:\Documents\Coding\Webscraping\MacEng15\private\service.json'
    credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('drive', 'v2', credentials=credentials)

    f = open('input.txt', 'r')
    #f = open('shortTextFile.txt', 'r')
    content = f.readlines()
    
    outfile = open('output.txt', 'w')
    outfileDNE = open('DNE.txt', 'w')
    outfileDenied = open('denied.txt', 'w')
    
    for line in content:
        line = line.rstrip() #remove trailing whitespace
        data = parseInput(service, line)
        writeToFile(outfile, data)

        if data['format'] == 'DNE':
            writeOther(outfileDNE, data)
        elif data['format'] == 'denied':
            writeOther(outfileDenied, data)
       
    outfile.close
    outfileDNE.close
    outfileDenied.close     
    print "Done!"


def getFormat(service, fileID):
    try:
        #use the API to get the file type if it is a FILE not a gdoc
        file = service.files().get(fileId=fileID).execute()
        format = file['fileExtension'].lower()
        uploadDate = file['createdDate'] #RFC 3339 format
        
        if (format == ''): #to handle like one case.. may or may not work.. for id = 0BxW61uJyyN8TS3g1V0dwMVhmWEE
            format = 'odt'

    except:
        uploadDate = ""
        #send get request to verify exists and hasn't been deleted
        r = requests.get('https://docs.google.com/open?id=' + fileID)
        print r.status_code
        #if 404 status code then DNE
        if r.status_code == 404:
            format = "DNE"

        #elif OK then it is either a google doc OR don't have access to it
        elif r.status_code == 200:
            gdocString = 'meta property="og:title" content=' #all google docs SHOULD (bit sketchy) have this string in source, while if no access it won't contain this string

            if (gdocString in r.text):
                format = "gdoc"

            else:
                format = "denied"

        #if none of these work then we missed a case and should identify it. Flag as UNKNOWN
        else:
            format = "UNKNOWN"

    return format, uploadDate


def getDescription(filename):
    filenameArr = filename.split('.')
    if (len(filenameArr) > 1): #if had at least one '.' and last part after the last '.' isn't longer than 4 char
        filenameArr.pop(-1).lower()
        description = '-'.join(filenameArr)
 
    else:
        description = filename
        
    return description

    
def getMatType(filename):
    #FindAll to cover straight forward types that have consistent spelling
    typeTagsRaw = re.findall('quiz|tutorial|assignment', filename, re.IGNORECASE)
    for tag in typeTagsRaw:
        return tag.lower()

    #Tags as a NOTE
    noteTag = re.search('note|lecture|review|chapter|chap|ch|module|week', filename, re.IGNORECASE)
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
    tag = re.search('v([A-Z]|\d+)', filename, re.IGNORECASE) #vA, v3, etc. OR Test 1a, Test 1b
    if (tag is not None):
        version = tag.groups()[0].upper()
        return version
        
    tag = re.search('(test|quiz|midterm|assignment|lecture|note|chapter|chap|ch|module|week)(\s|_)?(\d{1,2})([A-Z]?)($|\s|_)', filename, re.IGNORECASE)
    if (tag is not None):
        version = tag.groups()[3].upper()
        return version

    return ""


def getVolume(filename):
    tag = re.search('(test|quiz|midterm|assignment|lecture|note|chapter|chap|ch|module|week)(\s|_)?(\d{1,2})([A-Z]?){0,}($|\s|_)', filename, re.IGNORECASE)
    if (tag is not None):
        version = str(int(tag.groups()[2].upper()))
        return version
    
    else:
        return ""
    

def parseInput(service, input):
    output = {}
    
    lineList = re.split("\t", input)
    index = lineList[0]
    text = lineList[4]
    fileID = lineList[6].split('?id=')[1]
    
    output['code'] = lineList[1] + ' ' + lineList[3]

    output['description'] = getDescription(text)

    output['format'] = getFormat(service, fileID)[0]
    output['dateCreated'] = getFormat(service, fileID)[1]

    output['solution'] = getSol(text)
    
    # TODO: change tests depending on the type #what does this mean?
    output['type'] = getMatType(text)
    
    output['year'] = getYear(text)
    
    output['semesterId'] = getSemester(text)

    output['version'] = getVersion(output['description'])

    output['volume'] = getVolume(output['description'])
        
    output['fileID'] = fileID

    print index + " : " + output['format']
    
    return output


def writeToFile(outfile, data):
    outfile.write(json.dumps(data))
    outfile.write('\n')

def writeOther(outfile, data):
    shortData = {'code':data['code'],
                'title':data['description'],
                'format':data['format'],
                'link':'https://docs.google.com/open?id=' + data['fileID']
                }

    outfile.write(json.dumps(shortData))
    outfile.write('\n')
main()