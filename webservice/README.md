## How to setup

1. create virtual environment using `conda create --name iot python=3.6`
2. use virtual environment we just created: `conda activate iot`
3. install required packages: `pip install -r requirements.txt`


## How to run in SSL mode

1. ssh into the server
2. go to `/home/proverbs/iot/selfiot/webservice`
3. run `sudo python manage.py runsslserver --certificate ../www.proverbs.top/fullchain1.pem --key ../www.proverbs.top/privkey1.pem 0.0.0.0:3000`
