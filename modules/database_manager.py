from sqlitedict import SqliteDict
import discord
class DataManager:
    def __init__(self):
        with SqliteDict('./data/memberData') as member_data:
            print(f'[INFO] Database initialized. Currently holding data of {len(member_data)} members.')

    def add_new_member(self, new_member):
        with SqliteDict('./data/memberData') as member_data:
            if new_member in member_data.keys():
                return False
            else:
                if new_member.isinstance(discord.Member):
                    member_data[new_member.id] = {}
                else:
                    member_data[new_member] = {}
            return True