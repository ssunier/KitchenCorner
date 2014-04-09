#!/usr/local/bin/python2.7

import sys
import cgi
import MySQLdb

import dbconn
import cgi_utils_sda
from skim22_dsn import DSN

def getCursor(database):
    DSN['database'] = database
    conn = dbconn.connect(DSN)
    return conn.cursor(MySQLdb.cursors.DictCursor)

def checksRequiredFields(database,form_data):
    msg = ''
    if 'title' not in form_data:
        msg += '<p>Title is required.'
    if 'addedby' not in form_data:
        msg += '<p>Addedby is required.'
    if 'total-time' not in form_data:
        msg += '<p>Total time is required.'
    if 'quantity1' not in form_data:
        msg += '<p>Quantity is required.'
    if 'name1' not in form_data:
        msg += '<p>Name is required.'
    if 'instructions' not in form_data:
        msg += '<p>Instructions are required.'
    if msg != '':
        msg += '<p>Please resubmit with information for the required fields.'
    return msg
    
def recipeExists(cursor,title):
    hasRecipe = False
    data = (title,)
    cursor.execute('SELECT rid FROM recipe WHERE title = %s',data)
    row = cursor.fetchone()
    if row != None:
        hasRecipe = True
    return hasRecipe

def insertToRecipe(cursor,title,addedby,totaltime,instructions):
    data = (title,addedby,totaltime,instructions,)
    cursor.execute('INSERT INTO recipe(title,addedby,totaltime,instructions) VALUES (%s,%s,%s,%s)',data)

def ingredientExists(cursor,name):
    hasIngredient = False
    data = (name,)
    cursor.execute('SELECT id FROM ingredient WHERE name = %s',data)
    row = cursor.fetchone()
    if row != None:
        hasIngredient = True
    return hasIngredient

def insertToIngredient(cursor,name,unit):
    data = (name,unit,)
    cursor.execute('INSERT INTO ingredient(name,unit) VALUES (%s,%s)',data)

def insertToRecipeQuantity(cursor,recipe_title,ingredient_name,quantity):
    #gets recipe ID from title
    data = (recipe_title,)
    cursor.execute('SELECT rid FROM recipe WHERE title = %s',data)
    row = cursor.fetchone()
    recipe_id = '{rid}'.format(**row)
    
    #gets ingredient ID from name
    data = (ingredient_name,)
    cursor.execute('SELECT id FROM ingredient WHERE name = %s',data)
    row = cursor.fetchone()
    ingredient_id = '{id}'.format(**row)
   
    data = (recipe_id,ingredient_id,quantity,)
    cursor.execute('INSERT INTO recipequantity(rid,id,quantity) VALUES (%s,%s,%s)',data)
    
def main():
    cursor = getCursor('skim22_db') 
    #insertToRecipe(cursor,'Orange2',33,60,'Step is blah')
    #print recipeExists(cursor,'Orange')
    #insertToRecipeQuantity(cursor,'Orange','flour',4)

if __name__ == '__main__':
    main()
    #print main(sys.argv[1],sys.argv[2],sys.argv[3])
