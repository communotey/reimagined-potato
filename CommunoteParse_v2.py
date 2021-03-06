#Spaghetti code by: David Cleave

import re
import json
import urllib2

import requests
from google.oauth2 import service_account
from apiclient import errors
from apiclient.discovery import build

from dateutil import parser
import calendar


def main():
    base_path = '/home/ec2-user/environment/reimagined-potato/'
    SCOPES = ['https://www.googleapis.com/auth/drive']
    #SERVICE_ACCOUNT_FILE = 'G:\\Documents\\Coding\\Webscraping\\MacEng15\\private\\creds\\service.json' #CHANGE
    SERVICE_ACCOUNT_FILE = '/home/ec2-user/environment/reimagined-potato/creds/service.json'
    credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('drive', 'v2', credentials=credentials)

    f = open(base_path + 'input.txt', 'r')
    #f = open(base_path + 'shortTextFile.txt', 'r')
    content = f.readlines()
    
    outfile = open(base_path + 'output.txt', 'w')
    outfileDNE = open(base_path + 'DNE.txt', 'w')
    outfileDenied = open(base_path + 'denied.txt', 'w')
    
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


def getMetaData(service, fileID):
    
    try:
        #use the API to get the file type if it is a FILE not a gdoc
        file = service.files().get(fileId=fileID).execute()
        format = file['fileExtension'].lower()
        uploadDate = timestamp(file['createdDate']) #RFC 3339 format
        filename = file['title']
        
        if (format == ''): #to handle like one case.. may or may not work.. for id = 0BxW61uJyyN8TS3g1V0dwMVhmWEE
            format = 'odt'

    except:
        #if it is a gdoc or there was an error
        filename = ""
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

    return format, uploadDate, filename


def getDescription(filename):
    filename = filename.replace('/', ' ')
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
    return "3" #TODO: Update this to scrape based on the course if can't be parsed?


def getVersion(filename):    
	lastChunk = filename.split()[-1]

	tag = re.search('(v)([^\s]+)', lastChunk, re.IGNORECASE)
	if (tag is not None):
		version = tag.groups()[1].upper()
		return version

	return ""


def getVolume(filename):
    tag = re.search('(test|quiz|midterm|assignment|lecture|note|chapter|chap|ch|module|week)(\s|_)?(\d{1,2})([A-Z]?){0,}($|\s|_)', filename, re.IGNORECASE)
    if (tag is not None):
        volume = str(int(tag.groups()[2].upper()))
        return volume
    
    else:
        return ""
    

def parseInput(service, input):
    output = {}
    
    #Would need to first scrape the description (file name) from google drive
    #and use that in most of the functions rather than the whole string of text
    #change from text to desciption for: getSol, getMatType, getYear, getSemester
    #keep in mind google docs won't work so if gdoc then use the input.txt file name as the description

    lineList = re.split("\t", input)
    index = lineList[0]
    text = lineList[4]
    fileID = lineList[6].split('?id=')[1]
    
    output['code'] = lineList[1] + ' ' + lineList[3]

    

    output['format'], output['date'], filename = getMetaData(service, fileID)


    #if got filename from drive api
    if filename != "":
        description = getDescription(filename)

    #else couldn't get filename from drive api
    else:
        description = getDescription(text) #change this function to get from api, not input.txt

    
    #Set date to the Jan 2nd of the parsed year and converted to a timestamp\
    output['year'] = getYear(description)
    if output['year'] != "":
    	output['date'] = str(timestamp('Jan 2 ' + output['year']))

    output['description'] = description
        
    output['solution'] = getSol(description)
    
    # TODO: change tests depending on the type #what does this mean?
    output['type'] = getMatType(description)
    
    output['semesterId'] = getSemester(description)

    output['version'] = getVersion(description)

    output['volume'] = getVolume(description)
        
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


def timestamp(isoDate):
	timeObj = parser.parse(isoDate)
	timestamp = calendar.timegm(timeObj.timetuple())
	return timestamp

main()