import json
from modules.database_manager import DataManager
from sqlitedict import SqliteDict
class QuoteKeeper:

    def __init__(self, guild_members):
        self.quoteKeeperDataManager = DataManager()
        self.refresh_quotes(guild_members)


    def refresh_quotes(self, guild_members): 
        with SqliteDict("./data/memberData.db") as member_data:
            for member in guild_members:
                if member.id not in member_data.keys():
                    self.scoreKeeperDataManager.add_new_member(member)
                    self.scoreKeeperDataManager.update_entry(member, "SavedQuotes", [])
                else:
                    continue  

    def add_quote(self, quote, member):
        self.quoteKeeperDataManager.update_entry(member, "SavedQuotes", quote, increment=True)
        print(f"[INFO] Quote Added From {member.name}.")

    def retrieve_quotes(self, member):
        with open('quote_bank.json') as raw_quotes:
            quote_dict = json.load(raw_quotes)
            member_quotes = quote_dict[member]
            return member_quotes