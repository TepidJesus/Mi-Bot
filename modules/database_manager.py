from sqlitedict import SqliteDict
import discord

#TODO: Add uniformity to member.id. All inputs should accept the raw member object then get id.

class DataManager:
    def __init__(self):
        with SqliteDict('./data/memberData.db') as member_data:
            print(f'[INFO] Database initialized. Currently holding data of {len(member_data)} members.')

    def add_new_member(self, new_member): # Adds a new member to the database (if they do not already exist.)
        with SqliteDict('./data/memberData.db') as member_data:
            if isinstance(new_member, discord.Member):
                new_member = new_member.id
            if new_member in member_data.keys():
                return False
            else:
                member_data[new_member] = {}
            member_data.commit()
            return True

    def update_entry(self, member, key, value, increment=False):
        with SqliteDict('./data/memberData.db') as member_data:
            if not isinstance(member, discord.Member):
                member_id = member
            else:
                member_id = member.id    

            if member_id not in member_data.keys():
                return False
            else:
                if increment:
                    if isinstance(member_data[member_id][key], list):
                        member_data[member_id][key].append(value)
                    else:
                        current_val = member_data[member_id][key]
                        member_data[member_id][key] = value + current_val
                else:
                    member_data[member_id][key] = value
            member_data.commit()
            return True

    def remove_member(self, member):
        with SqliteDict('./data/memberData.db') as member_data:
            if member.id not in member_data.keys():
                return False
            else:
                del member_data[member.id]
                member_data.commit()
            return True
