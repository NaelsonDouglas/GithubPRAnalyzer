from pymongo import MongoClient
class MongoConnector:
    def __init__(self):
        self.client = MongoClient('localhost', 27017)
        self.db = self.client['Github']
        try:
            self.db.create_collection('PullRequests')
        except:
            pass
        self.matches = self.db['PullRequests'].create_index(('issue'), unique = True)

    def insert_one(self, collection,data):
        x=self.db[collection].find_one({'issue':data['issue']})
        if x == None:
            self.db[collection].insert_one(data)

    def exists(self,repository,issue):
        document = None
        try:
            document = self.db[repository].find_one({'issue':data['issue']})
            if document != None:
                return true
        except:
            return False