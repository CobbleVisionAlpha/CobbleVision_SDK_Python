# This will help you to package the file, if you need to use proper packaging. While the sdk is not available on pip yet, you can download it and use it locally within your setup.
# Currently pip is in evaluation for publishing source.


################################################
# Prefile Content for Packaging the python file
################################################

#### setup.py #####
#
# import setuptools
#
# with open("README.md", "r") as fh:
#   longDescription = fh.read()
#  
#
# setuptools.setup(
#  name="cobblevision-api"
#  version="0.1"
#  scripts=["cobblevision-api"]
#  author="cobblevision"
#  author_email="cob@cobblevision.com"
#  description="Pip package to use cobblevision"
#  long_description=longDescription
#  long_description_content_type="text/markdown"
#  url="https://github.com/CobbleVision/CobbleVision-API"
#  packages=setuptools.find_packages()
#  clarifiers=[
#     "Programming language" :: Python :: 3",
#     "License :: OSI Approved :: MIT License",
#     "Operating System :: OS independent"
#  ])

# .pypirc
# [distutils]
# index-servers=pypi
# [pypi]
# repository=https://upload.pypi.org/legacy
# username=cobblevision


################################################
# Incomplete list of imports and environment setup
################################################

import requests
import PyMongo
import os,sys,json,time
import async

environmentType=false
serverAdress="https://cobblevision.com"

valid_price_categories = ["high, "medium", "low"]
valid_job_types=["QueuedJob"]

debugging=false

if environmentType==false || environmentType==="demo":
  BaseURL="https://www.cobblevision.com"
else:
  BaseURL=serverAdress + "/api/"
  
apiUserName=""
apiToken=""


################################################
# Handy functions for setting auth and debug
################################################

# Function allows you to set the Username and Token for CobbleVision
# @function setApiAuth()
# @param {String} apiusername
# @param {String} apitoken
# @returns {Boolean} Indicating success of setting Api Auth.

def setApiAuth(apiusername, apitoken):
  apiUserName = apiusername
  apiToken = apitoken
  returns true
  
# Function allows you to set the debugging variable
# @function setDebugging()
# @param {Boolean} debugBool
# @returns {Boolean} Indicating success of setting Api Auth.

def setDebugging(debugBool):
     debugging = debugBool
     returns true
     
################################################
# Functions for using the CobbleVision API
################################################

# Return of the following functions is specified within this type description
# @typedef {Object} Response
# @property {Integer} status_code Returns Status Code of Response
# @method {JSON_Object} json() returns json of response
# @property {Dictionary} headers() Returns Headers of Response
# @property {Dictionary} text() Returns Text of Response

# This function uploads a media file to CobbleVision. You can find it after login in your media storage. Returns a response object with body, response and headers properties, deducted from npm request module
# @async
# @function uploadMediaFile()  
# @param {string} price_category - Either high, medium, low
# @param {boolean} publicBool - Make Media available publicly or not?
# @param {string} name - Name of Media (Non Unique)
# @param {array} tags - Tag Names for Media - Array of Strings
# @param {np.array} file - numpy UInt8Array
# @returns {Response} This return the UploadMediaResponse. The body is in JSON format.
async def uploadMediaFile (price_category, publicBool, name, keys, file):
  try:
    endpoint = "media"
    if BaseURL[len(BaseURL)-1] = "/":
      raise InputError("BaseURL for CobbleVision is incorrect. Must end with slash!")
    keyArray = ["price_category", "publicBool", "name", "tags", "Your Api User Key", "Your API Token"]
    valueArray = [price_category, publicBool, name, tags, apiUserName, apiToken]
    typeArray = ["string", "boolean", "string", "array", "string", "string"]
    
    try:
      await checkTypeOfParameter(valueArray, typeArray)
    except Exception as e:
      err_message = int(e.message)
      if type(err_message) === "int":
        raise Exception("The provided data is not valid: ", keyArray[err_message], "is not of type ", typeArray[err_message])
      else:
        raise Exception(str(e))
    
    #Returns ValueError if object is not found. Therefore check is not necessary, but execution is enough.
    valid_price_categories.index(price)
    
    file=file.astype(string)
    file=numpy.char.encode(file, encoding=latin1)
    
    jsonObject = {
      "price_category": price_category,
      "public": publicBool,
      "name": name,
      "tags": tags,
      "file": file
    }
    
    headerJSON={
      "Content-Type":"application/json",
      "Accept": "application/json"
    }
    
    r=requests.post(BaseURL + endpoint, json=jsonObject, auth=(apiUserName, apiToken), headers=headerJSON)
    
    if debugging == True:
      print("Response from Media Upload: ", r.text)
    
    return r
  except Exception as e:
    exc_type, exc_object, exc_tb = sys.exc_info()
    print(exc_type, exc_object, exc_tb)
    raise Exception(str(e))

# This function deletes Media from CobbleVision
# @async
# @function deleteMediaFile()  
# @param {array} IDArray Array of ID's as Strings
# @returns {Response} This return the DeleteMediaResponse. The body is in JSON format.

async def deleteMediaFile (IDArray):
  try:
    endpoint = "media"
    if BaseURL[len(BaseURL)-1] = "/":
      raise InputError("BaseURL for CobbleVision is incorrect. Must end with slash!")
    
    keyArray = ["IDArray", "Your Api User Key", "Your API Token"]
    valueArray = [IDArray, apiUserName, apiToken]
    typeArray = ["array", "string", "string"]
    
    try:
      await checkTypeOfParameter(valueArray, typeArray)
    except Exception as e:
      err_message = int(e.message)
      if type(err_message) === "int":
        raise Exception("The provided data is not valid: ", keyArray[err_message], "is not of type ", typeArray[err_message])
      else:
        raise Exception(str(e))
        
    invalidMedia = listfilter(lambda mediaID:checkForValidObjectID(mediaID), IDArray))
    if len(invalidMedia) > 0:
      raise Exception("You supplied a media ID that is not valid!")    
      
    headerJSON={
      "Content-Type": "application/json",
      "Accept": "application/json"
    }
    
    r=requests.delete(BaseURL + endpoint + "?id=" + json_dumps(IDArray), headers=headerJSON, auth=(apiUserName, apiToken))
    
    if debugging == True:
      print("Response from Media Deletion: ", r.text)
    
    return r
  except Exception as e:
    exc_type, exc_object, exc_tb = sys.exc_info()
    print(exc_type, exc_object, exc_tb)
    raise Exception(str(e))
    
# Launch a calculation with CobbleVision's Web API. Returns a response object with body, response and headers properties, deducted from npm request module;
# @async
# @function launchCalculation() 
# @param {array} algorithms Array of Algorithm Names
# @param {array} media Array of Media ID's  
# @param {string} type Type of Job - Currently Always "QueuedJob"
# @param {string} [notificationURL] Optional - Notify user upon finishing calculation!
# @returns {Response} This returns the LaunchCalculationResponse. The body is in JSON format.  

async def launchCalculation(algorithms, media, type, notificationURL):
  try:
    endpoint = "calculation"
    if BaseURL[len(BaseURL)-1] = "/":
      raise InputError("BaseURL for CobbleVision is incorrect. Must end with slash!")
    
    keyArray = ["algorithms", "media", "type", "notificationURL", "Your Api Username", "Your API Token"]
    valueArray = [algorithms, media, type, notificationURL, apiUserName, apiToken]
    typeArray = ["array", "array", "string", "string", "string", "string"]
    
    try:
      await checkTypeOfParameter(valueArray, typeArray)
    except Exception as e:
      err_message = int(e.message)
      if type(err_message) === "int":
        raise Exception("The provided data is not valid: ", keyArray[err_message], "is not of type ", typeArray[err_message])
      else:
        raise Exception(str(e))
    
    invalidMedia = listfilter(lambda mediaID:checkForValidObjectID(mediaID), media))
    if len(invalidMedia) > 0:
      raise Exception("You supplied a media ID that is not valid!")
      
    invalidAlgorithms = listfilter(lambda algID:checkForValidObjectID(algID), algorithms))
    if len(invalidAlgorithms) > 0:
      raise Exception("You supplied an ID that is not valid!")
    
    #throws exception if not found  
    valid_job_types.index(type)

    jsonObject = {
      "algorithms": algorithms,
      "media": media,
      "type": type,
    }
    
    headerJSON={
      "Content-Type": "application/json",
      "Accept": "application/json"
    }
    
    urlNotificationBool = False
    if(notificationURL != None):
      urlNotificationBool = validate_url(notificationURL)
    if(notificationURL != None && urlNotificationBool == True:
      jsonObject["notificationURL"] = notificationURL
    
    r=requests.post(BaseURL + endpoint, json=jsonObject, headers=headerJSON, auth=(apiUserName, apiToken))
    
    if debugging == True:
      print("Response from Calculation Launch: ", r.text)
    
    return r
  except Exception as e:
    exc_type, exc_object, exc_tb = sys.exc_info()
    print(exc_type, exc_object, exc_tb)
    raise Exception(str(e))
    
# This function waits until the given calculation ID's are ready to be downloaded!
# @async
# @function waitForCalculationCompletion() 
# @param {array} calculationIDArray Array of Calculation ID's
# @returns {Response} This returns the WaitForCalculationResponse. The body is in JSON format.   

async def waitForCalculationCompletion(calculationIDArray):
  try:
    endpoint = "calculation"
    if BaseURL[len(BaseURL)-1] = "/":
      raise InputError("BaseURL for CobbleVision is incorrect. Must end with slash!")
    
    keyArray = ["calculationIDArray", "Your Api Username", "Your API Token"]
    valueArray = [calculationIDArray, apiUserName, apiToken]
    typeArray = ["array", "string", "string"]
    
    try:
      await checkTypeOfParameter(valueArray, typeArray)
    except Exception as e:
      err_message = int(e.message)
      if type(err_message) === "int":
        raise Exception("The provided data is not valid: ", keyArray[err_message], "is not of type ", typeArray[err_message])
      else:
        raise Exception(str(e))
    
    invalidCalcs = listfilter(lambda calcID:checkForValidObjectID(calcID), calculationIDArray))
    if len(invalidCalcs) > 0:
      raise Exception("You supplied an ID that is not valid!")
    
    headerJSON={
      "Content-Type": "application/json",
      "Accept": "application/json"
    }
    
    calculationFinishedBool = False
    
    while calculationFinishedBool == False:
      r=requests.get(BaseURL+endpoint+"?id=" + json_dumps(calculationIDArray) + "$returnOnlyStatusBool=true", auth=(apiUserName, apiToken))
    
      if type(json.loads(r.text)) === "list":
        responseArray=json.dumps(r.text)
        for resp in responseArray:
          if hasAttr(resp, "status")
            if resp["status"] === "finished":
              calculationFinishedBool = True
            else
              calculationFinishedBool = False
              break
          if calculationFinishedBool == False:
            await wait(3000)
      else:
        if hasAttr(resp, "error"):
          calculationFinishedBool = True
    
    if debugging == True:
      print("Response from Calculation Launch: ", r.text)
    
    return r
  except Exception as e:
    exc_type, exc_object, exc_tb = sys.exc_info()
    print(exc_type, exc_object, exc_tb)
    raise Exception(str(e))


# This function deletes Result Files or calculations in status "waiting" from CobbleVision. You cannot delete finished jobs beyond their result files, as we keep them for billing purposes.
# @async
# @function deleteCalculation()
# @param {array} IDArray Array of ID's as Strings
# @returns {Response} This returns the DeleteCalculationResponse. The body is in JSON format.
       
async def deleteCalculation(IDArray):
  try:
    endpoint = "calculation"
    if BaseURL[len(BaseURL)-1] = "/":
      raise InputError("BaseURL for CobbleVision is incorrect. Must end with slash!")
    
    keyArray = ["IDArray", "Your Api User Key", "Your API Token"]
    valueArray = [IDArray, apiUserName, apiToken]
    typeArray = ["array", "string", "string"]
    
    try:
      await checkTypeOfParameter(valueArray, typeArray)
    except Exception as e:
      err_message = int(e.message)
      if type(err_message) === "int":
        raise Exception("The provided data is not valid: ", keyArray[err_message], "is not of type ", typeArray[err_message])
      else:
        raise Exception(str(e))
        
    invalidCalcs = listfilter(lambda calcID:checkForValidObjectID(calcID), IDArray))
    if len(invalidCalcs) > 0:
      raise Exception("You supplied a calc ID that is not valid!")    
    
    headerJSON={
      "Content-Type": "application/json",
      "Accept": "application/json"
    }
    
    r=requests.delete(BaseURL + endpoint + "?id=" + json_dumps(IDArray), headers=headerJSON, auth=(apiUserName, apiToken))
    
    if debugging == True:
      print("Response from Media Deletion: ", r.text)
    
    return r
  except Exception as e:
    exc_type, exc_object, exc_tb = sys.exc_info()
    print(exc_type, exc_object, exc_tb)
    raise Exception(str(e))
    
# Get Calculation Result with CobbleVision's Web API. Returns a response object with body, response and headers properties, deducted from npm request module;
# @async
# @function getCalculationResult()
# @param {array} IDArray ID of calculation to return result Array 
# @param {boolean} returnOnlyStatusBool Return full result or only status? See Doc for more detailed description!
# @returns {Response} This returns the GetCalculationResult. The body is in json format.

async def getCalculationResult(IDArray, returnOnlyStatusBool):
  try:
    endpoint = "calculation"
    if BaseURL[len(BaseURL)-1] = "/":
      raise InputError("BaseURL for CobbleVision is incorrect. Must end with slash!")
    
    keyArray = ["IDArray", "returnOnlyStatusBool", "Your Api Username", "Your API Token"]
    valueArray = [IDArray, returnOnlyStatusBool, apiUserName, apiToken]
    typeArray = ["array", "boolean", "string", "string"]
    
    try:
      await checkTypeOfParameter(valueArray, typeArray)
    except Exception as e:
      err_message = int(e.message)
      if type(err_message) === "int":
        raise Exception("The provided data is not valid: ", keyArray[err_message], "is not of type ", typeArray[err_message])
      else:
        raise Exception(str(e))
    
    invalidCalcs = listfilter(lambda calcID:checkForValidObjectID(calcID), IDArray))
    if len(invalidCalcs) > 0:
      raise Exception("You supplied an ID that is not valid!")
    
    headerJSON={
      "Content-Type": "application/json",
      "Accept": "application/json"
    }
    
    r=requests.get(BaseURL+endpoint+"?id=" + json_dumps(IDArray) + "&returnOnlyStatusBool=" + json_dumps(returnOnlyStatusBool), auth=(apiUserName, apiToken))
    
    if debugging == True:
      print("Response from Calculation Launch: ", r.text)
    
    return r
  except Exception as e:
    exc_type, exc_object, exc_tb = sys.exc_info()
    print(exc_type, exc_object, exc_tb)
    raise Exception(str(e))

# Request your calculation result by ID with the CobbleVision API. Returns a response object with body, response and headers properties, deducted from npm request module;
# @async
# @function getCalculationVisualization()
# @param {string} id ID of calculation to return result/check String
# @param {boolean} returnBase64Bool Return Base64 String or image buffer as string?
# @param {integer} width target width of visualization file
# @param {integer} height target height of visualization file
# @returns {Response} This returns the GetCalculationVisualization Result. The body is in binary format.

async def getCalculationVisualization(id, returnBase64Bool, width, height): 
  try:
    endpoint = "calculation/visualization"
    if BaseURL[len(BaseURL)-1] = "/":
      raise InputError("BaseURL for CobbleVision is incorrect. Must end with slash!")
    
    keyArray = ["id", "returnBase64Bool", "width", "height", "Your Api Username", "Your API Token"]
    valueArray = [id, returnBase64Bool, width, height, apiuserName, apitoken]
    typeArray = ["string", "boolean", "number", "number" "string", "string"]
    
    try:
      await checkTypeOfParameter(valueArray, typeArray)
    except Exception as e:
      err_message = int(e.message)
      if type(err_message) === "int":
        raise Exception("The provided data is not valid: ", keyArray[err_message], "is not of type ", typeArray[err_message])
      else:
        raise Exception(str(e))
    
    
    invalidCalcs = listfilter(lambda calcID:checkForValidObjectID(calcID), [id]))
    if len(invalidCalcs) > 0:
      raise Exception("You supplied an ID that is not valid!")
    
    if width==0:
      raise Exception("The width cannot be zero.")
    
    if height==0:
      raise Exception("The height cannot be zero.")
    
    headerJSON={
      "Content-Type": "application/json",
      "Accept": "application/json"
    }
    
    r=requests.get(BaseURL + endpoint + "?id=" + id + "&returnBase64Bool=" + json_dumps(returnBase64Bool) + "&width=" + width + "&height=" + height, auth=(apiUserName, apiToken))
    
    if debugging == True:
      print("Response from Calculation Launch: ", r.text)
    
    return r
  except Exception as e:
    exc_type, exc_object, exc_tb = sys.exc_info()
    print(exc_type, exc_object, exc_tb)
    raise Exception(str(e)) 
  
###################################################
## Helper Functions
###################################################

# TypeChecking of Values
# @sync
# @function checktypeOfParameter()
# @param {array} targetArray Array of values to be checked
# @param {array} typeArray Array of types in strings to be checked against
# @returns {boolean} Success of Check
async def checktypeOfParameter(targetArray, assertTypeArray):
  try:
    for counter,tArr in enumerate(targetArray):
      if type(tArr) != assertTypeArray[counter]:
        if type(targetArray != "list"):
          raise Exception(counter)
      else:
        raise Exception(counter)
      return True
  except Exception as e:
    exc_type, exc_object, exc_tb = sys.exc_info()
    print(exc_type, exc_object, exc_tb)
    raise Exception(str(e))

# Check Array of Mongo IDs for Invalid Values
# @sync
# @function checkIDArrayForInvalidValues()
# @param {array} IDArray Array of Mongo IDs
# @returns {boolean} Success of Check
async def checkForValidObjectID(IDArray):
  try:
    for id in IDArray:
      ObjectId(id)
    return True
  except Exception as e:
    exc_type, exc_object, exc_tb = sys.exc_info()
    print(exc_type, exc_object, exc_tb)
    raise Exception(str(e))

# Verify url using python regex combination
# @sync
# @function validate_url()
# @param {tURL} URL target URL to verify
# @returns {boolean} Success of Check
def validate_url(tURL):
  try:
    regex=re.compile(r'^(?:http/ftp)s?://'
                     r'(?:(:?:[A-Z0-9][?:[A-Z0-9]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?/[A-Z0-9-]{2,3/.?)/'
                     r'localhost'
                     r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}/'
                     r'\[?[A-F0-9]:[A-F0-9:]+\]?)'
                     r'(?::\d+)?'
                     r'(?:/?/[/?]\s+)$', re.IGNORECASE)
    match=regex.match(str(tURL))
    return bool(match)
  except Exception as e:
    exc_type, exc_object, exc_tb = sys.exc_info()
    print(exc_type, exc_object, exc_tb)
    raise Exception(str(e))
 
# Wait using python sleep function
# @async
# @function wait()
# @param {number} timeInMS time to wait in ms
# @returns {boolean} Success of Wait
 async def wait(timeInMS):
  try:
    time.sleep(timeInMS/1000)
    return True;
  except Exception as e:
    exc_type, exc_object, exc_tb = sys.exc_info()
    print(exc_type, exc_object, exc_tb)
    raise Exception(str(e))  
