import string
import json
import os

"""
This is a respone class to manage JSON responses.
It will have methods that iterate over a basic json object
and json lists.
Hopefully by combining the methods present in this class managing JSON will be cheza watoto.
"""
basedir           = os.path.abspath(os.path.dirname(__file__))


class DocIDs():
    def __init__(self):
        # open doc ids for GN refs
        self.doc_ids = {} 
        # open all doc ids file
        self.all_doc_ids = self.loadFile("../static/assets/data/refs_id_name.json")
        self.formatDocIDs(self.all_doc_ids)


    def loadFile(self, file_name):
        file_path = os.path.join(basedir, file_name)
        if os.path.isfile(file_path):
            f = open(file_path, "rb")
            result = json.load(f)
            f.close()
            return result
        else:
            raise Exception("\n{0} -- File does not exist\n".format(file_path))

    def formatDocIDs(self, values):
        for _key, _val in values.items():
            #print("Key {0}".format(_key))
            if isinstance(_val, list):
                #print("We have a list of values")
                for theObject in _val:
                    docName = self.formatDocumentName(theObject['filename'])
                    docID   = theObject['id']
                    #print("Tuple --> {0}, {1}".format(docID, docName))
                    self.doc_ids.update({docID: docName})

    def formatDocumentName(self, val):
       result = val.removesuffix('.pdf')
       result = result.removesuffix('.txt')
       result = result.replace('_', ' ')
       return result


    def getInfo(self, doc_id):
        if doc_id in self.doc_ids.keys():
            return self.doc_ids[doc_id]
        else:
            return doc_id

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


the_doc_ids = DocIDs()

"""
%s/{*,\n"filename"/{"filename"/
:%s/author=/"author": /
:%s/journal=/"journal": /
:%s/url=/"url": /
:%s/doi=/"doi": /
:%s/issn=/"issn": /
:%s/urldate=/"urldate": /
:%s/volume=/"volume": /
:%s/number=/"number": /
:%s/pages=/"pages": /
:%s/year=/"year": /
:%s/month=/"month": /
:%s/publisher=/"publisher": /
%s/:\s{/: "/
%s/*},/\*",/
%s/[a-z]\+},/[

Welcome to the GeneNetwork Question and Answer (GNQA)system. We utilize a large language model and 3000 scientific publications to make GNQA a subject matter expert in three areas: GeneNetwork.org research, genomics/genetics with regards to diabetes, and genomics/genetics with regards to aging.  At the moment when you ask GNQA something it will attempt to return a sensible answer with ``real'' references. To this end we aim to reduce hallucinations and provide a knowledge launchpad for a researcher to enhance their knowledge on the relevant subject matter.  GNQA is not a finished product as we are working diligently to improve it daily. Thanks for using GNQA!
"""