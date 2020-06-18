from Person import person

class user(person):
    noOfUsers = 0
    def __init__(self,name,email,password,gender,dateOfBirth,city,state,country,contact):
        person.__init__(self,name,email,password,gender,dateOfBirth,city,state,country,contact)
        self.active = True
        user.noOfUsers += 1
    

    def get_active(self):
        return self.active
    
    def set_active_online(self):
        self.active = True
    
    def set_active_offline(self):
        self.active = False
        

