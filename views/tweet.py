import json
from uuid import uuid4
from datetime import datetime

class TweetHandler:
    def __init__(self) -> None:
        pass


    def load_data(self, route):
        route = "db/" + route + ".json"
        with open(route, "r", encoding = 'utf-8') as f:
            results = json.load(f)
            return results


    def save_data(self, route, data):
        route = "db/" + route + ".json"
        with open(route, "r+", encoding = 'utf-8') as f:
            f.seek(0)
            json.dump(data, f, indent=2, default=str)


    def update_data(self, route, data):
        route = "db/" + route + ".json"
        with open(route, "r+", encoding = 'utf-8') as f:
            f.truncate(0)
            f.seek(0)
            json.dump(data, f, indent=2, default=str)


    def delete_data(self, user_id, results):
        tweets_to_delete = []

        for en, find in enumerate(results):
            if find["by"] == str(user_id):
                tweets_to_delete.append(en)
        
        for deleting in reversed(tweets_to_delete):
            results.pop(deleting)

        return results


    def setup_tweet(self, results, tweet_dict):
        tweet_dict["tweet_id"] = uuid4()
        tweet_dict["created_at"] = datetime.now()
        tweet_dict["updated_at"] = tweet_dict["created_at"]

        results.append(tweet_dict)
        return tweet_dict, results
    

    def find_register(self, tweet_dict, results):
        found = False

        for find in results:
            if str(tweet_dict["by"]) == list(find.keys())[0]:
                found = True
                find[str(tweet_dict["by"])].append(tweet_dict["tweet_id"])
                return found, results
        return found, results


    def find_tweet(self, tweet_id, results):
        for find in results:
            if find["tweet_id"] == str(tweet_id):
                return find
        return False

    
    def find_all_tweets_user(self, results, user_id):
        tweets_found = []
        for find in results:
            if find["by"] == str(user_id):
                tweets_found.append(find)
        if tweets_found:
            return tweets_found
        else:
            return False