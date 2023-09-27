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
        if doc_id in self.doc_ids.keys():
            return self.doc_ids[doc_id]
        else:
            return doc_id

the_doc_ids = DocIDs()

def getAuth(api_config):
    print('Bearer token -> ' + api_config['Bearer Token September 2023'])
    return {"Authorization": "Bearer " + api_config['Bearer Token September 2023']}


def formatBibliographyInfo(bibInfo):
    if isinstance(bibInfo, str):
        # remove '.txt'
        bibInfo = bibInfo.removesuffix('.txt')
    elif isinstance(bibInfo, dict):
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
    return '<div id="collapse_{0}" class="accordion-collapse collapse" aria-labelledby="heading_{0}" data-bs-parent="#{1}"><div class="accordion-body">{2}</div></div>'.format(doc_id, parentName, body_txt)

def createAccordionItem(parentName, doc_id, head_txt, body_txt, expand):
    return '<div class="accordion-item">{0}{1}</div>'.format(createAccordionHead(doc_id, expand, head_txt), createAccordionBody(parentName, doc_id, body_txt))

def createAccordionFromJson(theContext):
    result = ''
    # loop thru json array
    ndx = 0
    expand = 1
    for docID, summaryLst in theContext.items():
        if ndx > 0:
            expand = 0 
        # item is a key with a list
        comboTxt = ''
        for entry in summaryLst:
            comboTxt += '\t' + entry['text']
        print("\nRef -> {0}\n\tCombined text -> {1}\n".format(docID,comboTxt))

        docInfo = the_doc_ids.getInfo(docID)
        if docID != docInfo:
            bibInfo    = formatBibliographyInfo(docInfo)
        else:
            bibInfo    = docID
        docInfoStr = createAccordionItem('accordionRefs', docID,
                    'Reference #{0} -- Document ID {1}'.format(ndx, bibInfo),
                    '{0}'.format(comboTxt),
                    expand)
        result += docInfoStr
        ndx += 1
    return result

    '''
    for docID in theContext:
        if ndx == 1:
            expand = 0 #1
        else:
            expand = 0
        print("\nThe document identifier is -> {0}\n".format(json.dumps(docID,indent=2,sort_keys=False)))
        #docTxt  = docID['text']
        #docInfo = the_doc_ids.getInfo(docID['document_id'])
        #if docID != docInfo:
        #    bibInfo    = formatBibliographyInfo(docInfo)
        #else:
        #    bibInfo    = docID
        #docInfoStr = createAccordionItem('accordionRefs', docID,
        #            'Reference #{0} -- Document ID {1}'.format(ndx, docID),
        #            'Reference #{0} -- {1}'.format(ndx, bibInfo),
        #            docTxt,
        #            expand)
        #result += docInfoStr
        #print("\nThe document informaton is -> {0}\n\tbibinfo is {1}\n".format(docInfo,bibInfo))
        #print (docInfoStr)
        #ndx += 1
    '''

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


