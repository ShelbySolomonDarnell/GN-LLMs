import requests
import sys
import time
import string
import json
import os
from apps.apihandler.client import Client


baseUrl           = 'https://genenetwork.fahamuai.com/api/tasks'
answerUrl         = baseUrl + '/answers'
basedir           = os.path.abspath(os.path.dirname(__file__))

apiClient         = Client(requests.Session(), api_key='')

class DocIDs():
    def __init__(self):
        f = open(os.path.join(basedir, "document_ids.json") , "rb" )
        result = json.load(f)
        f.close()
        self.doc_ids = result

    def getInfo(self, doc_id):
        return self.doc_ids[doc_id]
    
the_doc_ids = DocIDs()

def getAuth(api_config):
    print('Bearer token -> ' + api_config['Bearer Token August 2023'])
    return {"Authorization": "Bearer " + api_config['Bearer Token August 2023']}


def formatBibliographyInfo(bibInfo):
    if isinstance(bibInfo, str):
        # remove '.txt'
        bibInfo = bibInfo.removesuffix('.txt')
    else:
        # format string bibliography information
        bibInfo = "{0}. ".format(bibInfo['author'], bibInfo['title'], bibInfo['year'], bibInfo['doi'])
    return bibInfo


def askTheDocuments( extendUrl, my_auth ):
    try:
        res     = requests.post(baseUrl+extendUrl, 
                            data={}, 
                            headers=my_auth)
        res.raise_for_status()
    except:
        raise # what
    if (res.status_code != 200):
        return negativeStatusMsg(res), 0
    task_id     = getTaskIDFromResult(res)
    res         = getAnswerUsingTaskID(task_id, my_auth)
    if (res.status_code != 200):
        return negativeStatusMsg(res), 0
    return res, 1

def getAnswerUsingTaskID( extendUrl, my_auth ):
    try:
        res = requests.get(answerUrl+extendUrl, data={}, headers=my_auth)
        res.raise_for_status()
    except:
        raise
    return res

def openAPIConfig():
    f = open(os.path.join(basedir, "api.config.json") , "rb" )
    result = json.load(f)
    f.close()
    return result


def getTaskIDFromResult(res):
    task_id = json.loads(res.text)
    result  = '?task_id=' + str(task_id['task_id'])
    return result

def negativeStatusMsg(res):
    return 'Problems\n\tStatus code => {0}\n\tReason=> {res.reason}'.format(res.status_code, res.reason)

def filterResponseText(val):
    return json.loads(''.join([str(char) for char in val if char in string.printable]))

def getGNQA(query):
    res, task_id = apiClient.ask('?ask=' + query)
    res, success = apiClient.getAnswer(task_id) 
    '''
    res, queryGood = askTheDocuments('?ask=' + query, auth)
    if (queryGood==0):
        return res, '' 
    '''
    if ( success == 1 ):
        respText       = filterResponseText(res.text)
        answer         = respText['data']['answer']
        context        = respText['data']['context']
        accordionBody  = createAccordionFromJson(context)
        return answer, accordionBody
    else:
        return res, "Unfortunately I have nothing."

def createAccordionHead(doc_id, expanded, head_txt):
    if expanded == 0:
        expanded = "False"
    else:
        expanded = "True"
    return '<h2 class="accordion-header" id="heading_{0}"><button class="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#collapse_{0}" aria-expanded="{1}" aria-controls="collapse_{0}">{2}</button></h2>'.format(doc_id, expanded, head_txt)

def createAccordionBody(parentName, doc_id, body_txt):
    #docInfo = 
    return '<div id="collapse_{0}" class="accordion-collapse collapse" aria-labelledby="heading_{0}" data-bs-parent="#{1}"><div class="accordion-body">{2}</div></div>'.format(doc_id, parentName, body_txt)

def createAccordionItem(parentName, doc_id, head_txt, body_txt, expand):
    return '<div class="accordion-item">{0}{1}</div>'.format(createAccordionHead(doc_id, expand, head_txt), createAccordionBody(parentName, doc_id, body_txt))

def createAccordionFromJson(theContext):
    result = ''
    # loop thru json array
    ndx = 1
    for docInfo in theContext:
        if ndx == 1:
            expand = 1
        else: 
            expand = 0
        bibInfo    = formatBibliographyInfo(the_doc_ids.getInfo(docInfo['document_id']))
        docInfoStr = createAccordionItem('accordionRefs', 
                                         docInfo['document_id'], 
                                         #'Reference #{0} -- Document ID {1}'.format(ndx, docInfo['document_id']), 
                                         'Reference #{0} -- {1}'.format(ndx, bibInfo), 
                                         docInfo['text'], 
                                         expand)
        result += docInfoStr
        print (docInfoStr)
        ndx += 1
    return result

'''
my_auth = getAuth(openAPIConfig())

res, task_id = AskClient('Which is better, rats or mice?')
print (res)
print ("Ask for the result behind the task id --> {0}".format(task_id))
res, other = AnsClient(task_id)
print (res)
respText       = filterResponseText(res.text)
answer         = respText['data']['answer']
context        = respText['data']['context']
print ("Context --> {1}\nAnswer --> {0}".format(answer, context))
print (getJsonDocIDs())
print(getJsonRefs())
'''


