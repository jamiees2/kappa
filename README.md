# kappa

A project euler like contest environment.

dependencies:
To run this software you must first install all dependencies specified in problemtools.
initalize the submodules
```
git submodule init
git submodule update
```
install pip requirements
```
sudo -H pip3 install -r requirements.txt
```
setup postgres sql
```
sudo apt install postgressql
```
Create a user for the kappa system. default username epsilon ( that can stay the same ),
Edit kappa.py and enter a random string into the app.secret. This should be long and secure. Start postgressql.
```
sudo systemctl start postgressql
```
Login as the newly created postgres user and initalize the database user and database
```
sudo su - postgres
./db/setup_db.sh epsilon "The secret you created earlier" epsilon
```

To run:
```
python3 kappa.py <contest_dir>
```

To build a contest:
```
problems/build_contest <contest_dir>
```

For the contest format, see an example contest at `example_contest`.

Based on &epsilon;, see [epsilon](https://github.com/ForritunarkeppniFramhaldsskolanna/epsilon)
