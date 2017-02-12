# Import our Twitter library
import tweepy
import subprocess # For running commands

# Add in a Stream class to get tweets as soon as they're posted
class MyStreamListener(tweepy.StreamListener):

	# On receiving a tweet, print the image URL and tweet id
	def on_status(self, status):
		image_url = "User did not post an image" # Changes if they did
		out = "You need to post an image."

		# Can cause an exception if the person 
		# does not post with an image
		try:
			image_url = status.entities['media'][0]['media_url_https']
		except:
			pass # If it errors, it will use the above image_url

		tweet_id = status.id
		username = status.author._json['screen_name']
		print('image url:' + image_url)
		print('tweet id: ' + str(tweet_id))
		print('username: ' + username)

		# Put code for talking to our AI here
		# python3 ./isitoffensive image_url
		if "User did not post an image" not in image_url:
			process = subprocess.Popen(['/usr/bin/python3', '/home/ubuntu/TwitterBot/isitoffensive.py', image_url], stdout=subprocess.PIPE)
		# We don't need stderr, since the AI script doesn't
		# write there

		# Well we know the image URL is right, let's print
		# Out what we're getting in the other script.

		# That runs the isitoffensive scripts Greg and I made,
		# and it will return some text to tweet

		# This will grab the output and store it in a variable
		# called out, let's see what's stored there when we 
		# check the tweeted image
			out = process.communicate()[0].decode("utf-8")

		# Add username to output
		out = '@' + username + ' ' + out

		print('We will tweet: ' + str(out))

		# Reply based on above response from the AI here
		
		# Get a random happy image
		hi_filepath = '/home/ubuntu/images/nonoffensive/'
		hi_filename = 'happy.jpg'
		happy_image = hi_filepath + hi_filename
		# I sort of deleted all our non-offensive images
		# To save space, so we'll need to download some more

		# Send the reply
		api.update_with_media (happy_image, status=out, in_reply_to_status_id=tweet_id)

		print('Reply sent')

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
myStream.filter(track=['#IsThisOffensive', '#AmIOffensive'], async=True)


