"""File upload script"""
"""Uploads files from local storage to communote via api
with associated data previously parsed and stored in output.txt"""

import json
import requests
import time


def main():
    creds_file = open("G:\\Documents\\Coding\\Webscraping\\MacEng15\\private\\creds\\communote_credentials.json", "r") #CHANGE
    creds = json.loads(creds_file.read())
    userId = creds["userId"]
    jwt = creds["jwt"]

    uploadLog = open('uploads.log', 'r')
    uploads = uploadLog.read()
    uploadLog.close()
    uploadLog = open('uploads.log', 'a')

    #open output.txt
    f = open("output.txt")
    #f = open("outputShort.txt")


    #read data file
    content = f.readlines()

    validFormats = ['doc', 'docx', 'pdf', 'odt', 'gdoc']
    for line in content:
        data = json.loads(line)
        print "\n" + "=====" + data["description"] + "====="
        if data['fileID'] not in uploads:

            if data["format"] in validFormats:
                #make a new course if it doesn't exist

                reqCourseUrl = "https://api.communote.net/api/course?urlId=MCMASTER-UNIVERSITY-HAM-ONT-CAN&code=" + data["code"].replace(" ", "-").lower() #CHANGE to local host
                r = requests.get(reqCourseUrl)

                 # the problem is you get a 200 then redirects to a error page. Look into how to determine if the course exists or not.
                if r.status_code == 404:
                    newCourse(data["code"], userId, jwt)
                else:
                    print "Course exists"

                #call upload(data)
                response = upload(data, userId, jwt)
                if response.status_code == 200:
                    uploadLog.write(data["fileID"] + '\n')
                else:
                    print '*'*20 + ' \n' + 'ERROR! Status code: ' + str(response.status_code) + '\n' + '*'*20

            else:
                print "Skipping upload. Format: " + data["format"]
        else:
            print "Skipping upload. File already uploaded."
    uploadLog.close()


def encode(code):
    code = code.lower()
    code = code.strip()
    code = code.replace(' ', '-')
    code = ''.join(code.split())
    return code



def newCourse(code, userId, jwt):
    reqUrl = "https://api.communote.net/api/course/new" #CHANGE to local host

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
    reqURL = "https://api.communote.net/api/file/new" #CHANGE to local host

    #adjust the format to what it has been converted/downloaded as
    if file_data["format"] == "gdoc" or file_data["format"][0:3] == "doc":
        print "setting file_format to odt"
        file_format = "odt"
    else:
        file_format = file_data["format"]

	#TODO: Can't get date from gdocs b/c can't use api until granted access. For now will use current date if gdoc
    if file_data["date"] == "":
    	print "time unknown setting as: " + str(time.time())
    	dateCreated = str(time.time())
    else:
        dateCreated = str(file_data["date"])

    description = file_data["description"]
    semesterId = file_data["semesterId"]
    solution = file_data["solution"]
    file_type = file_data["type"]
    Version = file_data["version"] 
    Volume = file_data["volume"]
    courseUrl = file_data["code"]
    schoolUrl = "MCMASTER-UNIVERSITY-HAM-ONT-CAN"

    semesterId = file_data["semesterId"]


    #i.e. /downloads/MATH 1ZA3/Test 2.pdf
    fileName = description + '.' + file_format
    filePath = 'downloads/' + courseUrl + '/'
    file = {'file-to-upload':open(filePath + fileName, 'rb')}

 
    data = {"description": description,
            "dateCreated": dateCreated,
            "semesterId": semesterId,
            "solution": solution,
            "format": file_format,
            "type": file_type,
            "Version": Version,
            "Volume": Volume,
            "userId": userId,
            "courseUrl": encode(courseUrl),
            "schoolUrl": schoolUrl,
            "jwt": jwt
            }
    
    r = requests.post(reqURL, data=data, files=file)


    return r

main()
