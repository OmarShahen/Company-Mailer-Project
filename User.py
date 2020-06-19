from Person import person

class user(person):
    noOfUsers = 0
    def __init__(self,name,email,password,gender,dateOfBirth,city,country,contact):
        person.__init__(self,name,email,password,gender,dateOfBirth,city,country,contact)
        self.active = True
        user.noOfUsers += 1
        self.appPassword = None
    
    
    
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
        

