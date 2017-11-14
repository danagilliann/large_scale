# large_scale

### notes
- Copy/paste Scalica
- Full deployment —> Scalia scripts (adj. 2-3 lines)
- 2 nodes 
- 1 node: app server —> http server/web server
- 1 node: database
- 1 node: hadoop
    - automated to some degree
    - htp servers
    - least painful: in memory or google data flow or amazon map reduce
    - script periodically runs job => through db
    - “sqoop”: dedup
    - cron linux
    - read/write in db directly
    - read actual schema and connect to table directly —> bypass orm
- batch job
    - not super fancy
    - real duplicates 
- google data flow/amazon
    - stage data —> costly
    - a bit more complicated
    - upside: worry about logic
    - data flow: understanding new technology
    - amazon: free tier
- local in memory
    - easiest

