#
#	Need to add SPARQLWrapper to requirments
#	Need to have the index json file to read from
#

import json
import requests
import io
import csv
from SPARQLWrapper import SPARQLWrapper, JSON

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

def get_WikiData_Id(uri):
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery("""
    SELECT DISTINCT ?wiki
    WHERE {
            <"""+uri+"""> <http://www.w3.org/2002/07/owl#sameAs> ?wiki.
            FILTER regex(?wiki,'wikidata.org')
    }
    """)
    sparql.setReturnFormat(JSON)
    sparql.setTimeout(10000)
    results = sparql.query().convert()
    try:
        wid = results["results"]["bindings"][0]['wiki']['value']
        return wid[wid.rfind('/')+1:]
    except IndexError:
        return ''

def get_WikiData_DE_label(wikiId):
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
    sparql.setQuery("""PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX wd: <http://www.wikidata.org/entity/>
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
    PREFIX dbo: <http://dbpedia.org/ontology/>
    SELECT DISTINCT ?label 
    WHERE 
    { 
      {wd:"""+wikiId+""" skos:altLabel ?label.} 
      UNION
      {wd:"""+wikiId+""" rdfs:label ?label.} 
      UNION
      {wd:"""+wikiId+""" dbo:alias ?label.}
      FILTER (lang(?label) = 'en')
    } """)
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
    with open("labels.csv", "w") as out:
        writer = csv.writer(out)
        with io.open('./dbpredicateindex14.json', mode="r", encoding="utf-8") as f:
            for cnt, line in enumerate(f):
                obj = json.loads(line)
                url = obj['_source']['uri']
                if url in uriLabels:
                    print ("passed")
                    continue
                #url = 'http://dbpedia.org/resource/Cologne'
                print(cnt,url)
                DBlabels = get_DBPedia_DE_label(url,'en')
                labelsSet=list(set(DBlabels))
                synonyms=get_synonyms_wordnet(url[url.rfind('/')+1:],'en')
                labelsSet=labelsSet+synonyms
                uriLabels[url]=labelsSet
                
                writer.writerow([url.encode('utf-8'),uriLabels[url]])