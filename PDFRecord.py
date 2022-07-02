import json

class JsonData(object):
    def __init__(self, j):
         self.__dict__ = json.loads(j)

         
class PDFRecord:
    condition = 'New'
    def __init__(self, date, particular, details, withdrawal, deposit, balance):
        self.date = date
        self.particular = particular
        self.details = details
        self.withdrawal = withdrawal
        self.deposit = deposit
        self.balance = balance
    
    

    def __repr__(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=False, indent=4)


#Mercedes = Car('Mercedes', 'S Class', 'Red')

#print (Mercedes.color)