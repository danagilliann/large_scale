Group 8 Project Submission
---
* Go to: `http://104.196.149.173/micro/`
* username: `test`
* password: `test`
* note: the university for `test` is set to NYU, so you can only post questions in the NYU page

To try out the remove-duplicate feature
---
* Go to `http://35.227.70.109/micro/university/1/`
* Create a new question that has already been asked
* Run the batch job (next section)
* Refresh the page
* You should see that the question you just asked is marked as a duplicate

## Running the Batch Job
To run the job, first run have the database accept connections by running the following on the command-line:

```
cd /var/www/site/depot/dataflow
sudo python trigger_pipeline.py
```

## Install required packages
```
$ sudo apt-get update
$ sudo apt-get install mysql-server libmysqlclient-dev python-dev python-virtualenv
(Set a mysql root password)
$ ./first_install.sh
```

## Install the proper databases
```
$ cd db
$ ./install_db.sh
(Will ask for the mysql root password configured above).
$ cd ..
```

## Sync the database
```
$ source ./env/bin/activate
$ cd web/scalica
$ python manage.py makemigrations micro
$ python manage.py migrate
```


## After the first installation, from the project's directory, run the server
```
$ source ./env/bin/activate
$ cd web/scalica
$ python manage.py runserver
```

Access the site at `http://localhost:8000/micro`

## Steps to restart DB
```
1) in /web/scalica, run python manage.py flush
2) in /web/scalica, run rm -rf /micro/migrations/*
3) drop scalica database in mysql
4) redo all set-up steps in the github README starting from ./install_db.sh
```

## Connecting the Compute Engine instance to Cloud SQL instance
- https://cloud.google.com/sql/docs/mysql/connect-compute-engine
- use UNIX sockets instructions, not TCP socket instructions
- `service apache2 reload`

**Check**
```
cd var/www/site/scalica
ls
```
**You should have**
```
cloud_sql_proxy (executable)
creds.json (credentials for cloud sql)
manage.py
micro
scalica
utils
```



