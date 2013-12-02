import os
import pdb
import numpy as np
import math
import json

class Query:

	def __init__(self, data_path):
		self.R = 3959
		self.coordinates = 0
		self.locations = 0
		# tweet_data entry = [latitude, longitude, tweet]
		self.entry_length = 3 # 
		self.tweet_data = []

		# process data
		with open(data_path) as f:
			content = f.readlines()
			# l = json with 'time' 'text' 'location' 'coordinates'
			for l in content:
				j = json.loads(l)
				self.process_tweet(j)

	def count(self):
		return len(self.tweet_data), self.coordinates, self.locations

	def get_lat_lon(self, somestring):
		# call google API for lat, lon
		lat = 45.0
		lon = 45.0
		return math.radians(lat), math.radians(lon)

	def distance(self, lat1, lon1, lat2, lon2):
		return math.acos( (math.sin(lat1)*math.sin(lat2)) + (math.cos(lat1)*math.cos(lat2)*math.cos(lon1-lon2)) )*self.R

	def process_tweet(self, tweet):

		e = [None] * self.entry_length

		# coordinate 
		if not (tweet['coordinates'] == None):
			self.coordinates += 1
			print 'coordinates : ', self.coordinates, tweet['coordinates']['coordinates']
			# coord = map(lambda w: math.radians(float(w)), tweet['coordinates']['coordinates'].split(','))
			e[0] = tweet['coordinates']['coordinates'][1] # latitude (in rad)
			e[1] = tweet['coordinates']['coordinates'][0] # longitude (in rad)
			# e[2] = math.sin(coord[0])
			# e[3] = math.cos(coord[0])
			e[2] = tweet['text']
		# location
		elif not (tweet['location'].strip() == ''):
			self.locations += 1
			print 'locations : ', self.locations, tweet['location']
			lat, lon = self.get_lat_lon(tweet['location'].strip()) # (in rad)
			e[0] = lat
			e[1] = lon
			# e[2] = math.sin(lat)
			# e[3] = math.cos(lat)
			e[2] = tweet['text']
		else:
			#print "no coordinate/location data"
			return

		self.tweet_data.append(e)

	def query_tweet(self, latitude, longitude, radius):
		matches = []
		lat_rad = math.radians(latitude)
		lon_rad = math.radians(longitude)
		for t in self.tweet_data:
			dist = self.distance(lat_rad, lon_rad, t[0], t[1])
			if dist <= radius:
				matches.append(t)
		return matches


if __name__ == '__main__':
	q = Query('../twitDB.txt')
	pdb.set_trace()
	print 'done'