#!/usr/bin/env python
#encoding: utf-8

# Name: Sheridan Sunier
# Project: Kitchen Corner
# Last Modified: 4.11.2014

"""
	get_recipes.python
	Python module for quering the Yummly API
	Returns a json file of multiple recipes
"""

import os, sys
from yummly import Client
import re,string
from collections import defaultdict

def stop_for_error():
    print "There was an HTTP error. You might want to try back in one hour."
    sys.exit(-1)

def split(recipe):
	i = defaultdict(lambda : defaultdict())
	p = '^((\d+( \d+/\d+)?)|(\d+/\d+))( (.+))?$'

	print "hello"

 	# for some reason when I make verbose it stops working... idk why
 	"""
		^				# beginning of string
		((\d+			# digit in range 0-9 1 or more times
			( \d+/		# matches any decimal digit in the second group
				\d+)	# matches any decimal digit in the thrid group (none)
				?)		# match expression in capture
		|				# or
		(\d+/			# more decimal matching! (should be none)
			\d+))		# more decimal matching in this group (could be none)
		( (.+))			# the remaining string (group 5)
		?				# creates groups
		$				# end of string
	"""
	for ingred in recipe.ingredientLines:
		m = re.match(p, ingred)
		#print len(m.groups())
		print m.group(5)
		try:
			x = getMeasurement(m.group(5))
			print x
			if x is None:
				i[m.group(5)][m.group(1)] = ""
			else:
				cleaned = removeMeasurement(m.group(5),x)
				i[cleaned][m.group(1)] = x
		
		except:
			print "exception inside split"
		print i


"""
	Given the remaining string, separate the measurement if it is in the set
	of measurements declared at the top of this file.  If there is no matching
	measurement, then set the unit to be none.
"""
def getMeasurement(group):
	print group
	value = None
	for k in re.findall('\w+', group):
		if k in meaSet:
			value = re.sub("s$", "",k)
			#print meaSet
	return value

def removeMeasurement(group, measurement):
	clean = ""
	for k in re.findall('\w+', group):
		if k in meaSet:
			continue
		clean += k + " "
	return clean

def main(query):
	"""Collect recipes that match your search query
	"""
	TIMEOUT = 10.0
	RETRIES = 0
	client = Client(api_id='d9efc743', api_key='bbb0c1439402e1181312a67278a37342', timeout=TIMEOUT, retries=RETRIES)

	try:
		search = client.search(q)
		l = len(search)
		for m in range(1):
			print m
			match = search.matches[m]
			#print match
			recipe = client.recipe(match.id)
			try:
				split(recipe)
			except:
				print "error when using split"		
	except:
		"there were no recipes fitting that descripton"


if __name__=="__main__":
	try:
		q = sys.argv[1]
	except:
		print "Usage enter a query"
		sys.exit(-1)
	main(q)






