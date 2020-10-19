# project2-m1-as3243
A chat application where chatbot responds to certain commands and users can talk to each other.
To use this repository, you must follow these steps:

1) Clone this repository by using git clone https://github.com/NJIT-CS490/project2-m1-as3243
2) Install flask using ([sudo] pip[3] install flask)
3) Install requests using the same process as above ([sudo] pip[3] install requests)
4) Run nvm install 7 to Upgrade Node version to 7
5) Run npm install to Install initial npm dependencies from package.json
6) Run touch .gitignore; echo "node_modules/" >> .gitignore; $ echo "static/script.js" >> .gitignore $ echo "package-lock.json" >> .gitignore to add files to your .gitignore
7) Run npm install --save-dev webpack from the folder that contains package.json! You will get an error if you are in a different folder to Install Webpack
This line starts up Webpack, which looks inside webpack.config.js, loads configuration options, and starts transpiling your JS code into static/script.js. You may be asked to also install webpack-cli. Type yes.
8) Run sudo yum install postgresql postgresql-server postgresql-devel postgresql-contrib postgresql-docs to Install PostGreSQL and Enter yes to all prompts.
9) Run sudo service postgresql initdb to Initialize PSQL database
10) Run sudo service postgresql start to  Start PSQL
11) Run sudo -u postgres createuser --superuser $USER to Make a new superuser
If you get an error saying "could not change directory", It worked.
12) Same as above, run sudo -u postgres createdb $USER to make a new database
13) Make sure your user shows up by running psql, \du, \l 
14) Make new use by running create user {some_username_here} superuser password {some_unique_new_password_here};
15) Type \q to quit
16) Run sudo yum update to get psql to work with Python
17) Run pip install psycopg2-binary
18) Run pip install Flask-SQLAlchemy==2.1
19) Create a new file in the directory project2-m1-as3243 called sql.env and add SQL_USER={your usrename} and SQL_PASSWORD={your password} and add sql.env to your .gitignore.
20) Now cd to environment and run npm install
21) Run pip install flask-socketio to install socketIO
22) Run pip install eventlet
23) Run npm install -g webpack
24) Run npm install --save-dev webpack
25) Run npm install socket.io-client --save
If you see any error messages, make sure you use sudo pip or sudo npm. If it says "pip cannot be found", run which pip and use sudo [path to pip from which pip] install
26) Open the file in vim: sudo vim /var/lib/pgsql9/data/pg_hba.conf
27) Run :%s/ident/md5/g to Replace all values of ident with md5
28) Run sudo service postgresql restart
29) Run npm install react-linkify --save
30) Run pip install googletrans
31) Run npm install react-google-login
32) Run npm run watch in one terminal (The program should not stop running. Leave it running.) If this step fails for whatever reason, please close your terminal and restart it, and re-run the command.
33) Open a new terminal and run python app.py
34) Make sure you hard refresh (Ctrl+R/Cmd+Shift+R) for HTML changes you make
35) One issue I had was getting the username to display with the texts. This is because when I called it from the state variable in Javascript, it showed as 
[Object object] but showed correctly in the return statement. When I looked it up online it said useEffect doesn't immediately update the state variables.
Another issue I had was creating a new database, because I was using Models.py at first. When I made my own I tried to make it as similar to Models as I could,and the datatypes were too small to hold the messages so it was throwing some errors which I fixed
36) I ran in to multiple technical errors during this project. When deploying to heroku the page could not read my script.js file. The reason for this was that my script.js file was in my .gitignore. However when I tried uploading my changes to heroku it was giving me another error about not having societio dependecncy. But it was wokring before that so I was confused why it had this issue all of a sudden. I ended up going through a couple steps but I had to manually add that dependency in my package.json, and also delete --watch from line 7 of it, becuase it was take a long time to upload to heroku otherwise
Another technical issue I overcame was was my git was pulling from an old repo even though it was set to a new repo. It was pulling multiple copies of a file, and also pulling a file I had deleted several commits ago. I fixed this by deleting my entire folder and creating a new one.

