class person:

    def __init__(self,name,email,password,gender,dateOfBirth,city,state,country,contact):

        self.name = name
        self.email = email
        self.password = password
        self.gender = gender
        self.dateOfBirth = dateOfBirth
        self.city = city
        self.state = state
        self.country = country
        self.contact = contact
    
    def get_name(self):
        return self.name
    
    def get_email(self):
        return self.email
    
    def get_password(self):
        return self.password
    
    def get_gender(self):
        return self.gender
    
    def get_dateOfBirth(self):
        return self.dateOfBirth
    
    def get_city(self):
        return self.city
    
    def get_state(self):
        return self.state
    
    def get_country(self):
        return self.country
    
    def get_contact(self):
        return self.contact
    
        
    
    def __str__(self):
        return self.name +" "+ self.password +" "+ self.email +" "+ self.gender +" "+ self.dateOfBirth +" "+ self.city +" "+ self.state +" "+ self.country +" "+ self.contact

    
