import json
from modules.database_manager import DataManager
from sqlitedict import SqliteDict
from operator import itemgetter

class ScoreKeeper:

    CLASS_KEY = "SwearScore"

    def __init__(self, guild_members, dataManager):
        self.scoreKeeperDataManager = dataManager
        self.refresh_scores(guild_members)
        self.scoreKeeperDataManager.ensure_category(self.CLASS_KEY, 0)

    def alter_score(self, member, num):
        self.scoreKeeperDataManager.update_entry(member, self.CLASS_KEY, num, True)
        return True

    def refresh_scores(self, guild_members):
        with SqliteDict("./data/memberData.db") as member_data:
            for member in guild_members:
                if not self.scoreKeeperDataManager.in_database(member.id):
                    self.scoreKeeperDataManager.add_new_member(member)
                    self.scoreKeeperDataManager.update_entry(member, self.CLASS_KEY, 0)
                else:
                    continue

    def get_top_three(self): # Top three list or if < 3 members is total num mumbers
        top_three = list()
        members_swear_counts = []
        with SqliteDict("./data/memberData.db") as member_data:
            for member_id in member_data.keys():
                members_swear_counts.append((member_id, member_data[member_id][self.CLASS_KEY]))
        
        members_swear_counts.sort(key=itemgetter(1), reverse=True)

        if len(members_swear_counts) < 3:
            lookup_range = len(members_swear_counts)
        else:
            lookup_range = 3

        for index in range(0, lookup_range):
            top_three.append(members_swear_counts[index])

        return top_three    

    def get_member_score(self, member):
        with SqliteDict("./data/memberData.db") as member_data:
            member_score = member_data[member.id][self.CLASS_KEY]
        return member_score

    def initialize_new_member(self, member):
        self.scoreKeeperDataManager.add_new_member(member)
        self.scoreKeeperDataManager.ensure_category_single(self.CLASS_KEY, 0, member)

