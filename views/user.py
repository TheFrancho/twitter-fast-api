#python libraries
from uuid import uuid4
from datetime import date
import json

#helpers modules
from helpers.password import generate_password

class UserHandler:
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
        for en, find in enumerate(results):
            if find["user_id"] == str(user_id):
                user_to_delete = results.pop(en)
                return user_to_delete, results
        return False, False


    def delete_register(self, user_id, results):
        for en, find in enumerate(results):
            for search in find.keys():
                if search == str(user_id):
                    register_to_delete = results.pop(en)
                    return register_to_delete, results
        return False, False


    def setup_user(self, results, user_dict):
        user_dict["user_id"] = uuid4()
        
        if not user_dict["birth_date"]:
            user_dict["birth_date"] = date(1999, 1, 1)

        user_dict["password"] = generate_password(user_dict["password"])
        results.append(user_dict)
        return user_dict, results


    def setup_register(self, logic, user_dict):
        new_register = {str(user_dict["user_id"]) : []}
        logic.append(new_register)
        return logic


    def edit_user_into(self, user_id, results, user_dict):
        for find in results:
            if find["user_id"] == str(user_id):
                user_dict = user_dict.dict()
                for keys in find.keys():
                    if keys in user_dict.keys() and user_dict[keys]:
                        find[keys] = user_dict[keys]
                user_dict = find.copy()
                return user_dict
        return None


    def find_user(self, user_id, results):
        for find in results:
            if find["user_id"] == str(user_id):
                return find
        return False