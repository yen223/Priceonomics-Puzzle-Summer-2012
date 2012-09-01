#!/usr/bin/env python 
import urllib2
import simplejson as json
from itertools import groupby
from datetime import datetime, date
from collections import defaultdict
from math import floor

def get_json_from_url(url="http://dl.dropbox.com/u/274/readings_formatted.json"):
    req = urllib2.Request(url)
    opener = urllib2.build_opener()
    f = opener.open(req)
    data = json.load(f)
    return data

def get_hourly_average(dataset, location, date, hour):
    local_data = dataset[location]
    index = 0

    for datum in local_data:
        print datum
    temps = [float(d['temperature']) for d in local_data 
            if d['timestamp'].date() == date
            and d['timestamp'].hour == hour]
    # print temps
    average = sum(temps)/len(temps)
    return average

def main():
    data = get_json_from_url()
    data.sort(key=lambda d:d['location'])
    dataset = defaultdict(list)
    for k, g in groupby(data, key=lambda d: d['location']):
        for datum in g:
            temperature = datum['temperature']
            ts = datetime.strptime(datum['timestamp'], "%Y-%m-%d %H:%M:%S")
            dataset[k].append({'temperature':temperature, 'timestamp':ts})
    data_SFO = dataset['SFO']
    data_NRT = dataset['NRT']
    data_IAD = dataset['IAD']

    #for key, val in dataset.iteritems():
    #    print key,":",val
    a = get_hourly_average(dataset, "NRT", date(2012,06,15),13) 
    b = get_hourly_average(dataset, "IAD", date(2012,06,16),14)
    c = get_hourly_average(dataset, "SFO", date(2012,06,17),13)

    print 'a=', a
    print 'b=', b
    print 'c=', c
    x = floor(c ** (b - a - 7))
    print 'x=', x

if __name__ == "__main__":
    main()
