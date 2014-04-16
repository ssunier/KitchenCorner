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

    tmpl = cgi_utils_sda.file_contents('InsertRecipe.html')
    msg = ''  
    form_data = cgi.FieldStorage()
    
    #KitchenCorner.searchRecipeTable(cursor,'skim22_db',form_data)

    title = form_data.getfirst('title')
    totaltime = form_data.getfirst('total-time')
    addedby = form_data.getfirst('addedby')
    #for i in range (0,4):
    quantity = form_data.getfirst('quantity1')
    name = form_data.getfirst('name1')
    unit = form_data.getfirst('unit1')
    instructions = form_data.getfirst('instructions')

    inputFeedback = KitchenCorner.checksRequiredFields('skim22_db',form_data)

    #If the user entered values for all the required fields
    if inputFeedback == '':
       #Checks to see if recipe with the same title already exists
        if KitchenCorner.recipeExists(cursor,title):
            print "<p>Recipe already in database."
        else:
            KitchenCorner.insertToRecipe(cursor,title,addedby,totaltime,instructions)
	    print "<p>Recipe not in database; inserted new entry."

	    #Checks to see if the recipe's ingredients already exist
	    if KitchenCorner.ingredientExists(cursor,name):
                print  "<p>Ingredient already in database."
            else:
                KitchenCorner.insertToIngredient(cursor,name,unit)
            	print "<p>Ingredient not in database; inserted new entry."

	    #Updates the recipe quantity table with ingredients of this new recipe
	    KitchenCorner.insertToRecipeQuantity(cursor,title,name,quantity)
	    print "<p>Updated recipe quantity table."
	    
    #else:
	 #print inputFeedback


    page = tmpl.format(message=msg)
    print page
