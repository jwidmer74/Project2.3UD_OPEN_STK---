"# Project2.3UD_OPEN_STK---" 
clone or download the contents of https://github.com/jwidmer74/Project2.3UD_OPEN_STK--- into a folder
open your browser and paste https://github.com/jwidmer74/Project2.3UD_OPEN_STK---/archive/master.zip
Extract the Project2.3UD_OPEN_STK----master.zip
#Install oracle virtual box see https://www.virtualbox.org/wiki/Documentation
#Install vagrant and set path varible if needed see link https://www.vagrantup.com/downloads.html
With your google account log on to https://console.developers.google.com/api
Click the help icon on the right, search "Setting up OAuth 2.0" on your Client ID for Web Application.
Set authorized redirect URIs to http://localhost:5000/categoryauth/ 
Set Authorized JavaScript origins to http://localhost:5000 
Download the the contents of https://github.com/jwidmer74/Project2.3UD_OPEN_STK---  into your local machine
Replace the client_secret.json at the root level of with your new .json file downloaded from https://console.developers.google.com/apis/credentials/oauthclient
You downloaded json file will look simular to this naming format client_secret_668549381288-72cm321dq07ogp784qslisimnhq9rsi1.apps.googleusercontent.com.json
Simply rename it to client_secret.json and replace the existing one downloaded from github in path ...\Project2.3UD_OPEN_STK----master\Project2.3UD_OPEN_STK----master\Vagrant\client_secret.json
Open your client_secret.json file and update the value of templates/login.html line 34.
#cd to the directory which contains the .vagrant file
...\Project2.3UD_OPEN_STK----master\Project2.3UD_OPEN_STK----master\vagrant
#Execute the command "vagrant up"
#After some time the VM will be created. It will be several minutes
#After VM creation is complete run the command in the vagrant directory "vagrant ssh"
#You should see "The shared directory is located at /vagrant
#To access your shared files: cd /vagrant"
#If not run the vagrant global-status command to get your id the run the command "vagrant ssh" and your id
#cd /vagrant
Load the data base
Execute the command "python database2.py"
Start the website with the command "python application.py"
Open your browser navigate to http://localhost:5000
The api can be found at http://localhost:5000/category/JSON and http://localhost:5000/category/<int:category_id>/menu/JSON'
Authentication can be found by clicking the Login link at the top right side of the browser page.

