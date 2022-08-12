from modules.database_manager import DataManager
from sqlitedict import SqliteDict

class QuoteKeeper:

    CLASS_KEY = "SavedQuotes"

    def __init__(self, guild_members):
        self.quoteKeeperDataManager = DataManager()
        self.refresh_quotes(guild_members)
        self.quoteKeeperDataManager.ensure_category(self.CLASS_KEY, [])
        with SqliteDict('./data/memberData.db') as member_data:
            print(member_data.items())



    def refresh_quotes(self, guild_members): 
        with SqliteDict("./data/memberData.db") as member_data:
            for member in guild_members:
                if member.id not in member_data.keys():
                    self.quoteKeeperDataManager.add_new_member(member)
                    self.quoteKeeperDataManager.update_entry(member, self.CLASS_KEY, [])
                else:
                    continue  

    def add_quote(self, quote, member):
        self.quoteKeeperDataManager.update_entry(member, self.CLASS_KEY, quote, increment=True)
        print(f"[INFO] Quote Added From {member.name}.")

    def retrieve_quotes(self, member):
        with SqliteDict('./data/memberData.db') as member_data:
            print(member_data[member.id])
            return member_data[member.id][self.CLASS_KEY]