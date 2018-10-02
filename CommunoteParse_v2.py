#Spaghetti code by: David Cleave

import re #REEEEEEEEEEEEEEEEEEEEEEE

def main():
    #f = open('output1.txt', 'r')
    f = open('shortTextFile.txt', 'r')
    #f = open('testFile1.txt', 'r')
    content = f.readlines()


    for line in content:
        data = parseInput(line)
        #if (data.format is not None):

    #Just printing the files
        #print str(typeTags) + "\t"*(3-len(typeTags)) + data.dateCreated + "\t" + filename
            
        
def getFormat(filename):
    sections = re.split('.')
    extension = sections[len(sections) - 1]

    if (extension is not None):
        return extension
    else:
        return False

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

    output['facilty'] = lineList[1]
    output['code'] = lineList[3]

    
    # $Type $Volume? $YearCreated $Semester? v$Volume? $Solution?
    textArr = lineList[4].split('.')
    if (len(textArr)>1):
        output['format'] = textArr[-1] #risky in the case that its a google doc with a '.' in the name
        textArr.pop()
    else:
        # TODO: get format from Google Drive API
        output['format'] = 'google doc or similar' #if there is no '.' meaning no file extension in name meaning its a google doc or google word doc etc. could determine by js: document.getElementById("drive-active-item-info").innerText

    # in case for whatever reason there are multiple periods, convert to dashes
    text = "-".join(textArr)
    output['description'] = text

    # turn the remaining string into an array
    words = text.split(' ')

    output['solution'] = getSol(text)
    
    # TODO: change tests depending on the type
    output['type'] = getMatType(text)
    
    year = getYear(text) #should it be text or words?
    
    output['semesterId'] = getSemester(text)
        
    output['S3OrginalLink'] = lineList[6]

    #print output

    return output

main()
