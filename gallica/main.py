#!bam/bin/python

import requests
import re
from random import randint
import json
import optparse
import mysql.connector as mariadb
import logging
from logging.handlers import RotatingFileHandler

logger = logging.getLogger()
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s')
file_handler = RotatingFileHandler('logs/gallica.log', 'a', 1000000, 1)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
logger.addHandler(stream_handler)

url_gallica = "http://gallica.bnf.fr/"
url_iiif = 'http://gallica.bnf.fr/iiif/'

connection = mariadb.connect(host='localhost', user='root', password='changeme', database='gallica')
cursor = connection.cursor()

def get_xml_gallica(query = ''):
    request_url = url_gallica + "SRU?operation=searchRetrieve&exactSearch=false&collapsing=true&version=1.2&query=(%28gallica%20all%20\"" + query + "\"%29%20and%20dc.type%20all%20\"partition\")&suggest=10'"
    logger.info("Generate query : " + request_url)
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
        logger.info("Retrieve ark" + ark)
        request_url = url_iiif + ark + '/manifest.json'
        response =  requests.get(request_url)
        if response.status_code == 200:
            manifest = json.loads(response.content)
            for metadata in manifest['metadata']:
                if not isinstance(metadata['value'], list):
                    cursor.execute("INSERT IGNORE INTO glc_metadata (ark,label,value) VALUES (%s,%s,%s)", (ark, metadata["label"], metadata["value"]))
            for image in manifest['sequences']:
                for canvas in image['canvases']:
                    for image in canvas['images']:
                        file_name = image['resource']['@id'].replace('/','_')
                        url_image = image['resource']['@id']
                        response = requests.get(url_image)
                        path_img = dest_dir + '/' + file_name;
                        with open(path_img, 'wb') as f:
                            logger.info('Save file in ' + path_img)
                            f.write(response.content)
                        cursor.execute("INSERT IGNORE INTO glc_partition (id,ark) VALUES (%s,%s)", (file_name, ark))
            connection.commit()

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
