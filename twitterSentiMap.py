import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob
from geopy.geocoders import Nominatim
import csv
import os

'https://www.geeksforgeeks.org/twitter-sentiment-analysis-using-python/'

'Bearer Token --> AAAAAAAAAAAAAAAAAAAAAKxyeQEAAAAAh3DhqFBl%2F3v9m3GRPkWIYamvw5A%3D6JIpO39pEwlbeWUrDZTKYPkcT5rtLWrXBm9IdkAQAGI7wBTWt2'

class TwitterClient(object):
	'''
	Generic Twitter Class for sentiment analysis.
	'''
	def __init__(self):
		'''
		Class constructor or initialization method.
		'''
		# keys and tokens from the Twitter Dev Console
		consumer_key = 'YGPWEW8ri0w6oOWpDjl58cbKf'
		consumer_secret = 'P0oGSkE4POvwMFMhdV5SUmMXjz9ZDkT5clFfNSDomrUgdAJiMM'
		access_token = '3227102551-9deCxw4wwzPGdFeQhxI9m6rucv7GLdONF3YizfO'
		access_token_secret = 'hM0cTPWZXbY5IXueXhq6FUbANI69YV2zMqddmcyzHDDBR'

		# attempt authentication
		try:
			# create OAuthHandler object
			self.auth = OAuthHandler(consumer_key, consumer_secret)
			# set access token and secret
			self.auth.set_access_token(access_token, access_token_secret)
			# create tweepy API object to fetch tweets
			self.api = tweepy.API(self.auth)
		except:
			print("Error: Authentication Failed")

	def clean_tweet(self, tweet):
		'''
		Utility function to clean tweet text by removing links, special characters
		using simple regex statements.
		'''
		return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]\w+:\/\/\S+)", " ", tweet).split())

	def get_tweet_sentiment(self, tweet):
		# create TextBlob object of passed tweet text
		analysis = TextBlob(self.clean_tweet(tweet))
		# set sentiment
		if analysis.sentiment.polarity > 0:
			return 'positive'
		elif analysis.sentiment.polarity == 0:
			return 'neutral'
		else:
			return 'negative'	

	def average_sentiment(self, tweets):
		'''
		Utility function to classify sentiment of passed tweet
		using textblob's sentiment method
		'''
		average_sentiment = 0
		num_tweets = 0
		for tweet in tweets: 
			# create TextBlob object of passed tweet text
			analysis = TextBlob(self.clean_tweet(tweet))
			print(analysis.sentiment.polarity)
			if analysis.sentiment.polarity != 0:
				num_tweets += 1
				average_sentiment += analysis.sentiment.polarity
			
		return (average_sentiment / num_tweets)

	def get_trends(self): 
		
		closest_trends = self.api.closest_trends(28.3772, -81.5707)
		
		return closest_trends
	
	def get_sentiment(self, query, count): 
		tweets = []
		try:
			# call twitter api to fetch tweets
			fetched_tweets = self.api.search_tweets(q = query, count = count, result_type = 'mixed')
			# parsing tweets one by one
			# empty dictionary to store required params of a tweet
			

			for tweet in fetched_tweets:
				parsed_tweet = {}
				# saving text of tweet
				parsed_tweet['text'] = tweet.text
				# empty dictionary to store required params of a tweet
				if tweet.retweet_count > 0:
				# if tweet has retweets, ensure that it is appended only once
					if parsed_tweet not in tweets:
						tweets.append(parsed_tweet)
				else:
					tweets.append(parsed_tweet)
			print(tweets)
			return tweets

		except tweepy.errors.TweepyException as e:
			# print error (if any)
			print("Error : " + str(e))
	
	def get_tweets(self, query, count):
		'''
		Main function to fetch tweets and parse them.
		'''
		# empty list to store parsed tweets
		tweets = []

		try:
			# call twitter api to fetch tweets
			fetched_tweets = self.api.search_tweets(q = query, count = count, result_type = 'mixed')
			# parsing tweets one by one
			# print(fetched_tweets)
			f = open('zion_park.txt', 'w')
			for tweet in fetched_tweets:
				# empty dictionary to store required params of a tweet
				# parsed_tweet = {}
				# saving text of tweet
				# print("\n\n",tweet.text,"\n\n")
				parsed_tweet = tweet.text
				
				if tweet.retweet_count > 0:
					# if tweet has retweets, ensure that it is appended only once
					if parsed_tweet not in tweets:
						# tweets.append(parsed_tweet)
						f.write("\n" + str(tweet.text) + "\n")
				else:
					tweets.append(parsed_tweet)
				# saving sentiment of tweet
				#parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)

				# appending parsed tweet to tweets list
				
			# return parsed tweets
			# print(len(tweets))
			return fetched_tweets

		except tweepy.errors.TweepyException as e:
			# print error (if any)
			print("Error : " + str(e))
	
def get_location(query): 
		geocoder = Nominatim(user_agent = "SentimentAnalysis")
		location = geocoder.geocode(query)
		# print(location.address)
		return((location.latitude, location.longitude))

def main():
	# creating object of TwitterClient Class
	api = TwitterClient()


	disney = ["Tweets"]
	queries = ["Disney World", "Smithsonian Museum", "Gateway Arch", "Busch Stadium", "Zion National Park", "Grand Canyon", "Statue of Liberty", "Tampa Bay", "Orlando", "Charleston", "Miami", "Myrtle Beach", "The Alamo", "Panama City Beach", "Times Square", "Las Vegas", "Yosemite National Park", "New Orleans"]
	disney_tweets = []
	# calling function to get tweets
	for query in queries: 
		location = get_location(query)
		print(location)
	# f = open('%s', 'w',)
	# tweets = api.get_tweets(query = "Zion National Park", count = 100)
	# num_tweets = 0
	# f = open('disneytweetsjson.txt', 'w')
	# for tweet in tweets: 
	# f.write(str(tweets))	
	# print(disney_tweets)
		# ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
		# print("Positive tweets percentage: {} % \
		# 	".format(100*len(ptweets)/len(tweets)))
		
		# ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
		# print("Neutral tweets percentage: {} % \
		# 	".format(100*(len(tweets) -(len( ntweets )+len( ptweets)))/len(tweets)))
		
		# print("Negative tweets percentage: {} % \
		# 	".format(100*len(ntweets)/len(tweets)))
		# average_sentiment = api.average_sentiment(tweets)
		# print(average_sentiment)
		
		# print(average_sentiment)
	# with open('disney_tweets.csv', 'w') as f:

    # 	# using csv.writer method from CSV package
	# 	write = csv.writer(f)

	# 	write.writerow(disney)
	# 	write.writerow(disney_tweets)
		
	
if __name__ == "__main__":
	# calling main function
	main()
