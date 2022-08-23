import discord
from sqlitedict import SqliteDict

class ActivityMonitor:

    CLASS_KEY = "ActivityHistory"

    def __init__(self, guild_members, dataManager):
        self.activityMonitorDataManager = dataManager
        self.refresh_scores(guild_members)
        self.activityMonitorDataManager.ensure_category(self.CLASS_KEY, {})

    def full_activity_check(self, guild_members):
        with SqliteDict("./data/memberData.db") as member_data:


        current_activities = user.activities
        spotify_activity = current_activities[1]  # For Future Implementation
        main_activity = current_activities[0]

    


    



        

        
    