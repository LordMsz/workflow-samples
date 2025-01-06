1. Open container with all dependent services
2. Run `/bin/python3 01_basic_spark.py` or other scripts (TODO: fix Python path)
    - alternatively `/opt/spark/bin/spark-submit 01_basic_spark.py` to submit to cluster
3. Open http://localhost:8080/ and http://localhost:4040/

To query Postgres:
Open interactively the container and run `psql -U postgres`
select * from filtered_data;