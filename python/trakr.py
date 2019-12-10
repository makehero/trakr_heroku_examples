import json, os, requests

'''
A simple testing class that leverages the Trakr API to perform a visual test
between the local dev environment vs the Heroku development (deployed) environment
'''
class trakr():
    def __init__(self):
        self.app_name = os.environ.get('HEROKU_APP_NAME')
        self.trakr_api_token = os.environ.get('TRAKR_API_TOKEN')
        self.trakr_project_id = os.environ.get('TRAKR_PROJECT_ID')
        self.local_port = '5000'
        self.initialized = False
        self.can_test = False

        if self.app_name is None:
            print('You need to set the HEROKU_APP_NAME config var in your .env file')

        if self.trakr_api_token is None:
            print('You need to set the TRAKR_API_TOKEN config var in your .env file. For example, if you have successfullly installed the Trakr addon, run `heroku config:get TRAKR_API_TOKEN -s  >> .env`')

        if self.app_name is not None and self.trakr_api_token is not None:
            self.initialized = True

        if self.initialized and self.trakr_project_id is not None:
            self.can_test = True
            self.tunnel_url = f'http://trakr-project-{self.trakr_project_id}.localtunnel.me'

        if self.initialized:
            self.dev_url = f'https://{self.app_name}.herokuapp.com'
            self.trakr_api = 'https://app.trakr.tech/api/v1'

    ##
    # Create a corresponding project on Trakr
    #
    def createProject(self):
        if self.initialized and self.can_test == False:
            endpoint = f'{self.trakr_api}/project'
            data = {
                'production': {
                    'url': self.dev_url,
                },
                'title': self.app_name,
                'scan_url': 1,
                'uris': [
                    '/',
                ],
            }
            headers = {'x-api-key': self.trakr_api_token}
            response = requests.post(endpoint, headers=headers, data=json.dumps(data))
            if response.status_code == 200:
                response_body = response.json()
                if response_body['status'] == 'success':
                    print(f"Project is successfully created on Trakr, please add TRAKR_PROJECT_ID={response_body['result']['id']} in your .env file")
                else:
                    print(response_body)
            else:
                print(f'We had encountered issues while trying to create a project with status code {response.status_code}')
        else:
            print('You have already created the project in Trakr as indicated in the config var TRAKR_PROJECT_ID')

    ##
    # Running a test between the local environment against the development
    # environment
    #
    def runTest(self):
        if self.initialized and self.can_test:
            endpoint = f'{self.trakr_api}/project/{self.trakr_project_id}/compare_build'
            data = {
                'environment': 'production',
                'build_url': self.tunnel_url,
            }
            headers = {'x-api-key': self.trakr_api_token}
            response = requests.post(endpoint, headers=headers, data=json.dumps(data))
            if response.status_code == 200:
                response_body = response.json()
                if response_body['status'] == 'success':
                    print(f"Your test have been triggered. You can see the result at {response_body['result']['url']}")
                else:
                    print(response_body)
        else:
            print('You need to run `heroku local:run python ./trakr.py create` first to link a project on Trakr.')
