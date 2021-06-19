This demo app is hosted on DigitalOcean App Platform.

CockroachCloud is the database for this app.

DBCONNSTR is set in the DigitalOcean App setting environment variable as:
```
postgres://{username}:{password}@{cockroachcloudhostname}:26257/{clustername}.{databasename}?sslmode=require
```
