#!/usr/bin/env python
#encoding: utf-8

# Name: Sheridan Sunier
# Project: Kitchen Corner
# Last Modified: 4.9.2014


"""
	clean_ingredient.py
	takes in the data from yummly api and cleans the ingredient lists
	so that the data is fit to be entered into our tables
"""

from yummly import Client
import sys, os
import re, string
from collections import defaultdict, Counter

# measurements are imported as a stoplist would be
measurements = [w.strip() for w in open('measurements.txt').readlines()]
meaSet = set(measurements)

"""
	Given a recipe, single out the quantities
	and separate from the rest of the ingredient string
"""
def split(recipe):
	i = defaultdict(lambda : defaultdict())

	p = '^((\d+( \d+/\d+)?)|(\d+/\d+))( (.+))?$'

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
		
		x = getMeasurement(m.group(5))

		if x is None:
			i[m.group(5)][m.group(1)] = ""

		else:
			cleaned = removeMeasurement(m.group(5),x)

			i[cleaned][m.group(1)] = x

	print i
	return i


"""
	Given the remaining string, separate the measurement if it is in the set
	of measurements declared at the top of this file.  If there is no matching
	measurement, then set the unit to be none.
"""
def getMeasurement(group):
	value = None
	for k in re.findall('\w+', group):
		if k in meaSet:
			value = re.sub("s$", "",k)
			break
	return value

def removeMeasurement(group, measurement):
	clean = ""
	for k in re.findall('\w+', group):
		if k in meaSet:
			continue
		clean += k + " "
	return clean


"""
Testing Data - Comment back out when done
"""
TIMEOUT = 5.0
RETRIES = 0

client = Client(api_id='d9efc743', api_key='bbb0c1439402e1181312a67278a37342', timeout=TIMEOUT, retries=RETRIES)

search = client.search('red curry paste')
match = search.matches[0]
recipe = client.recipe(match.id)

#print recipe


if __name__ == '__main__':
	split(recipe)



