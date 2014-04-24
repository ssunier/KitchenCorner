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

# TESTING
"""
TIMEOUT = 10.0
RETRIES = 0
client = Client(api_id='d9efc743', api_key='bbb0c1439402e1181312a67278a37342', timeout=TIMEOUT, retries=RETRIES)
search = client.search("curry")
match = search.matches[0]	
recipe = client.recipe(match.id)
"""

"""
	Given a recipe, single out the quantities
	and separate from the rest of the ingredient string
"""

class Clean(object):

	def __init__(self):
		self.recipe_ingred = defaultdict(lambda : defaultdict())

	def split(self, recipe):
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
			try:
				x = self.getMeasurement(m.group(5))
				if x is None:
					self.recipe_ingred[m.group(5)][m.group(1)] = ""
				else:
					cleaned = self.removeMeasurement(m.group(5),x)
					self.recipe_ingred[cleaned][m.group(1)] = x
			
			except:
				print "exception"
		print self.recipe_ingred
		return self.recipe_ingred


	"""
		Given the remaining string, separate the measurement if it is in the set
		of measurements declared at the top of this file.  If there is no matching
		measurement, then set the unit to be none.
	"""
	def getMeasurement(self, group):
		value = None
		for k in re.findall('\w+', group):
			if k in meaSet:
				value = re.sub("s$", "",k)
				#print meaSet
		return value

	def removeMeasurement(self, group, measurement):
		clean = ""
		for k in re.findall('\w+', group):
			if k in meaSet:
				continue
			clean += k + " "
		return clean

	#def main(recipe):
	#	try:
	#		split(recipe)
	#	except:
	#		print "something happened"


if __name__ == '__main__':
	c = Clean()
	c.split(recipe)

