from sqlitedict import SqliteDict
import asyncio

from bot import bot_disconnect

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


class Activity:
    def __init__(self, obj):
        self.name = obj.name
        self.play_time = {"week": 0, "month": 0, "year": 0, "Total": 0}
        self.id = obj.id
        self.picture = obj.large_image.url

class ActivityMonitor:

    CLASS_KEY = "ActivityHistory"

    def __init__(self, dataManager):
        self.activityMonitorDataManager = dataManager
        self.activityMonitorDataManager.ensure_category(self.CLASS_KEY, [{}, {}, {}]) #[WEEKLY, MONTHLY, YEARLY]

    async def full_activity_check(self, bot_instance): # Will be run every 5 minutes, so will assume user has been doing a given activity for that time.
        while True:
            await asyncio.sleep(30)
            with SqliteDict("./data/memberData.db") as member_data:
                for member in bot_instance.get_all_members():
                    if not member.bot:
                        if len(member.activities) != 0:
                            main_activity = member.activities[0] 
                            current_history = self.activityMonitorDataManager.get_data(member, self.CLASS_KEY)
                            if main_activity.id not in current_history[0].keys():
                                dtt = member_data[str(member.id)]
                                dct = dtt[self.CLASS_KEY][0]
                                dct[main_activity.name] = 5
                                dtt[self.CLASS_KEY][0] = dct
                                member_data[str(member.id)] = dtt
                            else:
                                dtt = member_data[str(member.id)]
                                dct = dtt[self.CLASS_KEY][0]
                                dct[main_activity.name] += 5
                                dtt[self.CLASS_KEY][0] = dct
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
        played_games = {}
        with SqliteDict("./data/memberData.db") as member_data:

            for member in self.activityMonitorDataManager.get_current_guild().members:
                if not member.bot:
                    dtt = member_data[str(member.id)]
                    dct = dtt[self.CLASS_KEY][0]
                    for game in dct.keys():
                        if game not in played_games.keys():
                            played_games[game] = dct[game]
                        else:
                            played_games[game] += dct[game]
