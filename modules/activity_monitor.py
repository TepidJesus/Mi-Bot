import discord


class ActivityMonitor:
    def __init__(self, client):
        try:
            with open('activity_valut.json', 'r'):
                print('[INFO] Existing Activity Data Detected - A New Activity File Will Not Be Generated')
        except:
            with open('activity_valut.json', 'x') as file:
                print('[INFO] No Existing Activity Data Found - Generating New Activity File')
                file.write('{}')

        self.bot = client
        self.activity_cache = {} 

    async def activity_check(self, user):
        current_activities = user.activities
        spotify_activity = current_activities[1]  # For Future Implementation
        main_activity = current_activities[0]

        if user not in self.activity_cache.keys():
            self.activity_cache[user] = [{main_activity: 1}]
        elif main_activity not in self.activity_cache[user][0]:
            self.activity_cache[user][0][main_activity] = 1
        else:
            self.activity_cache[user][0][main_activity] += 1


    



        

        
    