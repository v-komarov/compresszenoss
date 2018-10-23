#!/usr/bin/python3.6
#coding:utf-8

import json
import asyncio
import argparse
from pymemcache.client import base
from kafka import KafkaProducer,KafkaConsumer

import conf as co



parser = argparse.ArgumentParser()
parser.add_argument('topic_consumer', metavar='topic-consumer', type=str, help='topic of region zenoss')
parser.add_argument('topic_producer', metavar='topic-producer', type=str, help='topic of summarize zenoss')
parser.add_argument('prefix', metavar='prefix', type=str, help='prefix id of events')





def to_topic(producer,msg,evid,status_severity,mch,topic_producer,ttl):
    
    mch.set(evid,status_severity,ttl)
    producer.send(topic_producer, json.dumps(msg).encode())
    




async def Compress(consumer,producer,prefix,mch,topic_producer):

    for m in consumer:
        msg = json.loads(m.value.decode())
        evid = u"{}-{}".format(prefix,msg["evid"])
        status_severity = u"{}-{}".format(msg["status"],msg["severity"])
        msg["evid"] = evid
        severity = msg["severity"]

        if severity not in ("Info","Debug","Clear"):

            ### Проверка существования ключа
            r = mch.get(evid)


            if r:
                # Проверка значения
                if r.decode() != status_severity:
                    print(u"ключи не равны! {} и {}".format(r.decode(),status_severity))
                
                    ## Запись кэш
                    to_topic(producer,msg,evid,status_severity,mch,topic_producer,20)
                else: 
                    print(u"ключи равны! {} и {}".format(r.decode(),status_severity))
            else:

                ## Запись кэш
                to_topic(producer,msg,evid,status_severity,mch,topic_producer,30)

                print(m.value.decode())






if __name__ == "__main__":

    args = parser.parse_args()
    topic_consumer = args.topic_consumer
    topic_producer = args.topic_producer
    prefix = args.prefix

    ### kafka
    producer = KafkaProducer(bootstrap_servers=co.ka_host)
    consumer = KafkaConsumer(topic_consumer,bootstrap_servers=co.ka_host, auto_offset_reset='latest')
    
    ### memcached
    mch = base.Client((co.memcache_host,co.memcache_port))


    asyncio.get_event_loop().run_until_complete(Compress(consumer,producer,prefix,mch,topic_producer))
    asyncio.get_event_loop().run_forever()

