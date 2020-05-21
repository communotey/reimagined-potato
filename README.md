# reimagined-potato

## Recommended Setup

* Python 3.7
* Conda for communote virtualenv
* pip3 for the rest
  * Jupiter notebook

## TODO

communoteParse_v2.py
	change the name of script to something less confusing such as parse.py
	parse version (single digit after a v, sometimes A or B versions)
	parse semesterID using (Winter:0 spring: 1 summer: 2 fall: 3)
	need to change getFormatAndDesc(filename) so that if it is a google doc it returns something useful. Currently returns "unknown"
		or have it return "GDOC" and have the downloadScript.py recog that as a google doc then have a way to determine if it should be downloaded as odt or odp
			only a handful of these cases so could hard code it if too much work
				if it should be odt, has line "<body dir="ltr" role="application" class="" itemscope="" itemtype="http://schema.org/CreativeWork/PresentationObject">"
					ends with "/PresentationObject" on the other hand if it should be odt, ends with "/DocumentObject"


downloadScript.py
	GDOC file type as mentioned in above in communoteParse_v2 section
	figure out authentication for google drive API to convert docx --> google doc
		trying using service account info in google-cloud-communote-211623.json
	

uploadScript.py
	code uses format: e.g. MATH 1ZA3
	for dataCreated: if only know the year, use Jan 2nd of that year. Not sure what the format is of the data (iso or epoch?)
	use only semesterID, don't use semester (Winter:0 spring: 1 summer: 2 fall: 3)
	may need to make changes to the parser.py output to make the upload script easier to send data as needed in the appropriate format
	
	

CHANGES: (23/10/2018)

communoteParse_v2.py
	REMOVED redundant noteTag check
	getSemester:
		made it return "" reather than 0 if no semester is parsed
		fixed it to lowercase the tag found before comparing to seasons. findall ingnored case but still returned uppercase strings which then didn't match the lowercase strings
	
	CHANGED getVersion:
		finished previously incomplete function
		
	ADDED output['version'] = getVersions(filename)
	
	CHANGED getFormatAndDesc:
		if no "." in file name means is a GDOC, changed that case to return "GDOC" as the extension rather than "unknown"
		
	ADDED scrapeGDocType(fileID): 
		if no "." from getFormatAndDesc then calls this to return it's googledoc download type i.e. odt, odp, dos
			appears there are only odt files anyways.
		
	problem with: {"code": "CHEM 1E03", "description": "Chapter 19 & 20", "format": "odt", "solution": false, "volume": "19", "version": "", "year": "", "semesterId": "", "type": "note", "fileID": "0BxW61uJyyN8TS3g1V0dwMVhmWEE"}
	It is a .doc but doesn't have a file extension in the original file name. The parser then labbels it as an odt when it should be labeled as a .doc in the output text file. Only want google docs to be labelled as odt's in the output.txt file.
	
	
	
	
	
Dec 2nd
	
	Problem where uploading docx but sending data in request that it is odt or vice verse? maybe not. could just be that the odt files can't be viewed on site b/c not supported yet?
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	

