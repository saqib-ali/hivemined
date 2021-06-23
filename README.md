This is a Getting Started app to demo the connectivity to CockroachCloud DB from Heroko or DigitalOcean App Platform. 

DBCONNSTR is set in the Heroku or DigitalOcean App setting environment variable as:
```
postgres://{username}:{password}@{cockroachcloudhostname}:26257/{clustername}.{databasename}?sslmode=require
postgres://{username}:{password}@free-tier4.aws-us-west-2.cockroachlabs.cloud:26257/{clustername}.defaultdb?sslmode=require

```
