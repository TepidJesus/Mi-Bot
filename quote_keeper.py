import json

class QuoteKeeper:

    def __init__(self):
        try:
            with open('quote_bank.json', 'x'):
                print('[INFO] No Existing JSON Data Found\n[INFO]Generating New File')
        except:
            print('[INFO] Existing JSON Data Detected\n[INFO] A New File Will Not Be Generated')

    def add_quote(self):
        with open('quote_bank.json', 'r') as raw_quotes:
            quote_dict = json.load(raw_quotes)