
BAD_WORDS = 'fuck'

class Message_processor():

    def listify_message(self, message_raw):
        print(f'[MESSAGE]: {message_raw.author} Says \"{message_raw.content}\"')
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
            if word in BAD_WORDS:
                num_swear_words += 1
            else:
                continue
        
        return num_swear_words 
