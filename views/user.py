from uuid import UUID, uuid4
from datetime import date
import json

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