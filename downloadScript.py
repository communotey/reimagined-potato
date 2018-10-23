#Script used to download files from google drive to computer
import urllib2
import json
import os
import requests

#from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

#could the problem be that it needs the file key to be included in the request?

def googleDocify(OGfileID):
    #///START - quick start sample code///
    
    # If modifying these scopes, delete the file token.json.
    SCOPES = 'https://www.googleapis.com/auth/drive'

    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('drive', 'v3', http=creds.authorize(Http()))\
              
    # Call the Drive v3 API
    results = service.files().list(
        pageSize=10, fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])

    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print(u'{0} ({1})'.format(item['name'], item['id']))

    #///END - quick start sample code///
            

    APIKey = ""
    secret = ""
    clientID = ""

    reqURL = "https://www.googleapis.com/drive/v2/files/" + OGfileID + "/copy"
    params = {"convert":"true", "supportsTeamDrives":"true", "fields":"id,kind,mimeType", "alt":"json", "key":APIKey}   
    
    response = requests.post(reqURL, params=params)
                   
    print response.text

    #get ID from response
    #return ID from the response

    
#test with a docx file    
googleDocify('0BxW61uJyyN8TaV82MWtiZ2JQemM')


 

    #https://drive.google.com/file/d/0BxW61uJyyN8TaV82MWtiZ2JQemM/view
    #the download link isn't working for this one docx to odt
    #can't download docx as ODT. need to open as google doc then can download but it assigns it a new ID for the google doc version
    #can convert the document by getting the key from scraping _initProjector from https://drive.google.com/file/d/0BxW61uJyyN8TaV82MWtiZ2JQemM/view and then once have the key
    #use POST: https://clients6.google.com/drive/v2internal/files/0BxW61uJyyN8TaV82MWtiZ2JQemM/copy?convert=true&supportsTeamDrives=true&fields=id,kind,mimeType&key=AIzaSyDVQw45DwoYh632gvsP5vPDqEKvb-Ywnb8&alt=json
    #when clicking convert to google drive also has the request url: https://clients6.google.com/drive/v2internal/files/1qatRFo_F2roKK9oZ7EJ6Y3tB5MsJ-xXo78NFITDkxNA/authorize?&appId=619683526622&supportsTeamDrives=true&key=AIzaSyDVQw45DwoYh632gvsP5vPDqEKvb-Ywnb8
    #which has the ID in the request url which is the ID of the google doc that it has been converted to. It's actually the 1qatRFo_... part thats after /files/...
    #
    
def main():
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

        #TODO: there are a few files where fileFormat already == 'odt'. In this case it should be downloaded as is using dataFormat["format"] instead of trying to convert
            
        downloadFormat = getDownloadFormat(fileFormat)
        
        """
        if (downloadFormat == 'odt') or (downloadFormat == 'odp'):
            downloadLink = 'https://docs.google.com/document/export?format=' + downloadFormat + '&id=' + fileID + '&includes_info_params=true'
        else:
            downloadLink = 'https://drive.google.com/uc?authuser=0&id=' + fileID + '&export=download'
        """

        #temp use this as the downloadLink rather than the above code
        downloadLink = 'https://drive.google.com/uc?authuser=0&id=' + fileID + '&export=download'
        
        print downloadLink
        
        #check fileFormat then handle download differently if doc then odt or whatever
        fileName = os.path.dirname(os.path.abspath(__file__)) + '/downloads/' + fileDesc + '.' + fileFormat
        print fileName
        #From user: PabloG https://stackoverflow.com/questions/22676/how-do-i-download-a-file-over-http-using-python
        downloadFile(downloadLink, fileName)
        print 'done'


def getDownloadFormat(fileFormat):
    if (fileFormat == 'doc') or (fileFormat == 'docx') or fileFormat == '':
        downloadFormat = 'odt'
        
    elif (fileFormat == 'ppt'):
        downloadFormat = 'odp'
    
    else:
        downloadFormat = fileFormat

    return downloadFormat

    
def downloadFile(downloadLink, fileName):
        u = urllib2.urlopen(downloadLink)
        f = open(fileName, 'wb')

        block_sz = 8192
        while True:
            buffer = u.read(block_sz)
            if not buffer:
                break
            f.write(buffer)
        f.close()











    

