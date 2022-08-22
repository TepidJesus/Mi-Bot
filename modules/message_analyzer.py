class Message_processor():

    def __init__(self):
        with open('./data/word-blacklist.txt', 'r') as raw_blacklist:
            self.word_blacklist_raw = raw_blacklist.read().split(',')
        self.word_blacklist = list()
        for word in self.word_blacklist_raw:
            word = word.strip(' ')
            self.word_blacklist.append(word)       
        print('[INFO] Word Blacklist Loaded')
        
        self.message_log = dict()
        print('[INFO] Message Log Initialised')

    def listify_message(self, message_raw):
        self.message_list = list()
        self.message_list = message_raw.content.split(' ')
        for i in range(len(self.message_list)):
            if self.message_list[i].isalpha():
                self.message_list[i] = self.message_list[i].lower()
            elif self.message_list[i].isalnum() != True:
                self.message_list[i] = self.message_list[i].strip('!')
                self.message_list[i] = self.message_list[i].strip('.')
                self.message_list[i] = self.message_list[i].strip(',')
                self.message_list[i] = self.message_list[i].strip('-')
                self.message_list[i] = self.message_list[i].strip('?')
                self.message_list[i] = self.message_list[i].lower()
            else:
                continue
        return self.message_list
        
    def swear_check(self, list_message):
        num_swear_words = 0
        for word in list_message:
            if word in self.word_blacklist:
                num_swear_words += 1
            else:
                continue
        
        return num_swear_words 

    def spam_check(self, raw_message):
        if raw_message.author.id in self.message_log:
            self.message_log[raw_message.author.id] += 1
        else:
            self.message_log[raw_message.author.id] = 1
