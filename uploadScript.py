"""File upload script"""
"""Uploads files from local storage to communote via api
with associated data previously parsed and stored in output.txt"""

import json
import requests

#TODO: Script to create new course if doesn't exist
#TODO: Scrape semester, eval number etc in parsing script better.

def main():
    #open output.txt
    #f = open("output.txt")
    f = open("outputShort.txt")
    
    #read data file
    content = f.readlines()

    for line in content:
        print line
        data = json.loads(line)
        #call upload(data)
        upload(data)

def upload(data):
    #determine fileName including format assuming converted docx --> odt etc.
    fileName = getFileName(data)
    
    #send request to communote api with data 
    reqURL = "https://api.communote.net/api/file/new"

    #adjust any of the data if needed before passing it on
    dateCreated = data["year"] #need to adjust this to be a date, not just year
    description = data["description"]
    semester = data["semester"] #does it need semester AND semester ID?
    semesterID = data["semesterID"]
    solution = data["solution"]
    type = data["format"] #what is type??? there is also a format param
    format = data["format"]
    Version = data["version"] #TODO: Add versions to parser, look for single digit
    S3OriginalLink = "google blah blah" + data["fileID"]
    _creator = "5b3699ba791da980bbfeafea" #my user ID? what name to I upload it under?
    _course = data["code"] #TODO: parser needs to be aligned with schema once sorted out
    _school = "MCMASTER-UNIVERSITY-HAM-ONT-CAN" #is this correct?
    #TODO: How will the actual file attached if using a POST request
    
    #is it params?   
    params = {"dateCreated": dateCreated, 

    response = requests.post(reqURL, params=params)
    #verify uploaded without error else log error

              

def getFileName(data):
    OGFormat = data["format"]
    if (OGFormat == 'doc') or (OGFormat == 'docx') or (OGFormat == ''):
        fileFormat = 'odt'
        
    elif (OGFormat == 'ppt'):
        fileFormat = 'ods'

    else:
        fileFormat = OGFormat

    fileName = data["description"] + '.' + fileFormat
    return fileFormat
    
main()
