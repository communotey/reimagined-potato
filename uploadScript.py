"""File upload script"""
"""Uploads files from local storage to communote via api
with associated data previously parsed and stored in output.txt"""

import json
import requests

#TODO: Script to create new course if doesn't exist?
#TODO: Scrape semester, eval number etc in parsing script better.

def main():
    #open output.txt
    #f = open("output.txt")
    f = open("outputShort.txt")
    
    #read data file
    content = f.readlines()

    validFormats = ['doc', 'docx', 'pdf', 'odt', 'gdoc']
    for line in content:
        data = json.loads(line)
        if data["format"] in validFormats:
            #call upload(data)
            upload(data)
        else:
            print "Skipping upload. Format: " + data["format"]

def upload(data):   
    #send request to communote api with data 
    reqURL = "https://api.communote.net/api/file/new"
    #reqURL = "http://httpbin.org/post"

    #adjust the format to what it has been downloaded as
    if data["format"] == "gdoc" or data["format"][0:3] == "doc":
        file_format = "odt"
    else:
        file_format = data["format"]

    dateCreated = data["year"] #need to adjust this to be a date, not just year
    description = data["description"]
    semesterID = data["semesterId"]
    solution = data["solution"]
    file_type = data["format"] #what is type??? there is also a format param
    Version = data["version"] #TODO: Add versions to parser, look for single digit
    Volume = data["volume"] #add to the parser. i.e. Test 1 vs. Test 2
    S3OriginalLink = "https://docs.google.com/open?id=" + data["fileID"]
    _creator = "5b3699ba791da980bbfeafea" #my user ID? what name to I upload it under?
    _course = data["code"]
    _school = "MCMASTER-UNIVERSITY-HAM-ONT-CAN" #is this correct?
    #TODO: How will the actual file attached if using a POST request

    #/downloads/MATH 1ZA3/Test 2.pdf
    filePath = 'downloads/' + _course + '/' + description + '.' + file_format
    file = {'file':open(filePath, 'rb')}

 
    data = {"description": description,
            "dateCreated": dateCreated,
            "semesterID": semesterID,
            "solution": solution,
            "type": file_type,
            "Version": Version,
            "Volume": Volume,
            "S3OriginalLink": S3OriginalLink,
            "_creator": _creator,
            "_course": _course,
            "_school": _school
            }
    

    print "data: "
    print data
    r = requests.post(reqURL, data=data, files=file)

    print
    print "status code: "
    print r.status_code
    print
    print "request headers: "
    print r.request.headers
    print
    #print "request body: "
    #print r.request.body
    print 


    
main()
