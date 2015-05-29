from settings import consumer_key, consumer_secret
from settings import access_token, access_token_secret

import tweepy

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

me = api.me().id
print(me)


followers = {}

for follower in tweepy.Cursor(api.followers).items():
    followers[follower.id] = follower.screen_name
    follower.follow()

print(followers)

# api.send_direct_message(user, 'Hello!')
try:
    api.send_direct_message(user_id=59873349, text='Hello world!')
except tweepy.TweepError as e:
    print(e.response)

# public_tweets = api.home_timeline()
for dm in api.direct_messages():
    print(dm)

