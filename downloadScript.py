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
	SERVICE_ACCOUNT_FILE = 'G:\\Documents\\Coding\\Webscraping\\MacEng15\\private\\creds\\service.json' #//CHANGE
	credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
	service = build('drive', 'v2', credentials=credentials)

	print "Remember to clear downloads.log if doing a fresh download and want all files to be redownloaded."
	print "If log is cleared, delete the downloaded files too."

	#open and read output.txt

	dataFile = open('output.txt','r')
	#dataFile = open('outputShort.txt','r') #using outputShort cause don't want to download all the files everytime i test it.

	downloadLog = open('downloads.log', 'r')
	downloads = downloadLog.read()
	downloadLog.close()
	downloadLog = open('downloads.log', 'a')
	content = dataFile.readlines()

	#for each line read data from output file
	count = 0
	for line in content:
		count += 1
		data = json.loads(line)
		fileID = data["fileID"]
		fileDesc = data["description"]
		fileFormat = data["format"]
		courseCode = data["code"]

		#print fileID

		validFormats = ['doc', 'docx', 'pdf', 'odt', 'gdoc']

		#maybe write to another file to keep note of which were not downloaded

		#download every 50th file for testing
		#if count % 50 == 0:
		if True:
			print str(count) + '/' + str(len(content)) + '\t' + fileID
			if fileID not in downloads:
				if (fileFormat in validFormats):

					#Make new folder for course if doesn't exist
					fileDir = os.path.dirname(os.path.abspath(__file__)) + '\\downloads\\' + courseCode

					if (not os.path.exists(fileDir)):
						os.makedirs(fileDir)
			        
			        #convert from doc or docx to google doc if needed
					if (fileFormat == 'doc'):
						GDoc = convertFile(service, fileID, fileDesc) #convert to GDoc
						fileID = GDoc['id'] #fileID of new GDoc
						mimeType = 'application/vnd.oasis.opendocument.text' #mimeType for odt
						filePath = fileDir + '\\' + fileDesc + '.odt' #directory for odt download
						isGDoc = True

					#else if already a google doc (doesn't need conversion)
					elif (fileFormat == 'gdoc'):
						mimeType = 'application/vnd.oasis.opendocument.text' #mimeType for odt
						filePath = fileDir + '\\' + fileDesc + '.odt'
						isGDoc = True
			            
					#for remaining files: pdf and odt and ppt (no google api conversion)    
					else:
						filePath = fileDir + '\\' + fileDesc + '.' + fileFormat
						mimeType = None
						isGDoc = False

					#Download File
					exportFile(service, fileID, filePath, mimeType, isGDoc)
					downloadLog.write(data["fileID"] + '\n') #writes the fileID of document before conversion



				else:
					print "Skipping download. File format: " + fileFormat
			else:
				print "Skipping download. File already downloaded."
	downloadLog.close
	print "End of download script."


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





    

