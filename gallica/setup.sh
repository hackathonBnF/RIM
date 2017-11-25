#!/bin/bash

virtualenv bam
source bam/bin/activate
pip install -r requirements.txt

mkdir db files logs
