#!bam/bin/python

import requests
import re

url_gallica = "http://gallica.bnf.fr/"

def get_xml_gallica():
    request_url = url_gallica + "SRU?operation=searchRetrieve&exactSearch=false&collapsing=true&version=1.2&query=(dc.type%20all%20%22partition%22)&suggest=10'"
    response = requests.get(request_url)
    return response

def get_ark(xml):
    ark = []
    for line in xml:
        match_obj = re.search(r'<link>(.*)<[/]link>', xml)
        if match_obj:
             ark.append(match_obj.group(1))
    return ark

xml = get_xml_gallica()
print get_ark(xml.content)
