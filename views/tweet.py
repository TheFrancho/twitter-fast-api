import json

class TweetHandler:
    def __init__(self) -> None:
        pass


    def load_data(self, route):
        route = "db/" + route + ".json"
        with open(route, "r", encoding = 'utf-8') as f:
            results = json.load(f)
            return results
    

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