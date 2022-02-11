import json

class ScoreKeeper:
    def __init__(self) -> None:
        try:
            with open('swear_counts.json', 'x'):
                print('[INFO] No Existing JSON Data Found\n[INFO]Generating New File')
        except:
            print('[INFO] Existing JSON Data Detected\n[INFO] A New File Will Not Be Generated')


    def alter_score(self, member_name, num):
        with open('swear_counts.json', 'r') as self.raw_json_scores:
            self.members_swear_count = json.load(self.raw_json_scores)
            self.current_points = self.members_swear_count[member_name]
            self.new_points = self.current_points + num
            self.members_swear_count[member_name] = self.new_points
        with open('swear_counts.json', 'w') as file:
            json.dump(self.members_swear_count, file)

    def refresh_scores(self, guild_members):
        with open('swear_counts.json', 'r') as raw_json_scores:
            self.member_swear_counts = json.load(raw_json_scores)
            for member in guild_members:
                if member.name not in self.member_swear_counts.keys():
                    self.member_swear_counts[member.name] = 0
                else:
                    continue 
        with open('swear_counts.json', 'w') as file:
            json.dump(self.member_swear_counts, file)     