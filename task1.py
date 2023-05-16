import tweepy

# Setting up Twitter API authentication
consumer_key = "jAD89hWR1biQ0b0F2C5gh8pOu"
consumer_secret = "mTNDA71Ik8M9xlbFvgLEJ5J8Cm9jp6PfSZksm8wEBDFbollqnJ"
access_token = "1562211954537930752-92roBUcdoVcxFTwspLFDAnZHkML1Ly"
access_token_secret = "IJvfzfe0OMQVtKzGvpovaIDFpmosnlw3ZUzUjHEVZWxiW"
bearer_token = "AAAAAAAAAAAAAAAAAAAAAJb0nQEAAAAABnGUaFx19y9Ny9AI2i8%2FnvH7xV4%3D9iVbh3HLAq8xhIo0paI33rxRDqkU1Aj0DRp91W4YqlvKrbG0xY"

# Setting up tweepy API
client = tweepy.Client(bearer_token, 
                       consumer_key, 
                       consumer_secret, 
                       access_token, 
                       access_token_secret)

# Getting my own user information

user_fields = ["created_at", "pinned_tweet_id", "username", "id"]
my_user = client.get_me(user_fields=user_fields).data

# Getting userid, username, pinned tweet id, and created at date
user_id = my_user.id
username = my_user.username
pinned_tweet_id = my_user.pinned_tweet_id
created_at = my_user.created_at

#Printing the requested information
print("User ID: " + str(user_id))
print("Username: " + username)
print("Pinned Tweet ID: " + str(pinned_tweet_id))
print("Created at: " + str(created_at))





