import click
import requests
import json
import time
import random

session = requests.session()

metric_prefix = "system.load_test"
tagk_prefix = "tagk"
tagv_prefix = "tagv"


def init_prefix():
    # one hour one prefix: for tagv
    s_one_hour = int(time.time()) / 60 / 60
    # one day one prefix: for tagk
    s_one_day = s_one_hour / 24
    # one week one prefix: for metric name
    s_one_week = s_one_day / 7

    global metric_prefix, tagk_prefix, tagv_prefix
    metric_prefix = "system.load_test.{}".format(s_one_day)
    tagk_prefix = "tagk_{}".format(s_one_week)
    tagv_prefix = "tagv_{}".format(s_one_hour)


def compose_tags(tags_count):
    tags = {}
    i = 0
    while i < tags_count:
        tags["{}_{}".format(tagk_prefix, random.randint(1, 100))] = \
            "{}_{}".format(tagv_prefix, random.randint(1, 100))
        i += 1
    return tags


def compose_package(size, tags_count):
    data = []
    i = 0
    while i < size:
        i += 1
        item = {
            "timestamp": int(time.time()) * 1000,
            "metric": "{}.metric{}".format(metric_prefix, i),
            "value": random.randint(1, 100),
            "tags": compose_tags(tags_count)
        }

        data.append(item)

    return data


def send_data(data, opentsdb):
    url = "{}/api/put".format(opentsdb.strip('/'))
    try:
        response = session.post(url, data=json.dumps(data), timeout=2)
        if response.status_code != 204:
            click.echo(data)
            click.echo(response.content)

    except Exception as e:
        click.echo(e.message)


@click.command()
@click.option('--duration', default=-1,
              help='Test duration, -1 means infinite.')
@click.option('--tags', default=8,
              help='Tags count for one metric.')
@click.option('--mpp', default=200,
              help='Metrics per packet.')
@click.option('--pps', default=1,
              help='Packets per second')
@click.option('--opentsdb', default="http://localhost:4242",
              help='Opentsdb server address')
@click.option('--verbose', default=False,
              help='Whether to show debug')
def load_test(duration, mpp, tags, pps, opentsdb, verbose):
    click.echo('load_test duration: %s' % duration)
    click.echo('load_test mpp: %s' % mpp)
    click.echo('load_test tags: %s' % tags)
    click.echo('load_test pps: %s' % pps)
    click.echo('load_test opentsdb: %s' % opentsdb)
    click.echo('load_test verbose: %s' % verbose)
    init_prefix()

    start = int(time.time())
    time_that_second = int(time.time())
    packet_sent_this_second = 0
    total_sent = 0
    while True:
        # stop if exceed duration
        if duration > 0:
            if start + duration < int(time.time()):
                break

        time_this_second = int(time.time())
        if time_this_second != time_that_second:
            packet_sent_this_second = 0
            time_that_second = time_this_second

        if packet_sent_this_second < pps:
            data = compose_package(mpp, tags)
            if verbose:
                click.echo(json.dumps(data, indent=2))
            send_data(data, opentsdb)
            packet_sent_this_second += 1
            total_sent += mpp
        else:
            x = time.time()
            y = int(x) + 1
            click.echo("{}: will sleep {}".format(time_this_second, (y - x)))
            time.sleep(y - x)

    click.echo("total sent: {}".format(total_sent))


if __name__ == '__main__':
    load_test()
