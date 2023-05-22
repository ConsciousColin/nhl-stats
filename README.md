# NHL Stats Data + dbt + duck DB
A very much work in progress side project exploring the data the NHL makes available and what we can do with it. 

## Extract data from the NHL Stats API 
A simple flask app that pulls data from the NHL Stats API and writes it to parquet files.

## Process extracted data into duckdb
Use dbt to build higher level tables in duckdb. 


## What's next?
* Make duck db database available to the public
* Schedule data extraction and dbt runs