#!bam/bin/python

import requests
import re
from random import randint
import json
import optparse
import mysql.connector as mariadb

url_gallica = "http://gallica.bnf.fr/"
url_iiif = 'http://gallica.bnf.fr/iiif/'

connection = mariadb.connect(host='localhost', user='root', password='changeme', database='gallica')
cursor = connection.cursor()

def get_xml_gallica(query = ''):
    request_url = url_gallica + "SRU?operation=searchRetrieve&exactSearch=false&collapsing=true&version=1.2&query=(%28gallica%20all%20\"" + query + "\"%29%20and%20dc.type%20all%20\"partition\")&suggest=10'"
    response = requests.get(request_url)
    if response.status_code == 200:
        return response.content
    return ''

def get_ark(xml):
    ark = []
    xml = xml.split("\n")
    for line in xml:
        match_obj = re.search(r'<dc:identifier>http://gallica.bnf.fr/(.*)<[/]dc:identifier>', line)
        if match_obj:
            ark.append(match_obj.group(1))
    return ark

def get_partition(arks, dest_dir):
    for ark in arks:
        print("Retrieve ark" + ark)
        request_url = url_iiif + ark + '/manifest.json'
        response =  requests.get(request_url)
        if response.status_code == 200:
            manifest = json.loads(response.content)
            for metadata in manifest['metadata']:
                if not isinstance(metadata['value'], list):
                    cursor.execute("INSERT IGNORE INTO glc_metadata (ark,label,value) VALUES (%s,%s,%s)", (ark, metadata["label"], metadata["value"]))
            connection.commit()
            for image in manifest['sequences']:
                for canvas in image['canvases']:
                    for image in canvas['images']:
                        file_name = image['resource']['@id'].replace('/','_')
                        url_image = image['resource']['@id']
                        response = requests.get(url_image)
                        with open(dest_dir + '/' + file_name, 'wb') as f:
                            print('Save file' + ark)
                            f.write(response.content)

parser = optparse.OptionParser()

parser.add_option('-d', '--dest',
    action="store", dest="dest",
    help="destination directory", default="files/")

parser.add_option('-q', '--query',
    action="store", dest="query",
    help="Query term", default="")

options, args = parser.parse_args()

xml = get_xml_gallica(options.query)
arks = get_ark(xml)
get_partition(arks, options.dest)
