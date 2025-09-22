
from fake_data import data

class user_data:
    def __init__(self):
        pass
    
    
    def obtain_user_data(self, user_id):
        # Fetch user data from database or any other source
        # For demonstration, we'll use a static example from fake_data.py
        return data
    
    def get_energy_levels(user_id):
                """" Get all energy levels for all user checkins """
                energy_level_arr = []
                for d in data: #fake data only
                        if d['user_id'] == user_id:
                                # print(d)
                                for e in d['entries']:
                                        energy_level_arr.append(e['energy_level'])
                                        print(energy_level_arr)
                                break
                return energy_level_arr
    
    
    