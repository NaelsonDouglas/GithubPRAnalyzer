from api import Api
from mongo_connector import MongoConnector
import json

api = Api()
db = MongoConnector()

repositories = [{'owner':'pytorch', 'name':'pytorch'},{'owner':'tensorflow', 'name':'tensorflow'},{'owner':'scrapy', 'name':'scrapy'},{'owner':'scikit-learn', 'name':'scikit-learn'},
                {'owner':'ranger', 'name':'ranger'},{'owner':'django', 'name':'django'},{'owner':'ranger', 'name':'ranger'}]

for repo in repositories:
        pull_requests = api.list_pullreqs(repo['owner'],repo['name'])
        for pr in pull_requests:
                repo_owner = repo['owner']
                repo_name = repo['name']
                full_repo = repo_owner+'/'+repo_name
                if not db.exists(full_repo,pr['issue']):
                        a = api.analyze(repo_owner,repo_name,pr['issue'],'py')
                        if (a != None):
                                a['body'] = pr['body']
                                a['merged_at'] = pr['merged_at']
                                a['author_association'] = pr['author_association']
                                db.insert_one(full_repo,a)