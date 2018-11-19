"""File upload script"""
"""Uploads files from local storage to communote via api
with associated data previously parsed and stored in output.txt"""

import json
import requests

#TODO: Script to create new course if doesn't exist?
#TODO: Scrape semester, eval number etc in parsing script better.


def main():
    creds_file = open("G:\\Documents\\Coding\\Webscraping\\MacEng15\\private\\creds\\communote_credentials.json", "r")
    creds = json.loads(creds_file.read())
    userId = creds["userId"]
    jwt = creds["jwt"]

    #open output.txt
    #f = open("output.txt")
    f = open("outputShort.txt")

    #read data file
    content = f.readlines()

    validFormats = ['doc', 'docx', 'pdf', 'odt', 'gdoc']
    for line in content:
        data = json.loads(line)
        if data["format"] in validFormats:
            #make a new course if it doesn't exist

            reqCourseUrl = "https://api.communote.net/api/course?urlId=MCMASTER-UNIVERSITY-HAM-ONT-CAN&code=" + data["code"].replace(" ", "-").lower()
            print reqCourseUrl
            r = requests.get(reqCourseUrl)

             # the problem is you get a 200 then redirects to a error page. Look into how to determine if the course exists or not.
            if r.status_code == 404:
                print "status code for course: " + str(r.status_code)
                newCourse(data["code"], userId, jwt)
            else:
                print "course exists"
            #call upload(data)
            upload(data, userId, jwt)
        else:
            print "Skipping upload. Format: " + data["format"]



def encode(code):
    code = code.lower()
    code = code.strip()
    code = code.replace(' ', '-')
    code = ''.join(code.split())
    return code


encode(" MaTh 1ZA3")

def newCourse(code, userId, jwt):
    reqUrl = "https://api.communote.net/api/course/new"

    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

    data = {"contents":{"group":"","name":code.replace("-", " "),"title":code.replace("-", " ")},"jwt":jwt,"schoolUrl":"MCMASTER-UNIVERSITY-HAM-ONT-CAN","userId":userId}


    r = requests.post(reqUrl, data=json.dumps(data), headers=headers)

    if r.status_code == 200:
        print "Course: " + code + " created."

    else:
        print "Error creating course: " + code + " Status code: " + str(r.status_code)

    return



def upload(file_data, userId, jwt):   
    #send request to communote api with data 
    reqURL = "https://api.communote.net/api/file/new"

    #adjust the format to what it has been downloaded as
    if file_data["format"] == "gdoc" or file_data["format"][0:3] == "doc":
        file_format = "odt"
    else:
        file_format = file_data["format"]

    #dateCreated = data["year"] #need to adjust this to be a date, not just year
    dateCreated = "2018-11-18T03:14:22.884Z"
    description = file_data["description"]
    semesterId = file_data["semesterId"]
    solution = file_data["solution"]
    file_type = file_data["format"] #what is type??? there is also a format param
    Version = file_data["version"] #TODO: Add versions to parser, look for single digit
    Volume = file_data["volume"] #add to the parser. i.e. Test 1 vs. Test 2
    courseUrl = file_data["code"]
    schoolUrl = "MCMASTER-UNIVERSITY-HAM-ONT-CAN" #is this correct?
    #TODO: How will the actual file attached if using a POST request

    #/downloads/MATH 1ZA3/Test 2.pdf
    fileName = description + '.' + file_format
    filePath = 'downloads/' + courseUrl + '/'
    file = {'file-to-upload':open(filePath + fileName, 'rb')}

 #
    data = {"description": description,
            "dateCreated": dateCreated,
            "semesterId": semesterId,
            "solution": solution,
            "type": file_type,
            "Version": Version,
            "Volume": Volume,
            "userId": userId,
            "courseUrl": encode(courseUrl),
            "schoolUrl": schoolUrl,
            "jwt": jwt
            }
    
    print data["courseUrl"]
    r = requests.post(reqURL, data=data, files=file)

    print
    print "status code: "
    print r.status_code
    print
    print "request headers: "
    print r.request.headers
    print
    print "request body: "
    print r.request.body[:2000]
    print 
    print "==========================================================================================================================="
    print

main()
