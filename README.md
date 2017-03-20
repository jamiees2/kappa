# kappa

A project euler like contest environment.

## Setup
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
Start postgressql :
```
sudo systemctl start postgressql
```
Login as the newly created postgres user and initalize the database user and database ( This user was created for you ) :
```
sudo su - postgres
./db/setup_db.sh epsilon "epsilon" epsilon
```
This instruction leaves the default database password as "epsilon", this should be okay since this user only has access to the epsilon table.
And the database is only accessible from your computer. 

Setting the app.secret_key, this is done in kappa.py on line 45. Remcomendations regarding the key can be found : [secret key](http://flask.pocoo.org/docs/0.12/quickstart/)
## Run
Starting the program:
```
python3 kappa.py <contest_dir>
```

Build a contest:
```
problems/build_contest <contest_dir>
```
## creating problems
For the contest format, see an example contest at `example_contest`.

Based on &epsilon;, see [epsilon](https://github.com/ForritunarkeppniFramhaldsskolanna/epsilon)
