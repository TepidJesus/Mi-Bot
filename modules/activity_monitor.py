from sqlitedict import SqliteDict
import asyncio
import copy as cp
import datetime

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
        self.picture = obj.small_image_url if obj.small_image_url != None else obj.large_image_url

    def __eq__(self, other):
        if other.id == self.id:
            return True
        return False

    def __str__(self):
       return (f"Name: {self.name} ({self.id}) Time: {self.play_time} Picture: {self.picture}")

    def print_times(self):
        print(f"Week: {self.play_time['week']}")
        print(f"Month: {self.play_time['month']}")
        print(f"Year: {self.play_time['year']}")
        print(f"Total: {self.play_time['total']}")

    def get_weekly_time(self):
        return self.play_time["week"]

    def get_monthly_time(self):
        return self.play_time["month"]

    def get_monthly_time(self):
        return self.play_time["year"]

class ActivityMonitor:

    CLASS_KEY = "ActivityHistory"

    def __init__(self, dataManager, bot_instance):
        self.activityMonitorDataManager = dataManager
        self.activityMonitorDataManager.ensure_category(self.CLASS_KEY, []) # Stores Activity objects
        self.bot_instance = bot_instance
        self.last_date = datetime.date.today()

    async def full_activity_check(self): # Will be run every 5 minutes, so will assume user has been doing a given activity for that time.
        while True:
            await asyncio.sleep(15)
            with SqliteDict("./data/memberData.db") as member_data:
                for member in self.bot_instance.get_all_members():
                    if not member.bot:
                        if len(member.activities) != 0:
                            main_activity = member.activities[0] 
                            print(main_activity)
                            current_history = self.activityMonitorDataManager.get_data(member, self.CLASS_KEY) # Returns list
                            print(current_history)
                            if not any(curr.id == main_activity.application_id for curr in current_history): # If the activity is not in the list
                                print('Failed Comparison')
                                dtt = member_data[str(member.id)]
                                dct = dtt[self.CLASS_KEY]
                                dct.append(UserActivity(main_activity))
                                dtt[self.CLASS_KEY] = dct
                                member_data[str(member.id)] = dtt
                            else:
                                print('Passed Comparison')
                                dtt = member_data[str(member.id)]
                                dct = dtt[self.CLASS_KEY]
                                obj = next((act for act in dct if act.id == main_activity.application_id), None)
                                obj.play_time["week"] += 500
                                dtt[self.CLASS_KEY] = dct
                                member_data[str(member.id)] = dtt
                

                member_data.commit()
                print("[INFO] Activity Check Complete")
                self.activityMonitorDataManager.dump_database()

    def move_weekly_to_monthly(self):
        for member in self.bot_instance.get_all_members():
            for activity in self.activityMonitorDataManager.get_data(member, self.CLASS_KEY):
                curr_weekly = activity.play_time["week"]
                self.activity.play_time["month"] += curr_weekly
                self.activity.play_time["week"] = 0
        return

    def move_monthly_to_yearly(self, activity):
        for member in self.bot_instance.get_all_members():
            for activity in self.activityMonitorDataManager.get_data(member, self.CLASS_KEY):
                curr_monthly = activity.play_time["month"]
                self.activity.play_time["year"] += curr_monthly
                self.activity.play_time["month"] = 0
        return

    def move_yearly_to_total(self, activity):
        for member in self.bot_instance.get_all_members():
            for activity in self.activityMonitorDataManager.get_data(member, self.CLASS_KEY):
                curr_yearly = activity.play_time["year"]
                self.activity.play_time["total"] += curr_yearly
                self.activity.play_time["year"] = 0
        return

    def get_guild_stats(self, period):
        """ Returns the following as a tuple:
            - Total Hours of games played by the guild so far this week (int).
            - Most played game by the guild this week and hours of it (game)
            - Member who played the most hours during the week and their most played game (Member, time, game)
        """
        if period != "weekly" and period != "monthly" and period != "yearly":
            return None

        total_guild_hours = 0
        played_games = []
        top_member = None

        with SqliteDict("./data/memberData.db") as member_data:

            for member in self.bot_instance.get_all_members():
                member_played_games = []
                member_time = 0
                dtt = member_data[str(member.id)]
                if not member.bot and not len(dtt[self.CLASS_KEY]) == 0:
                    lst = dtt[self.CLASS_KEY]
                    for game in lst:
                        member_played_games.append(cp.copy(game))

                        if period == "monthly":
                            member_time += game.get_monthly_time()
                            total_guild_hours += game.get_monthly_time()
                        elif period == "yearly":
                            member_time += game.get_yearly_time()
                            total_guild_hours += game.get_yearly_time()
                        else:
                            total_guild_hours += game.get_weekly_time()
                            member_time += game.get_weekly_time()
                    
                    total_guild_hours += member_time

                    if (top_member == None or member_time > top_member[1]) and len(member_played_games) != 0:
                        if period == "monthly":
                            top_member = (member, member_time, max(member_played_games, key=lambda x: x.get_monthly_time()))
                        elif period == "yearly":
                            top_member = (member, member_time, max(member_played_games, key=lambda x: x.get_yearly_time()))
                        else:
                            top_member = (member, member_time, max(member_played_games, key=lambda x: x.get_weekly_time()))
                    
                    for game in member_played_games:
                        if game not in played_games:
                            played_games.append(game)
                        else:
                            obj = next((act for act in played_games if act.id == game.id), None)
                            if period == "monthly":
                                obj.play_time["month"] += game.get_monthly_time()
                            elif period == "yearly":
                                obj.play_time["year"] += game.get_yearly_time()
                            else:
                                obj.play_time["week"] += game.get_weekly_time()

        if len(played_games) != 0:
            if period == "monthly":
                most_played_game = max(played_games, key=lambda x: x.get_monthly_time())
            elif period == "yearly":
                most_played_game = max(played_games, key=lambda x: x.get_yearly_time())
            else:
                most_played_game = max(played_games, key=lambda x: x.get_weekly_time())
        else:
            most_played_game = None

        print(total_guild_hours, most_played_game, top_member)

        return (total_guild_hours, most_played_game, top_member)
                        
