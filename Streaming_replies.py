"""

Following code, streams tweets of username 'x1' containing specific keywords and stores the replies to those tweets in a JSON file.

"""
from tweepy import TweepError
import json
from tweepy import API
from tweepy import Cursor
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import creden

class TwitterAuthenticator():
    
    def authenticate_twitter_app(self):
        auth = OAuthHandler(creden.consumer_key, creden.consumer_secret)
        auth.set_access_token(creden.access_token, creden.access_secret)
        return auth
    
class TwitterClient():
    """
    
    Class to get tweets from user timeline
    
    """
    def __init__(self,twitter_user=None):
        self.auth=TwitterAuthenticator().authenticate_twitter_app()
        self.twitter_client=API(self.auth)
        self.twitter_user=twitter_user
    
    def get_tweets_from_self_timeline(self,num_tweets,tweet_output_file,hash_tag_list):
        """
        Function to print tweets,retweets and store the replies to the tweets

        """
        
        for tweet in Cursor(self.twitter_client.user_timeline,id=self.twitter_user,tweet_mode="extended",exclude_replies=True).items(num_tweets):
            tweets=[]
            if all(x not in tweet.full_text for x in hash_tag_list):                 
                continue
            else :
                try :        #Prints the retweets of account x1, and stores the replies to those retweets
                    print("\n\n")
                    print("1.Retweet  " +tweet.retweeted_status.full_text)
                    for all_tweet in Cursor(self.twitter_client.search,q='to:x2', since_id=tweet.id_str).items(300):  # x2 is the username of the page,whose tweets user x1 is retweeting
                        if hasattr(all_tweet, 'in_reply_to_status_id_str'):
                            if (all_tweet.in_reply_to_status_id_str==tweet.retweeted_status.id_str):
                                tweets.append(all_tweet.text)
                except AttributeError:
                    print("\n\n")
                    print("1.Tweet  " +tweet.full_text)  #Prints the tweets of account x1
                    for all_tweet in Cursor(self.twitter_client.search,q='to:x1', since_id=tweet.id_str).items(300):  #Stores the replies to the tweets of account x1
                        if hasattr(all_tweet, 'in_reply_to_status_id_str'):
                            if (all_tweet.in_reply_to_status_id_str==tweet.id_str):
                                tweets.append(all_tweet.text)
                except TweepError:
                    print("Limit reached!!!")
            if len(tweets) != 0 :
                self.write_to_file(tweets,tweet_output_file)
    def write_to_file(self,replies,fileName):
        """
        Function stores the replies of tweets to a JSON file

        """
        file_path='./' + fileName
        with open(file_path,'a') as fp:
            json.dump(replies, fp)
        
if __name__=="__main__":
    hash_tag_list = [x for x in input("Enter the hash tag list to filter tweets(separated by commas): ").split(',')]    
    account_name=input("Enter account user name whose tweets you want to scrape?")
    twitter_client=TwitterClient(account_name)
    twitter_client.get_tweets_from_self_timeline(100,"search_results.json",hash_tag_list)
    