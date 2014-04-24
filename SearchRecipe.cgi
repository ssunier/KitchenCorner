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
    cursor2 = KitchenCorner.getCursor('skim22_db') 

    tmpl = cgi_utils_sda.file_contents('SearchRecipe.html')
    mess = ''  
    form_data = cgi.FieldStorage()

    print KitchenCorner.processSearchRequest(cursor,cursor2,'skim22_db',form_data)

    page = tmpl.format(message=mess)
    print page
