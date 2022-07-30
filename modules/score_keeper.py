import json
from modules.database_manager import DataManager
from sqlitedict import SqliteDict

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
        with open('swear_counts.json', 'r') as raw_json_scores:
            members_swear_counts = json.load(raw_json_scores)
            sorted_counts = dict(sorted(members_swear_counts.items(), key=lambda item: item[1], reverse=True))

        lookup_range = 3
        if len(sorted_counts) < 3:
            lookup_range = len(sorted_counts)

        sorted_values = list(sorted_counts.values()) # Need a more effecient solution
        sorted_keys = list(sorted_counts.keys()) # Need a more effecient solution
        for index in range(0, lookup_range):
            temp_tup = (sorted_keys[index], sorted_values[index])
            top_three.append(temp_tup)

        return top_three    

    def get_member_score(self, member_name):
        with open('swear_counts.json', 'r') as raw_scores:
            all_scores = json.load(raw_scores)
        try:
            member_score = all_scores[member_name]
        except:
            return None
        return member_score
