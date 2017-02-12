# Import our Twitter library
import tweepy

# Add in a Stream class to get tweets as soon as they're posted
class MyStreamListener(tweepy.StreamListener):

	# On receiving a tweet, print the image URL and tweet id
	def on_status(self, status):
		image_url = "User did not post an image" # Changes if they did

		# Can cause an exception if the person 
		# does not post with an image
		try:
			image_url = status.entities['media'][0]['media_url_https']
		except:
			pass # If it errors, it will use the above image_url

		tweet_id = status.id
		print('image url:' + image_url)
		print('tweet id: ' + str(tweet_id))

		# Put code for talking to our AI here
		# python3 ./isitoffensive image_url

		# Reply based on above response from the AI here
	
	# If we get an error, handle it instead of crashing :)
	def on_error(self, status_code):
		# If we hit our rate limit cap
		if status_code == 420:
			return False

# Set up API keys
auth = tweepy.OAuthHandler('ih5fi9Ok9bsGSv8rJsuE1dQ4g','uu8jDA70qX6aRk0ncwrGgjuj98txbMcoxbjpU6yqCk0bKA3Bh2')
auth.set_access_token('830296557031350272-gydrr5kPF7bHEeBbuavGbY4wHINxfwO', 'DWVKLOImtno3eXi7SdyrqaNrzED3V8sp0Bei9poFXXZf6')

# Set up an API object
api = tweepy.API(auth)

# Create an instance of the stream class
# And login with our above auth object
myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)

# Listen for the #AmIOffensive hashtag
# async means it will grab new tweets while we can work on
# the ones it has grabbed so far
myStream.filter(track=['#AmIOffensive'], async=True)


