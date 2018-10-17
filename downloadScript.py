#Script used to download files from google drive to computer
import urllib2
import json
import os
import requests


#Convert docx to google doc
def googleDocify(OGfileID):
    #get the key by scraping it from the webpage. easy.
    #? use the OGfileId and the key to send a POST request to have it converted
    #??? use the response to get the ID of the new google doc that's been created

    #example ID of google doc
    #1-Q7okxyMGocqpiy2BP_zyROJeh-AuMy2P4C7OUJnJwo
    #example download link for ODT as used in previous code for downloading google docs:
    #https://docs.google.com/document/export?format=odt&id=1-Q7okxyMGocqpiy2BP_zyROJeh-AuMy2P4C7OUJnJwo

    key = 'AIzaSyDVQw45DwoYh632gvsP5vPDqEKvb-Ywnb8'
    #reqURL = "https://clients6.google.com/drive/v2internal/files/" + OGfileID + "/copy
    reqURL = "https://clients6.google.com/drive/v2internal/files/0BxW61uJyyN8TaV82MWtiZ2JQemM/copy"

    params = {'convert':'true', 'supportsTeamDrives':'true', 'fields':'id,kind,mimeType', 'key':key, 'alt':'json'} #is this right?
    headers = dict(authorization = 'removed for security')
    cookies = dict(__utma = 'removed for security'

    response = requests.post(reqURL, params=params, headers=headers, cookies=cookies)
    print response.status_code
    print
    print response.request.headers
    print
    print response.text

    
    
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
        downloadFormat = getDownloadFormat(fileFormat)
        print downloadFormat
        
        """
        if (downloadFormat == 'odt') or (downloadFormat == 'ods'):
            downloadLink = 'https://docs.google.com/document/export?format=' + downloadFormat + '&id=' + fileID + '&includes_info_params=true'
        else:
            downloadLink = 'https://drive.google.com/uc?authuser=0&id=' + fileID + '&export=download'
        """

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
        downloadFormat = 'ods'

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



