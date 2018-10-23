#!/usr/bin/python3.6

import asyncio
import websockets
import argparse


from kafka import KafkaConsumer

import conf as co


parser = argparse.ArgumentParser()
parser.add_argument('port', metavar='port', type=int, help='tcp port')
parser.add_argument('topic', metavar='kafka topic', type=str, help='topic of kafka')

consumer = None


async def SendEvt(websocket,path):
    for m in consumer:
        await websocket.send(m.value.decode())
        print("sent event %s" % m.value.decode())




if __name__ == "__main__":

    args = parser.parse_args()
    consumer = KafkaConsumer(args.topic,bootstrap_servers=co.ka_host, auto_offset_reset='latest')
    start_server = websockets.serve(SendEvt, '0.0.0.0', args.port)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
