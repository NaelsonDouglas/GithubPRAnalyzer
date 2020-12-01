import requests
import json
class Api:
        def get(self,url, parameters=None) -> dict:
                header = {'Authorization': 'token f55851722c20f63ebd5dff35875fbaa94f7a3f3a'}
                result = requests.get(url,params=parameters, headers=header)
                result = result.json()
                return result

        def  list_pullreqs(self,owner,repo,state='closed'):
                params = {'state':state}
                url = 'https://api.github.com/repos/{}/{}/pulls'.format(owner,repo)
                result = self.get(url,params)
                filtered_results = []
                for res in result:
                        cell = {}
                        cell['issue'] = res['number']
                        cell['merged_at'] = res['merged_at']
                        cell['author_association'] = res['author_association']
                        cell['body'] = res['body']
                        cell['validated'] = False
                        filtered_results.append(cell)
                return filtered_results

        def get_pullreq(self, owner,repo, pullreq_id):
                url = 'https://api.github.com/repos/{}/{}/pulls/{}'.format(owner,repo,str(pullreq_id))
                return self.get(url)

        def  get_pullreq_commits_shas(self, owner,repo, pullreq_id):
                all_pr = self.get_pullreq(owner,repo,pullreq_id)
                url = 'https://api.github.com/repos/{}/{}/pulls/{}/commits'.format(owner,repo,str(pullreq_id))
                result = self.get(url)
                only_shas_result = []
                for commit in result:
                        only_shas_result.append(commit['sha'])
                output = {}
                #output['body'] = all_pr['body']
                output['base_commit'] = all_pr['base']['sha']
                output['first_commit'] = only_shas_result[0]
                output['last_commit'] = only_shas_result[len(only_shas_result)-1]
                #output['shas'] = only_shas_result
                return output

        def  get_comments(self,owner,repo,issue):
                url = 'https://api.github.com/repos/{}/{}/issues/{}/comments'.format(owner,repo,str(issue))
                result = self.get(url)
                filtered_result = []
                for c in result:
                        cell = {}
                        cell['body'] = c['body']
                        cell['created_at'] = c['created_at']
                        cell['author_association'] = c['author_association']
                        filtered_result.append(cell)
                return filtered_result

        def  get_pullreq_changed_files(self, owner,repo, pullreq_id,extension=None):
                url = 'https://api.github.com/repos/{}/{}/pulls/{}/files'.format(owner,repo,str(pullreq_id))
                result = self.get(url)
                filtered_result = []
                commits_shas = self.get_pullreq_commits_shas(owner,repo,pullreq_id)
                for i in range(0, len(result)):
                        result_cell = result[i]
                        filename = str(result_cell['filename'])
                        if extension == None or filename.endswith('.'+extension):
                                try:
                                        result_cell.pop('patch')
                                except:
                                        pass
                                result_cell.pop('contents_url')
                                result_cell.pop('additions')
                                result_cell.pop('deletions')
                                result_cell.pop('changes')
                                result_cell.pop('blob_url')
                                if result_cell['status'] == 'modified':
                                        base_state_url = 'https://github.com/{}/{}/raw/{}/{}'.format(owner,repo,commits_shas['base_commit'],result_cell['filename'])
                                        #result_cell['base_state'] = requests.get(base_state_url).text
                                        result_cell['base_state'] = base_state_url
                                elif result_cell['status'] == 'created':
                                        result_cell['base_state'] = ''

                                pullreq_state_url = 'https://github.com/{}/{}/raw/{}/{}'.format(owner,repo,commits_shas['last_commit'],result_cell['filename'])
                                #result_cell['pullreq_state'] = requests.get(pullreq_state_url).text
                                result_cell['pullreq_state'] = pullreq_state_url
                                filtered_result.append(result_cell)
                return filtered_result

        def analyze(self, owner,repo, pullreq_issue_id,extension=None):
                changed_files = self.get_pullreq_changed_files(owner,repo, pullreq_issue_id,extension)
                if (len(changed_files) > 0):
                        comments = self.get_comments(owner,repo,pullreq_issue_id)
                        result = {}
                        result['changed_files'] = changed_files
                        result['comments'] = comments
                        result['issue'] = pullreq_issue_id
                        return result
                return None