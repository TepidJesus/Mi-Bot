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
                print(f"[INFO] A New Member Has Been Added To The Database (ID: {new_member})")
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
                print[f"[INFO] An Entry In The Database Was Updated (Key: {key} Value: {value} Increment: {increment})"]
                if increment:
                    if isinstance(member_data[member_id][key], list):
                        member_data[member_id][key].append(value)
                    else:
                        current_val = member_data[member_id][key]
                        member_data[member_id][key] = value + current_val
                else:
                    member_data[member_id][key] = value
            member_data.commit(blocking=True)
        return True

    def remove_member(self, member):
        with SqliteDict('./data/memberData.db') as member_data:
            if member.id not in member_data.keys():
                return False
            else:
                del member_data[member.id]
                print(f"[INFO] A Member Has Been Removed From The Database (ID: {member.id})")
                member_data.commit()
            return True

    def ensure_category(self, category, starter_key):
        with SqliteDict('./data/memberData.db', autocommit=True) as member_data:
            for member_id in member_data:
                try:
                    data = member_data[member_id][category]
                except:
                    print(f"[INFO] A New Category Has Been Added To The Database (ID: {member_id} Category: {category})")
                    member_data[member_id][category] = starter_key
            member_data.commit(blocking=True)
        return None

    def get_current_members(self):
        member_ids = []
        with SqliteDict('./data/memberData.db') as member_data:
            for member_id in member_data.iterkeys():
                member_ids.append(member_id)
        return member_ids

    def in_database(self, member_id):
        current_members = self.get_current_members()
        if member_id in current_members:
            return True
        return False