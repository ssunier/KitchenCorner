#!/usr/local/bin/python2.7

import sys

import cgi
import cgitb; cgitb.enable()
import cgi_utils_sda

import MySQLdb
from skim22_dsn import DSN
import dbconn
import KitchenCorner

if __name__ == '__main__':
    print 'Content-type: text/html\n'
    cursor = KitchenCorner.getCursor('skim22_db') 

    tmpl = cgi_utils_sda.file_contents('UpdateFridge.html')
    msg = ''  
    form_data = cgi.FieldStorage()
    
    page = tmpl.format(message=msg)
    print page