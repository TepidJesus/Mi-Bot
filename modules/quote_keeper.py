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
        with open('quote_bank.json', 'r') as raw_quotes:
            quote_dict = json.load(raw_quotes)
            member_current_quotes = quote_dict[member]
            member_current_quotes.append(quote)
        with open('quote_bank.json', 'w') as raw_quotes:
            json.dump(quote_dict, raw_quotes)

    def retrieve_quotes(self, member):
        with open('quote_bank.json') as raw_quotes:
            quote_dict = json.load(raw_quotes)
            member_quotes = quote_dict[member]
            return member_quotes