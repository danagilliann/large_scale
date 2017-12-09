This batch job marks questions as duplicates. It strips out the following words from each question before comparing if they're duplicate: "a", "an", "the", "is", "are", "can", "do", "will", "in", and "should". To run the job, first run have the database accept connections by running the following on the command-line:

```
./cloud_sql_proxy -instances=windy-watch-186102:us-central1:cora-sql=tcp:3306
```

Then, run the following Python script in a virtual environment:

```
python trigger_pipeline.py
```
