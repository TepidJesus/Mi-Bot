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
        using_spotify = False
        main_activity = current_activities[0]
    
        if len(current_activities) == 2:
            main_activity = current_activities[0] 
            using_spotify = True
    



        

        
    