#
#	Need to add SPARQLWrapper to requirments
#	Need to have the index json file to read from
#

import json
import requests
import io
import csv
from SPARQLWrapper import SPARQLWrapper, JSON
import time

def get_DBPedia_DE_label(uri,language):
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery("""
    select distinct ?label where { <"""
    + uri +"""> 
    <http://www.w3.org/2000/01/rdf-schema#label> ?label FILTER (lang(?label) = '"""+ language +"""') }
    """)
    sparql.setReturnFormat(JSON)
    sparql.setTimeout(10000)
    results = sparql.query().convert()
    labels = []
    for result in results['results']['bindings']:
        labels.append(result['label']['value'])
    return labels


def get_synonyms_wordnet(word,language):
    app_id = ''
    app_key = ''
    
    language = language
    word_id = word
    
    url = 'https://od-api.oxforddictionaries.com:443/api/v1/entries/' + language + '/' + word_id.lower() + '/synonyms'
    try:
        r = requests.get(url, headers = {'app_id': app_id, 'app_key': app_key})
        
        results=r.json()
        synonyms=results['results'][0]['lexicalEntries'][0]['entries'][0]['senses'][0]['synonyms']
        return [syn['text'] for syn in synonyms]
    except:
        return []
    

if __name__ == '__main__':
    uriLabels=dict({})
    request=0
    t0 = time.time()
    with open("labels.csv", "a+") as out:
        writer = csv.writer(out)
        with io.open('./dbpredicateindex14.json', mode="r", encoding="utf-8") as f:
            for cnt, line in enumerate(f):
                #if cnt < 20907:
                    #continue
                obj = json.loads(line)
                url = obj['_source']['uri']
                if url in uriLabels:
                    print ("passed")
                    continue
                #url = 'http://dbpedia.org/resource/Cologne'
                print(cnt,url)
                DBlabels = get_DBPedia_DE_label(url,'de')
                labelsSet=list(set(DBlabels))
                NewlabelsSet=labelsSet
                for label in labelsSet:
                    '''if request >=500:
                        request=0
                        t1 = time.time()
                        total = t1-t0
                        print ("request = ",request)
                        print ("total = ",total)
                        if total < 60:
                            time.sleep(60-total)
                        t0 = time.time()'''
                    synonyms=get_synonyms_wordnet(label,'de')
                    request=request+1
                    print ("request = ",request)
                    NewlabelsSet=NewlabelsSet+synonyms
                    
                    
                synonyms=get_synonyms_wordnet(url[url.rfind('/')+1:],'de')
                request=request+1
                NewlabelsSet=NewlabelsSet+synonyms
                NewlabelsSet=list(set(NewlabelsSet))
                
                uriLabels[url]=NewlabelsSet
                
                writer.writerow([url.encode('utf-8'),uriLabels[url]])