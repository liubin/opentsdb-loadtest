# opentsdb-loadtest
Simple load test for OpenTSDB 

# Run in Docker

With default parameters:

```
docker run liubin/opentsdb-loadtest
```

Custom parameters:

```
docker run liubin/opentsdb-loadtest --opentsdb http://10.0.0.6:4242 --duration 10 --pps 5 --mpp 400 --tags 5
```

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
