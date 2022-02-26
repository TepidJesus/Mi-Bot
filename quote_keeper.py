import json

class QuoteKeeper:

    def __init__(self):
        try:
            with open('quote_bank.json', 'x'):
                print('[INFO] No Existing Quote Data Found - Generating New Quote File')
        except:
            print('[INFO] Existing Quote Data Detected - A New Quote File Will Not Be Generated')

    def add_quote(self, quote, member):
        with open('quote_bank.json', 'r') as raw_quotes:
            quote_dict = json.load(raw_quotes)
            member_current_quotes = quote_dict[member]
            member_current_quotes.append(quote)
        with open('quote_bank.json', 'w') as raw_quotes:
            json.dump(quote_dict, raw_quotes)