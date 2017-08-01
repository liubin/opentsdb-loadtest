# opentsdb-loadtest
Simple load test for OpenTSDB 

# Install and run


```
$ pip install click
$ python load.py --help
```

Example:

```
 python load.py \
 --duration 10 \ # durate 10 seconds
 --pps 5 \ # 5 packet per second
 --mpp 400 \ # 400 metric per packet
 --tags 5 # 5 tags for one metric
```

In this example, we will send 20000 metrics( mpp * pps * duration), but there may be some error for about mpp * pps * 1 (second).