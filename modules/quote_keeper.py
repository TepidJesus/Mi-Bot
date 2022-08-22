from modules.database_manager import DataManager
from sqlitedict import SqliteDict

class QuoteKeeper:

    CLASS_KEY = "SavedQuotes"

    def __init__(self, guild_members, dataManager):
        self.quoteKeeperDataManager = dataManager
        self.refresh_quotes(guild_members)
        self.quoteKeeperDataManager.ensure_category(self.CLASS_KEY, [])

    def refresh_quotes(self, guild_members): 
        with SqliteDict("./data/memberData.db") as member_data:
            for member in guild_members:
                if not self.quoteKeeperDataManager.in_database(member.id):
                    self.quoteKeeperDataManager.add_new_member(member)
                    self.quoteKeeperDataManager.update_entry(member, self.CLASS_KEY, [])
                else:
                    continue

    def add_quote(self, quote, member):
        success = self.quoteKeeperDataManager.update_entry(member, self.CLASS_KEY, quote, increment=True)
        if success:
            print(f"[INFO] Quote Added From {member.name}.")
        else:
            print(f"[ERROR] Failed Whilst Adding Quote For {member.name}")

    def retrieve_quotes(self, member):
        with SqliteDict('./data/memberData.db') as member_data:
            print(member_data[member.id])
            print(member_data.keys())
            return member_data[member.id][self.CLASS_KEY]

    def initialize_new_member(self, member):
        self.quoteKeeperDataManager.add_new_member(member)
        self.quoteKeeperDataManager.ensure_category_single(self.CLASS_KEY, [], member)
        print(f"[INFO] A New Member, {member.name}, Has Been Added To The Quote Database")