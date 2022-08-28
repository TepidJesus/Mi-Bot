from sqlitedict import SqliteDict
import asyncio

#TODO: Store weekly and monthly, yearly stats using list inside category
#TODO: Add historic data section which will store previous years of data
#TODO: Implement automaticly moving weekly to monthly data and to yearly data
#TODO: Finish get_weelky_stats()
#TODO: Finish get_monthly_stats()
#TODO: Finish get_yearly_stats()
#TODO: Add weekly event that displays weekly stats for a guild (Top Games, most hours played by a member, etc)
#TODO: Add monthly event that displays monthly stats for a guild (Top Games, most hours played by a member, etc)
#TODO: Add yearly event that displays yearly stats for a guild (Top Games, most hours played by a member, etc)

class ActivityMonitor:

    CLASS_KEY = "ActivityHistory"

    def __init__(self, dataManager):
        self.activityMonitorDataManager = dataManager
        self.activityMonitorDataManager.ensure_category(self.CLASS_KEY, {})

    async def full_activity_check(self, bot_instance): # Will be run every 5 minutes, so will assume user has been doing a given activity for that time.
        while True:
            await asyncio.sleep(300)
            with SqliteDict("./data/memberData.db") as member_data:
                for member in bot_instance.get_all_members():
                    if not member.bot:
                        if len(member.activities) != 0:
                            main_activity = member.activities[0] 
                            current_history = self.activityMonitorDataManager.get_data(member, self.CLASS_KEY) # Dictionary
                            if current_history == None:
                                return

                            if main_activity.name not in current_history.keys():
                                dtt = member_data[str(member.id)]
                                dct = dtt[self.CLASS_KEY]
                                dct[main_activity.name] = 5
                                dtt[self.CLASS_KEY] = dct
                                member_data[str(member.id)] = dtt
                            else:
                                dtt = member_data[str(member.id)]
                                dct = dtt[self.CLASS_KEY]
                                dct[main_activity.name] += 5
                                dtt[self.CLASS_KEY] = dct
                                member_data[str(member.id)] = dtt
                

                member_data.commit()
                print("[INFO] Activity Check Complete")
                self.activityMonitorDataManager.dump_database()

    def get_activity_stats(self, member):
            return self.activityMonitorDataManager.get_data(member, self.CLASS_KEY)

    # def get_guild_weekly_stats(self):
