#!bam/bin/python

import requests
import re
from random import randint
import json

url_gallica = "http://gallica.bnf.fr/"

def get_xml_gallica():
    request_url = url_gallica + "SRU?operation=searchRetrieve&exactSearch=false&collapsing=true&version=1.2&query=(dc.type%20all%20%22partition%22)&suggest=10'"
    response = requests.get(request_url)
    return response

def get_ark(xml):
    ark = []
    xml = xml.split("\n")
    for line in xml:
        match_obj = re.search(r'<dc:identifier>http://gallica.bnf.fr/(.*)<[/]dc:identifier>', line)
        if match_obj:
            ark.append(match_obj.group(1))
    return ark

def get_page(arks):
    for ark in arks:
        print("Retrieve ark" + ark)
        request_url = 'http://gallica.bnf.fr/iiif/' + ark + '/manifest.json'
        response =  requests.get(request_url)
        if response.status_code == 200:
            manifest = json.loads(response.content)
            for image in manifest['sequences']:
                url_image = image['canvases'][0]['images'][0]['resource']['@id']
                response = requests.get(url_image)
                with open('files/' + str(randint(0,1000)) + '.jpg', 'wb') as f:
                    print('Save file' + ark)
                    f.write(response.content)


xml = get_xml_gallica()
print get_page(get_ark(xml.content))
