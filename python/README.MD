Trakr (trakr.tech) visual testing (python) example test script for Heroku apps

This test script is built for Heroku python web apps to quickly perform visual testing between
local development environment (heroku local) and the default heroku remote environment
Much of the concept can be extended to perform visual testing on multiple heroku remote environments

Requirements

1. You should have a Python web app deployed with Heroku. The easiest example will be
https://devcenter.heroku.com/articles/getting-started-with-python

2. You have installed the free Trakr heroku addon
https://elements.heroku.com/addons/trakr
Installing the addon will expose a config var named "TRAKR_API_TOKEN" for your app

3. You can access your app locally via the `heroku local web` command and the app should be
available on http://localhost:5000

4. You have installed Localtunnel (https://localtunnel.github.io/www/)

Preparing the test (One time)

1. Clone the script directory into your app directory so it looks like {app_dir}/trakr/test.py
inside the app_dir is where you will execute your Heroku commands

2. Import the TRAKR_API_TOKEN config var into your local .env file. You can use a command such as
heroku config:get TRAKR_API_TOKEN -s  >> .env

3. You should also import the HEROKU_APP_NAME config var into your local .env file if you have
https://devcenter.heroku.com/articles/dyno-metadata enabled
heroku config:get HEROK_APP_NAME -s  >> .env

If not, you can simply add this entry manually into your local .env file

4. Finally, run the test script and create a corresponding project on Trakr to house all the tests
heroku local:run python trakr/test.py create

If your project is created successfully, it should prompt you to add TRAKR_PROJECT_ID=[project_id] in your .env file

Running the test

Visual testing can be run whenever you have made some local changes and wants to test those changes visually
before pushing it to the Heroku remote environment.

1. Start your web app locally using the command `heroku local web`
IMPORTANT: make sure in your Profile you pass in the flag --reuse-port if you are using gunicorn. This will allow us to perform
port forwarding and expose your local development environment externally.

For example:
web: gunicorn gettingstarted.wsgi --reuse-port

2. Open another terminal and expose your local development environment using
`heroku local:run sh trakr/tunnel.sh`. It is important to run it under `heroku local run`
as it loads in our .env config vars

3. Open another terminal now the local dev environment can be accessed and run the command
`heroku local:run python trakr/test.py test` This will trigger a visual test between the local
development environment and the remote Heroku environment. You should get a URL where you can access
the test results.
