from SPARQLWrapper import SPARQLWrapper, JSON, CSV
import pandas as pd
import webbrowser

sparql = SPARQLWrapper("http://dbpedia.org/sparql")
sparql.setQuery("""
prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
prefix dbo: <http://dbpedia.org/ontology/>
prefix dc: <http://purl.org/dc/elements/1.1/>
prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
select distinct ?name  ?time ?company ?link ?games ?description  
where {
?games   rdf:type  dbo:Software;
dbo:developer ?company;
foaf:homepage ?link;
dbo:abstract ?description;
dbo:releaseDate ?time;
rdfs:label    ?name 
FILTER((lang(?name)="en")&&(regex(?name,"League"))&&(lang(?description)="en"))
}order by ?games
""")

sparql.setReturnFormat(JSON)
result = sparql.query().convert()
# ?name  ?time ?compay ?link ?games ?description
table = []
head = result["head"]["vars"]

print("count of result:" + str(len(result["results"]["bindings"])))
for item in result["results"]["bindings"]:

    _item = []
    name = item["name"]["value"]
    _item.append(name)

    time = item["time"]["value"]
    _item.append(time)

    company = item["company"]["value"]
    _item.append(company)

    url = item["link"]["value"]
    _item.append(url)

    games = item["games"]["value"]
    _item.append(games)

    description = item["description"]["value"]
    _item.append(description)

    table.append(_item)

_table = pd.DataFrame(table, columns=(head[0], head[1], head[2], head[3], head[4],head[5]))
# print(_table)
#
h = _table.to_html()

with open("games1.html", 'w', encoding='utf-8') as f:
# with open(a, 'w', encoding='utf-8') as f:
    f.write(h)
webbrowser.open('games1.html')
