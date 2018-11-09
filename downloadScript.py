#Script used to download files from google drive to computer
import urllib2
import json
import os
import io
import requests
from google.oauth2 import service_account
from apiclient import errors
from apiclient.discovery import build
from apiclient.http import MediaIoBaseDownload


def main():
    SCOPES = ['https://www.googleapis.com/auth/drive']
    SERVICE_ACCOUNT_FILE = 'G:\Documents\Coding\Webscraping\MacEng15\private\service.json'
    credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('drive', 'v2', credentials=credentials)

    #open and read output.txt
    #f = open('output.txt','r')
    dataFile = open('outputShort.txt','r') #using outputShort cause don't want to download all the files everytime i test it.
    content = dataFile.readlines()

    #for each line read data from output file
    for line in content:
        data = json.loads(line)
        fileID = data["fileID"]
        fileDesc = data["description"]
        fileFormat = data["format"]
        courseCode = data["code"]

        print fileID
        
        #Make new folder for course if doesn't exist
        fileDir = os.path.dirname(os.path.abspath(__file__)) + '/downloads/' + courseCode
        if (not os.path.exists(fileDir)):
            os.makedirs(fileDir)
        
        #convert from doc or docx to google doc if needed
        if (fileFormat == 'doc') or (fileFormat == 'docx'):
            GDoc = convertFile(service, fileID, fileDesc) #convert to GDoc
            fileID = GDoc['id'] #fileID of new GDoc
            mimeType = 'application/vnd.oasis.opendocument.text' #mimeType for odt
            filePath = fileDir + '/' + fileDesc + '.odt' #directory for odt download
            isGDoc = True

        #TODO: odp download is 90% corrupt even when doing it manually without using the API. Could export as PDF instead maybe. or just keep as ppt
        elif (fileFormat == 'ppt'):
            GDoc = convertFile(service, fileID, fileDesc) #convert to GDoc
            fileID = GDoc['id'] #fileID of new GDoc
            mimeType = 'application/vnd.oasis.opendocument.presentation' #mimeType for odp 
            #mimeType = 'application/pdf'
            filePath = fileDir + '/' + fileDesc + '.odp' #directory for odt download
            isGDoc = True
            
        #else if already a google doc (doesn't need conversion)
        elif (fileFormat == 'gdoc'):
            mimeType = 'application/vnd.oasis.opendocument.text' #mimeType for odt
            filePath = fileDir + '/' + fileDesc + '.odt'
            isGDoc = True
            
            
        else:
            filePath = fileDir + '/' + fileDesc + '.' + fileFormat
            mimeType = None #can you pass None for mime type if don't want to specify it?
            isGDoc = False

        #Download File
        exportFile(service, fileID, filePath, mimeType, isGDoc)   



def convertFile(service, origin_file_id, copy_title):
  copied_file = {'title': copy_title}
  try:
    return service.files().copy(fileId=origin_file_id, body=copied_file, convert='true').execute()
  except errors.HttpError, error:
    print 'An error occurred: %s' % error
  return None


def exportFile(service, fileID, fileName, mimeType, isGDoc):
    fh = io.FileIO(fileName, 'wb')
    if (isGDoc):
        request = service.files().export_media(fileId=fileID, mimeType=mimeType)
    else:
        request = service.files().get_media(fileId=fileID)
        
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print "Download %d%%." % int(status.progress() * 100)





main()





    

