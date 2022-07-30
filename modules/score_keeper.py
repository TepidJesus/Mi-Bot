import json
from modules.database_manager import DataManager
from sqlitedict import SqliteDict
from operator import itemgetter

class ScoreKeeper:
    def __init__(self, guild_members):
        self.scoreKeeperDataManager = DataManager()
        self.refresh_scores(guild_members)

    def alter_score(self, member, num):
        self.scoreKeeperDataManager.update_entry(member, "SwearScore", num, True)
        return True

    def refresh_scores(self, guild_members):
        with SqliteDict("./data/memberData.db") as member_data:
            for member in guild_members:
                if member.id not in member_data.keys():
                    self.scoreKeeperDataManager.add_new_member(member)
                    self.scoreKeeperDataManager.update_entry(member, "SwearScore", 0)
                else:
                    continue

    def get_top_three(self): # Top three list or if > 3 members is total num mumbers
        top_three = list()
        members_swear_counts = []
        with SqliteDict("./data/memberData.db") as member_data:
            for member_id in member_data.keys():
                members_swear_counts.append((member_id, member_data[member_id]["SwearScore"]))
        
        members_swear_counts.sort(key=itemgetter(1), reverse=True)

        if len(members_swear_counts) < 3:
            lookup_range = len(members_swear_counts)
        else:
            lookup_range = 3

        for index in range(0, lookup_range):
            top_three.append(members_swear_counts[index])

        return top_three    

    def get_member_score(self, member_name):
        with open('swear_counts.json', 'r') as raw_scores:
            all_scores = json.load(raw_scores)
        try:
            member_score = all_scores[member_name]
        except:
            return None
        return member_score
