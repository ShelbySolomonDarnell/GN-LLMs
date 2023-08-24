import sys
import time
import string
import json
import os

basedir           = os.path.abspath(os.path.dirname(__file__))

def getJsonDocIDs():
    f = open(os.path.join(basedir, "document_ids.json") , "rb" )
    result = json.load(f)
    f.close()
    return result

def getJsonRefs():
    f = open(os.path.join(basedir, "gn_bib.json") , "rb" )
    result = json.load(f)
    f.close()
    return result

doc_ids = getJsonDocIDs()
gn_refs = getJsonRefs()

doc_ids_keys = doc_ids.keys()
keys_gn_refs = gn_refs.keys()

'''
print (json.dumps(gn_refs['ashbrook_expanded2019']['filename'], indent=2))
print (doc_ids_keys)
print (keys_gn_refs)
'''
print (json.dumps(doc_ids, indent=2))


