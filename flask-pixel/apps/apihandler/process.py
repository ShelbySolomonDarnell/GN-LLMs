import requests
import string
import json

baseUrl   = 'https://genenetwork.fahamuai.com/api/tasks'
answerUrl = baseUrl + '/answers'

def getAuth(api_config):
    print('Bearer token -> ' + api_config['Bearer Token July 2023'])
    return {"Authorization": "Bearer " + api_config['Bearer Token July 2023']}

def getAnswerWithTaskID( extendUrl, my_auth ):
    print(answerUrl+extendUrl)
    res = requests.get(answerUrl+extendUrl, data={}, headers=my_auth)
    print(res.status_code, res.reason)
    return res.text

def askTheDocuments( extendUrl, my_auth ):
    print(baseUrl+extendUrl)
    res   = requests.get(baseUrl+extendUrl, data={}, headers=my_auth)
    return  res # the Task ID

def openAPIConfig():
    f = open( "/opt/apps/api.config.json" , "rb" )
    #f = open( "api.config.json" , "rb" )
    result = json.load(f)
    f.close()
    return result

def openJsonResponse():
    f = open( "/opt/apps/resp.json" , "rb" )
    #f = open( "resp.json" , "rb" )
    result = json.load(f)
    f.close()
    return result


def getQA( extendUrl, my_auth ):
    # You need a subroutine to remove special characters
    res                  = askTheDocuments(extendUrl, my_auth)
    if (res.status_code == 200):
        taskidjson = json.loads(res.text)
        print(taskidjson)
        extendForAnswer  = '?task_id=' + str(taskidjson['task_id'])
        str_answer       = getAnswerWithTaskID(extendForAnswer, my_auth)
        the_answer       = json.loads(''.join([str(char) for char in str_answer if char in string.printable]))
        '''
        This is where one creates a method to add the data to an object that creates accordion entries.
        the_answer_str   = json.dumps(the_answer, indent=2)
        '''
        return the_answer['data']['answer'], the_answer['data']['context']
    else:
        print('Problems\nStatus code => ' + str(res.status_code) + '\nReason => ' + res.reason + '\nYou will receive a saved response.')
        #print(res.status_code, res.reason)
        return '', ''#createAccordionFromJson(openJsonResponse())

def createAccordionHead(doc_id, head_txt):
    return '<h2 class="accordion-header" id="heading_{0}"><button class="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#collapse_{0}" aria-expanded="false" aria-controls="collapse_{0}">{1}</button></h2>'.format(doc_id, head_txt)

def createAccordionBody(parentName, doc_id, body_txt):
    return '<div id="collapse_{0} class="accordion-collapse collapse show" aria-labelledby="heading_{0}" data-bs-parent="#{1}"><div class="accordion-body">{2}</div></div>'.format(doc_id, parentName, body_txt)

def createAccordionItem(parentName, doc_id, head_txt, body_txt):
    return '<div class="accordion-item">{0}{1}</div>'.format(createAccordionHead(doc_id, head_txt), createAccordionBody(parentName, doc_id, body_txt))

'''
def createAccordionFromJson(expectedJsonResp):
    # get the answer
    answer = expectedJsonResp['data']['answer']
    # get context
    theContext = expectedJsonResp['data']['context']
'''
def createAccordionFromJson(theContext):
    result = ''
    # loop thru json array
    ndx = 1
    for docInfo in theContext:
        docInfoStr = createAccordionItem('accordionRefs', docInfo['document_id'], 'Reference #{0}'.format(ndx), docInfo['text'])
        result += docInfoStr
        print (docInfoStr)
        #print('Ref {0}\n\tDoc ID => {1},\n\tDoc Abstract ==> {2}'.format(ndx, docInfo['document_id'], docInfo['text'])) 
        ndx += 1
    return result

my_auth = getAuth(openAPIConfig())
#the_answer = getAnswerWithTaskID(myobj, my_auth)
#print(my_auth)
#print(the_answer)

#theQuestion = '?ask=How many rat and mouse species are present in GeneNetwork.org studies'
#the_question = askTheDocuments(theQuestion, my_auth)
#print('Task id is -> ' + the_question)

#ans, context = getQA(theQuestion, my_auth)
#print(ans)
#print(context)

