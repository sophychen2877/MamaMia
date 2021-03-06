#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
import boto.dynamodb2
from boto.dynamodb2.table import Table
from textblob import TextBlob



#Variables that contains the user credentials to access Twitter API
consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''

def get_sentiment(tweet):
    return TextBlob(tweet).sentiment
    

#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def on_data(self, data):
        tweet = json.loads(data)
        print (tweet['text'])
        try:
                tweets.put_item(data={
                 'id': str(tweet['id']),
                 'username': tweet['user']['name'],
                 'screen_name': tweet['user']['screen_name'],
                 'tweet': str(tweet['text'].encode('ascii','ignore')),
                 'followers_count': tweet['user']['followers_count'],
                 'location': str(tweet['user']['location']),
                 'geo': str(tweet['geo']),
                 'created_at': tweet['created_at'],
                 'sentiment': str(get_sentiment(str(tweet['text'].encode('ascii','ignore'))),
                 'subjectivity': str(get_sentiment(str(tweet['text'].encode('ascii','ignore'))).subjectivity),
                 'polarity': str(get_sentiment(str(tweet['text'].encode('ascii','ignore'))).polarity)
                 })
        except (AttributeError, Exception) as e:
                print (e)
        return True

    def on_error(self, status):
        print (status)

if __name__ == '__main__':

    conn = boto.dynamodb2.connect_to_region(region_name='',
                                            aws_access_key_id='',
                                            aws_secret_access_key='')
                                            

    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    tweets = Table('tweets_ft',connection=conn)

    #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    stream.filter(track=['Zoom'])
