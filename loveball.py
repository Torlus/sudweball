from settings import consumer_key, consumer_secret
from settings import access_token, access_token_secret
import random
import time
import tweepy

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

me = api.me().id
print('# I am ' + str(me))

count = 0
last = 0
followers_info = {}
random.seed()
last_dm = 0


def handle(e):
    print(e.response)
    if str(e.response).find('429') >= 0:
        time.sleep(60)

while True:
    followers_list = []
    try:
        for follower in tweepy.Cursor(api.followers).items():
            fid = follower.id
            followers_list.append(fid)
            if fid not in followers_info.keys():
                followers_info[fid] = follower.screen_name
                print('# Following ' + str(fid))
                follower.follow()
    except tweepy.TweepError as e:
        print(e.response)
        if str(e.response).find('429') >= 0:
            time.sleep(5)
        continue
    print("# Followers list ", end='')
    print(followers_list)
    print("# Followers info ", end='')
    print(followers_info)

    length = len(followers_list)
    if length == 0:
        continue

    while True:
        index = random.randint(0, length - 1)
        current = followers_list[index]
        if length == 1 or current != last:
            break

    last = current
    count += 1
    text = "[" + str(count) + "] Je suis la SudWeb Love Ball! "
    text += "Remplis-moi avec un message, et j'irai porter l'amour auprès d'un autre!"

    print("# Sending message to " + followers_info[current])

    try:
        dm = api.send_direct_message(user_id=current, text=text)
        if dm.id > last_dm:
            last_dm = dm.id
    except tweepy.TweepError as e:
        handle(e)
        continue

    message = None
    for n in range(3):
        time.sleep(20)
        try:
            for dm in api.direct_messages(since_id=last_dm):
                if dm.id > last_dm:
                    last_dm = dm.id
                if dm.sender_id == current:
                    message = dm.text
                    break
        except tweepy.TweepError as e:
            handle(e)

    if message is None:
        text = "[" + str(count) + "] Tu dois être occupé(e)... Tant pis! A une prochaine! "
    else:
        message = '@' + followers_info[current] + ' ' + message
        print(message)
        log = open('love.log','a+')
        log.write(message + '\n')
        log.close()
        text = "[" + str(count) + "] Merci pour ta contribution, je poursuis mon chemin, et je reviendrai te voir!"

    try:
        api.send_direct_message(user_id=current, text=text)
    except tweepy.TweepError as e:
        handle(e)
        continue

    time.sleep(20)
