import json

class QuoteKeeper:

    def __init__(self):
        try:
            with open('quote_bank.json', 'x'):
                print('[INFO] No Existing Quote Data Found - Generating New Quote File')
        except:
            print('[INFO] Existing Quote Data Detected - A New Quote File Will Not Be Generated')

    def refresh_quotes(self, guild_members):
        with open('quote_bank.json', 'r') as raw_quotes:
            guild_quotes = json.load(raw_quotes)
            for member in guild_members:
                if member.name not in guild_quotes.keys():
                    guild_quotes[str(member.name)] = []
                else:
                    continue
        with open('quote_bank.json', 'w') as raw_quotes:
            json.dump(guild_quotes, raw_quotes)       

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