#/usr/bin/env python

# Import sys for reading url from command line
import sys
import random

# Import AI API
from clarifai import rest
from clarifai.rest import ClarifaiApp
from clarifai.rest import Image as ClImage

# Get the url from the command line
url = sys.argv[1]

# DEBUG: Print out given URL
#print('We got URL: ' + url)

# If we get a \n char, remove it
url = url.rstrip()

# Create an 'app' object based off our Clarifai API Key
# This gives us access to the API
app = ClarifaiApp("J776KJ-Ob-GtKnS_jylW-yxWrT-gmDrHfRLzeJG-", "1eevauzVbedZnKdcuMCGoZHtzLVSaJ5ndeANzdBG")

# Load in their model to distinguish NSFW images
model = app.models.get("isoffensive")

# Give it an image
image = ClImage(url=url)

# Get probability it is NSFW
response = model.predict([image])

# Get how NSFW it thinks it is and store in a variable
nsfwAmount = response["outputs"][0]["data"]["concepts"][1]["value"]

# Great quotes from jesus himself
offended_Response = ["There are kids on here you know", "Sorry", "That's a little too much, have this instead", "No, not again :(", "Spicy"]
not_Offended_response = ["This is not offensive", "This is okay", "Woah, that was a close one",	"I hope the AI isn't wrong"]

# If the nsfw probability is less than 0.15, it is most likely SFW
# If the nsfw probability is greater than 0.85, it is most likely NSFW
if nsfwAmount > 0.15:
	# Pick a random offended response
	text_response = random.choice(offended_Response)

	# Is this considered a reply? Or just a mention..
	#api.update_status('@<username> ' + text_Response, tweetId)

	# This will insert the random response into the tweet, along
	# With the probability
	print (text_response + ", AI found image to be: " + str(nsfwAmount) + "% offensive!")

else:
	# Pick a random non-offended response
	text_response = random.choice(not_Offended_response)
	print (text_response + ", AI found image to be: " + str(nsfwAmount) + "% offensive.")
