import json

class ScoreKeeper:
    def __init__(self) -> None:
        try:
            with open('swear_counts.json', 'r'):
                print('[INFO] Existing Count Data Detected - A New Quote File Will Not Be Generated')
        except:
            with open('swear_counts.json', 'x') as file:
                print('[INFO] No Existing Count Data Found - Generating New Count File')
                file.write('{}')


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

    def get_top_three(self): # Top three list or if > 3 members is total num mumbers
        top_three = list()
        with open('swear_counts.json', 'r') as raw_json_scores:
            members_swear_counts = json.load(raw_json_scores)
            sorted_counts = dict(sorted(members_swear_counts.items(), key=lambda item: item[1], reverse=True))

        lookup_range = int()
        if len(sorted_counts) < 3:
            lookup_range = len(sorted_counts)
        else:
            lookup_range = 3

        sorted_values = list(sorted_counts.values()) # Need a more effecient solution
        sorted_keys = list(sorted_counts.keys()) # Need a more effecient solution
        for index in range(0, lookup_range):
            temp_tup = (sorted_keys[index], sorted_values[index])
            top_three.append(temp_tup)

        return top_three    

    def get_member_score(self, member_name):
        with open('swear_counts.json', 'r') as raw_scores:
            all_scores = json.load(raw_scores)
        try:
            member_score = all_scores[member_name]
        except:
            return None
        return member_score
