import string
import json
import os

"""
This is a respone class to manage JSON responses.
It will have methods that iterate over a basic json object
and json lists.
Hopefully by combining the methods present in this class managing JSON will be cheza watoto.
"""

class RespContext():
    def __init__(self, context):
        self.cntxt = context
        self.theObj = {}

    def parseIntoObject(self, info):
        # check for obj, arr, or val
        for key, val in info.items():
            if isinstance(val, list):
                self.parseIntoObject(val)
            elif isinstance(val, str) or isinstance(val, int):
                self.theObj[key] = val
            self.theObj[key] = self.val


def createAccordionFromJson(theContext):
    result = ''
    # loop thru json array
    ndx = 0
    for docID, summaryLst in theContext.items():
        # item is a key with a list
        comboTxt = ''
        for entry in summaryLst:
            comboTxt += '\t' + entry['text']
        #print("\nRef -> {0}\n\tCombined text -> {1}\n".format(docID,comboTxt))

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
    return result