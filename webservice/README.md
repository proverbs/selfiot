## How to run in SSL mode

1. ssh into the server
2. go to `/home/proverbs/iot/selfiot/webservice`
3. run `sudo python manage.py runsslserver --certificate ../www.proverbs.top/fullchain1.pem --key ../www.proverbs.top/privkey1.pem 0.0.0.0:3000`
