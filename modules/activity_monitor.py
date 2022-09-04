from sqlitedict import SqliteDict
import asyncio

#TODO: Store weekly and monthly, yearly stats using list inside category LAYOUT. 
# [WEEKLY{activity.name: time, ...}, MONTHLY{activity.name: time, ...}, YEARLY{activity.name: time, ...}]
#TODO: Add historic data section which will store previous years of data
#TODO: Implement automaticly moving weekly to monthly data and to yearly data
#TODO: Finish get_weelky_stats()
#TODO: Finish get_monthly_stats()
#TODO: Finish get_yearly_stats()
#TODO: Add weekly event that displays weekly stats for a guild (Top Games, most hours played by a member, etc)
#TODO: Add monthly event that displays monthly stats for a guild (Top Games, most hours played by a member, etc)
#TODO: Add yearly event that displays yearly stats for a guild (Top Games, most hours played by a member, etc)


class UserActivity:

    def __init__(self, obj):
        self.name = obj.name
        self.play_time = {"week": 5, "month": 0, "year": 0, "total": 0}
        self.id = obj.application_id
        self.picture = obj.large_image_url

    def __eq__(self, other):
        if other.id == self.id:
            return True
        return False

    def __str__(self):
       return (f"Name: {self.name} ({self.id}) Time: {self.play_time}")

    def print_times(self):
        print(f"Week: {self.play_time['week']}")
        print(f"Month: {self.play_time['month']}")
        print(f"Year: {self.play_time['year']}")
        print(f"Total: {self.play_time['total']}")

    def get_weekly_time(self):
        return self.play_time["week"]

class ActivityMonitor:

    CLASS_KEY = "ActivityHistory"

    def __init__(self, dataManager):
        self.activityMonitorDataManager = dataManager
        self.activityMonitorDataManager.ensure_category(self.CLASS_KEY, []) # Stores Activity objects

    async def full_activity_check(self, bot_instance): # Will be run every 5 minutes, so will assume user has been doing a given activity for that time.
        while True:
            await asyncio.sleep(15)
            with SqliteDict("./data/memberData.db") as member_data:
                for member in bot_instance.get_all_members():
                    if not member.bot:
                        if len(member.activities) != 0:
                            main_activity = member.activities[0] 
                            current_history = self.activityMonitorDataManager.get_data(member, self.CLASS_KEY) # Returns list
                            if not any(curr.id == main_activity.application_id for curr in current_history): # If the activity is not in the list
                                dtt = member_data[str(member.id)]
                                dct = dtt[self.CLASS_KEY]
                                dct.append(UserActivity(main_activity))
                                dtt[self.CLASS_KEY] = dct
                                member_data[str(member.id)] = dtt
                            else:
                                dtt = member_data[str(member.id)]
                                dct = dtt[self.CLASS_KEY]
                                obj = next((act for act in dct if act.id == main_activity.application_id), None)
                                obj.play_time["week"] += 5
                                dtt[self.CLASS_KEY] = dct
                                member_data[str(member.id)] = dtt
                

                member_data.commit()
                print("[INFO] Activity Check Complete")
                self.activityMonitorDataManager.dump_database()

    def get_weekly_activity_stats(self, member):
            return self.activityMonitorDataManager.get_data(member, self.CLASS_KEY)[0]

    def get_guild_weekly_stats(self):
        """ Returns the following as a tuple:
            - Total Hours of games played by the guild so far this week (int).
            - Most played game by the guild this week and hours of it (String, Int, game pic)
            - Member who played the most hours during the week and their most played game (Member, int, game)
        """
        total_guild_hours = 0
        most_played_game = None
        played_games = []
        top_member = None
        with SqliteDict("./data/memberData.db") as member_data:

            for member in self.activityMonitorDataManager.get_current_guild().members:
                member_played_games = []
                member_time = 0
                if not member.bot:
                    dtt = member_data[str(member.id)]
                    lst = dtt[self.CLASS_KEY][0]
                    for game in lst:
                        if game not in played_games:
                            member_played_games.append(game)
                            member_time += game.get_weekly_time()
                    
                        
