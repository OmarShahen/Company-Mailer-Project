from Person import person

class user(person):
    noOfUsers = 0
    def __init__(self,name,email,password,gender,dateOfBirth,city,country,contact):
        person.__init__(self,name,email,password,gender,dateOfBirth,city,country,contact)
        self.active = True
        user.noOfUsers += 1
        self.appPassword = None
        self.inbox_mails = []
        self.sent_mails = []
        self.trash_mails = []

        

    
    def set_appPassword(self,appPassword):
        self.appPassword = appPassword  
    def get_appPassword(self):
        return self.appPassword



    def get_active(self):
        return self.active
        
    def get_active_str(self):
        if self.active == True:
            return "online"
        else:
            return "offline"

    def set_active_online(self):
        self.active = True
    
    def set_active_offline(self):
        self.active = False
    
    def add_sent_mail(self, mail):
        self.sent_mails.append(mail)
    
    def get_all_sent_mails(self):
        return self.sent_mails
    
    def add_inbox(self, mail):
        self.inbox_mails.append(mail)
    def get_all_inbox(self):
        return self.inbox_mails
    def add_trash(self, mail):
        self.trash_mails.append(mail)
    def get_all_trash(self):
        return self.trash_mails


    
    
        

