import discord


class ActivityMonitor:
    def __init__(self, client):
        self.activity_cache = {}
        for member in 

    async def activity_check(self, user):
        current_activities = user.activities
        using_spotify = False
        main_activity = current_activities[0]
    
        if len(current_activities) == 2:
            main_activity = current_activities[0]
            using_spotify = True

        
    