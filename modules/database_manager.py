from sqlitedict import SqliteDict
import discord

class DataManager:
    def __init__(self):
        with SqliteDict('./data/memberData') as member_data:
            print(f'[INFO] Database initialized. Currently holding data of {len(member_data)} members.')

    def add_new_member(self, new_member): # Adds a new member to the database (if they do not already exist.)
        with SqliteDict('./data/memberData') as member_data:
            if new_member in member_data.keys():
                return False
            else:
                if new_member.isinstance(discord.Member):
                    member_data[new_member.id] = {}
                else:
                    member_data[new_member] = {}
            member_data.commit()
            return True

    def update_entry(self, member, key, value, increment=False):
        with SqliteDict('./data/memberData') as member_data:
            if not member.isinstance(discord.Member):
                member_id = member
            else:
                member_id = member.id

            if member_id not in member_data.keys():
                return False
            else:
                if increment:
                    current_val = member_data[member_id][key]
                    member_data[member_id][key] = value + current_val
                    member_data.commit()
                else:
                    member_data[member_id][key] = value
                    member_data.commit()
            return True

    def remove_member(self, member):
        with SqliteDict('./data/memberData') as member_data:
            if member.id not in member_data.keys():
                return False
            else:
                del member_data[member.id]
                member_data.commit()
            return True