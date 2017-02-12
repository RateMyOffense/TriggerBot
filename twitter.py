# Import our Twitter library
import random, tweepy, os
import subprocess # For running commands
import json # For processing JSON files

bio_start = "Post a tweet with #IsThisOffensive and I'll tell you if it is!"

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
		hi_filepath = '/home/ubuntu/images/kittens/'
		hi_filename = random.choice(os.listdir(hi_filepath))
		happy_image = hi_filepath + hi_filename

		# Send the reply
		api.update_with_media (happy_image, status=out, in_reply_to_status_id=tweet_id)

		print('Reply sent')

		# Add one to tweet counter
		
		# Get current count
		with open('stats.json', 'r') as data:
			stats = json.load(data)
			
		# Grab the current tweet amount
		curr_count = stats['total_tweets']

		# Grab the current offensive percentage
		off_percent = stats['offensive']

		# Determine new offensive %
		total_offensive_imgs = off_percent * curr_count
		if "offensive!" in image_url:
			# This was an offensive post
			off_percent = (total_offensive_imgs + 1) / (curr_count + 1)
		else:
			# Not offensive, don't increment
			off_percent = total_offensive_imgs / (curr_count + 1)

		# Save new offensive%
		stats['offensive'] = off_percent

		# Increment by 1
		stats['total_tweets'] = curr_count + 1
		curr_count  = curr_count + 1

		# Save new amount
		with open('stats.json', 'w') as data:
			data.write(json.dumps(stats))

		print ('\nNew Tweet Count: ' + str(curr_count))
		print ('\nNew Offensive Percentage: ' + str(off_percent))

		# Set new Bio and format % so it has no decimals
		bio = bio_start + " Images Scanned: " + str(curr_count) + " Offensive: " + "{0:.0f}".format(off_percent * 100) + "%"
		api.update_profile(description=bio)

	# If we get an error, handle it instead of crashing :)
	def on_error(self, status_code):
		# If we hit our rate limit cap
		if status_code == 420:
			return False

# Set up API keys
auth = tweepy.OAuthHandler('','')
auth.set_access_token('', '')

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


