#!/usr/local/bin/python2.7

import sys
import cgi
import MySQLdb

import dbconn
import cgi_utils_sda
from ssunier_dsn import DSN
from decimal import Decimal

def getCursor(database):
    DSN['database'] = database
    conn = dbconn.connect(DSN)
    return conn.cursor(MySQLdb.cursors.DictCursor)

#********Methods for inserting a recipe*******************

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
    #print "Inserted title: {title},addedby: {addedby},totaltime: {totaltime},and instructions: {instructions} into recipe table".format(title=title,addedby=addedby,totaltime=totaltime,instructions=instructions)

def ingredientExists(cursor,name,unit):
    hasIngredient = False
    data = (name,unit,)
    cursor.execute('SELECT id FROM ingredient WHERE name = %s and unit = %s',data)
    row = cursor.fetchone()
    if row != None:
        hasIngredient = True
    return hasIngredient

def insertToIngredient(cursor,name,unit):
    data = (name,unit,)
    cursor.execute('INSERT INTO ingredient(name,unit) VALUES (%s,%s)',data)
    #print "Inserted {name} with {unit} as its unit into ingredient table".format(name=name,unit=unit)

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
    #print "Inserted {quantity} {ingredient_name} for {recipe_title} into recipe quantity table.".format(quantity=quantity,ingredient_name=ingredient_name, recipe_title=recipe_title)

def processInsertRequest(cursor,database,form_data):
    msg = ''
    inputFeedback = checksRequiredFields(database,form_data)
    
    #if the user entered values for all the required fields
    if inputFeedback == '':
        title = form_data.getfirst('title')
        totaltime = form_data.getfirst('total-time')
        addedby = form_data.getfirst('addedby')
        instructions = form_data.getfirst('instructions')

        #inserts new recipe if it does not already exist
        if recipeExists(cursor,title):
            msg += '<p> Recipe with title ' + title + ' already in database.'
        else: 
            insertToRecipe(cursor,title,addedby,totaltime,instructions)
            msg += '<p> Recipe with title ' + title + ' not in database; inserted new entry.'
            
            for i in range(1,11):
                if 'quantity' + `i` in form_data and 'name' + `i` in form_data and 'unit' + `i` in form_data:
                    quantity = form_data.getfirst('quantity' + `i`)
                    name = form_data.getfirst('name' + `i`)
                    unit = form_data.getfirst('unit' + `i`)
		    #Checks to see if recipe's ingredients already exists in the database
                    if ingredientExists(cursor,name,unit):
                        msg +=  '<p>Ingredient with name ' + name + ' and unit ' + unit + ' already in database.'
                    else:
                        insertToIngredient(cursor,name,unit)
                        msg += '<p>Ingredient with name ' + name + ' and unit ' + unit + ' not in database; inserted new entry.'

                    #Updates the recipe quantity table with ingredients of this new recipe
                    insertToRecipeQuantity(cursor,title,name,quantity)
                    msg +=  '<p>Updated recipe quantity table.'
    else:
        msg += inputFeedback
    return msg
        

    


#*******Methods for searching a recipe***********

#returns as a tuple the values of all the fields that the user completed while searching for recipes
def getFormInputs(database,form_data):
    inputTuple = tuple();
    if 'title' in form_data:
        inputTuple += ('%' + form_data.getfirst('title') + '%',)
    if 'addedby' in form_data:
        inputTuple += (form_data.getfirst('addedby'),) 
    if 'total-time' in form_data:
        inputTuple += (form_data.getfirst('total-time'),)
    if 'instructions' in form_data: 
        inputTuple += ('%' + form_data.getfirst('instructions') + '%',)
    return inputTuple

#sets the end of the search query based on the fields that the user completed while searching for recipes
def setEndQuery(database,form_data):
    inputString = '';
    if 'title' in form_data:
        inputString += 'title LIKE %s AND '
    if 'addedby' in form_data:
        inputString += 'addedby = %s AND '
    if 'total-time' in form_data:
        inputString += 'totaltime <= %s AND '
    if 'instructions' in form_data:
        inputString += 'instructions LIKE %s AND '
    length = len(inputString) - 5
    return inputString[0:length]

def getIngredientFormInputs(database,form_data):
    inputTuple = tuple();
    if 'ingredient1' in form_data:
        inputTuple += ('%' + form_data.getfirst('ingredient1') + '%',)
    if 'ingredient2' in form_data:
        inputTuple += ('%' + form_data.getfirst('ingredient2') + '%',) 
    if 'ingredient3' in form_data:
        inputTuple += ('%' + form_data.getfirst('ingredient3') + '%',)
    if 'ingredient4' in form_data: 
        inputTuple += ('%' + form_data.getfirst('ingredient4') + '%',)
    return inputTuple

def setIngredientEndQuery(database,form_data):
    inputString = '';
    if 'ingredient1' in form_data:
        inputString += 'first.name LIKE %s AND '
    if 'ingredient2' in form_data:
        inputString += 'second.name LIKE %s AND '
    if 'ingredient3' in form_data:
        inputString += 'third.name LIKE %s AND '
    if 'ingredient4' in form_data:
        inputString += 'fourth.name LIKE %s AND '
    length = len(inputString) - 5
    return '(' + inputString[0:length] + ')'

def processSearchRequest(cursor,cursor2,database,form_data):
    msg = ''

    #title is a required field for searching
    if 'title' in form_data:

        #gets the search terms that the user provided for the recipe table (i.e. title,addedby,totaltime and instructions)
        recipe_data = getFormInputs(database,form_data)
        #sets the end of the prepared query based on the search terms the user provided
        recipe_endQuery = setEndQuery(database,form_data) 
     
        #Step 1: finds any matching recipes based on title,addedby,totaltime and/or instructions
        cursor.execute('SELECT rid,title,addedby,totaltime,instructions FROM recipe WHERE ' + recipe_endQuery,recipe_data)
        row = cursor.fetchone()
        if row == None: 
            msg += 'No matches found'
            return msg
              
        #Step 2: if the user provided ingredients as search inputs, check to see if these ingredients are
        #in any of the recipes found in Step 1
        while row != None:
            rid = '{rid}'.format(**row)
            ingredient_data = getIngredientFormInputs(database,form_data)
            matchesIngredient = False;
            if ingredient_data != tuple():
                ingredient_endQuery = setIngredientEndQuery(database,form_data)
                cursor2.execute('DROP TABLE if exists recipeWithIngredients')
                cursor2.execute('CREATE TABLE recipeWithIngredients as select recipe.rid,title,name from recipe,recipequantity,ingredient where recipequantity.rid = recipe.rid and recipequantity.id = ingredient.id and recipe.rid = %s', (rid,))
                cursor2.execute('SELECT recipe.rid FROM recipe,recipeWithIngredients as first,recipeWithIngredients as second, recipeWithIngredients as third, recipeWithIngredients as fourth WHERE recipe.rid = first.rid AND recipe.rid = second.rid AND recipe.rid = third.rid AND recipe.rid = fourth.rid AND ' + ingredient_endQuery,ingredient_data)
                row2 = cursor2.fetchone()
                if row2 != None:
                    matchesIngredient = True
               
        #Step 3: At this point, matching recipes (if any) have been found from step 1 or step 2.
        #Stores information about matching recipes in a message to the user
            if (matchesIngredient or (ingredient_data == tuple())):
                rid = '{rid}'.format(**row)
                title = '{title}'.format(**row)
                addedby = '{addedby}'.format(**row)
                totaltime =  '{totaltime}'.format(**row)
                instructions = '{instructions}'.format(**row)
                msg += '<p> Recipe ID: ' + rid + "<p> Title: " + title + "<p> Addedby: " + addedby + "<p> Totaltime: " + totaltime

                #gets ingredients of the recipe
                msg += '<p> Ingredients: '
                data = (rid,)
                cursor2.execute('SELECT quantity,unit,name FROM recipe,ingredient,recipequantity WHERE recipequantity.rid = recipe.rid AND recipequantity.id = ingredient.id AND recipe.rid = %s',data)
                row3 = cursor2.fetchone()
                while row3 != None:
                    quantity = '{quantity}'.format(**row3)
                    unit = '{unit}'.format(**row3)
                    name = '{name}'.format(**row3)
                    msg += "<p>" + quantity + " " + unit + " " + name 
                    row3 = cursor2.fetchone()
                msg += "<p> Instructions: " + instructions
                msg += "<p>**************************************"
            row = cursor.fetchone() #gets the next matching recipe
    else:
        msg += 'Please input a title for searching.'
    return msg

#**************Methods for viewing and updating the fridge*********************

def viewFridgeContents(cursor,fid):
    msg = ''
    data = (fid,)
    cursor.execute('SELECT quantity,unit,name FROM fridge,fridgequantity,ingredient WHERE fridgequantity.fid = fridge.fid AND fridgequantity.id = ingredient.id AND fridge.fid = %s ORDER BY name',data)
    row = cursor.fetchone()
    if row != None:
        msg += 'The contents of your updated fridge is listed alphabetically below:'
    else:
        msg += 'Your fridge is empty.'
        return msg

    while row != None:
        quantity = '{quantity}'.format(**row)
        unit = '{unit}'.format(**row)
        name = '{name}'.format(**row)
        msg += "<p>" + quantity + " " + unit + " " + name 
        row = cursor.fetchone()
    return msg

def updateFridgeQuantity(cursor,fid,ingredient_name,quantity):
    msg = ''

    #gets ingredient ID from name
    data = (ingredient_name,)
    cursor.execute('SELECT id FROM ingredient WHERE name = %s',data)
    row = cursor.fetchone()
    ingredient_id = '{id}'.format(**row)
   
    #checks to see if the ingredient already exists in the fridge
    data = (fid,ingredient_id,)
    cursor.execute('SELECT quantity FROM fridgequantity WHERE fid = %s AND id = %s',data)
    row = cursor.fetchone()

    if row == None: 
        data = (fid,ingredient_id,quantity,)
        cursor.execute('INSERT INTO fridgequantity(fid,id,quantity) VALUES (%s,%s,%s)',data)
        msg += 'Ingredient ' +  ingredient_name + ' does not already exist in the fridge; added new entry.'
    else:
        old_quantity = '{quantity}'.format(**row) 
        new_quantity = Decimal(old_quantity) + Decimal(quantity)
        data = (new_quantity,fid,ingredient_id,)
        cursor.execute('UPDATE fridgequantity SET quantity = %s WHERE fid = %s AND id = %s',data)
        msg += 'Ingredient ' + ingredient_name + ' already exists in the fridge; updated quantity to ' + str(new_quantity) + '.'

    return msg

def updateAndViewFridge(cursor,database,form_data):
    msg = ''
    
    if 'fid' in form_data: 
        fid = form_data.getfirst('fid')
        for i in range(1,5):
            if 'quantity' + `i` in form_data and 'name' + `i` in form_data and 'unit' + `i` in form_data:
                quantity = form_data.getfirst('quantity' + `i`)
                name = form_data.getfirst('name' + `i`)
                unit = form_data.getfirst('unit' + `i`)
            
                #Checks to see if ingredient already exists in ingredient table
                if ingredientExists(cursor,name,unit) == False:
                    insertToIngredient(cursor,name,unit)
                    #msg += '<p>Ingredient with name ' + name + ' and unit ' + unit + ' not in ingredients table; inserted new entry.'

                #Updates the fridge quantity table with newly added ingredients
                print updateFridgeQuantity(cursor,fid,name,quantity)                
        print viewFridgeContents(cursor,fid)

    else: 
        msg += 'Fridge ID is required'
    return msg
            
def main():
    cursor = getCursor('ssunier_db') 
    #insertToRecipe(cursor,'Orange2',33,60,'Step is blah')
    #print recipeExists(cursor,'Orange')
    #insertToRecipeQuantity(cursor,'Orange','flour',4)

if __name__ == '__main__':
    main()
    #print main(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5])
