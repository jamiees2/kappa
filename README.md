# kappa

A project euler like contest environment.
# Setup
dependencies:
To run this software you must first install all dependencies specified in problemtools : [problemtools](https://github.com/Kattis/problemtools/tree/121bf4eff7679cebc1104c1e1146f072f8ff449d)

initalize the submodules ( including the prementioned problemtools ) :
```
git submodule init
git submodule update
```
install pip requirements :
```
sudo -H pip3 install -r requirements.txt
```
setup postgres sql :
```
sudo apt install postgressql
```
Edit kappa.py and enter a random string into the app.secret that is used as a database password. This should be long and secure. 
    
Start postgressql :
```
sudo systemctl start postgressql
```
Login as the newly created postgres user and initalize the database user and database ( This user was created for you ) :
```
sudo su - postgres
./db/setup_db.sh epsilon "The secret you created earlier" epsilon
```

# Run
Starting the program:
```
python3 kappa.py <contest_dir>
```

Build a contest:
```
problems/build_contest <contest_dir>
```
# creating problems
For the contest format, see an example contest at `example_contest`.

Based on &epsilon;, see [epsilon](https://github.com/ForritunarkeppniFramhaldsskolanna/epsilon)
