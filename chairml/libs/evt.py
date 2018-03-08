import asyncio
from urllib.parse import unquote_plus
import aiohttp
import uvloop
import ujson
import sys
import numpy as np
from keras.preprocessing import  sequence
# -*- coding: utf-8 -*-

ATTEMPTS = 6


async def get_everythng(url, session, headers):
    async with session.get(url, headers=headers) as resp:
        data = await resp.json()
        if 200 <= resp.status < 300:
            if 'link' in resp.headers and resp.headers['link']:
                next_url, rel = unquote_plus(resp.headers['link']).split(';')
                if next_url:
                    next_url = next_url[1:-1]
            else:
                next_url = None
            return next_url, data
        else:
            return None, []


async def main(url, api_key, data):
    headers = {"Authorization": api_key, "Content-Type": "application/json"}
    async with aiohttp.ClientSession() as session:
        while url:
            attempts_left = ATTEMPTS
            exception = None
            while attempts_left > 0:
                try:
                    url, res = await get_everythng(url, session, headers)
                    asyncio.sleep(0.01)
                except aiohttp.client_exceptions.ClientConnectorError as e:
                    print(e, file=sys.stderr)
                    wait_for = ATTEMPTS / attempts_left
                    print(f'Waiting for {wait_for:1.3f}')
                    asyncio.sleep(wait_for)
                    attempts_left -= 1
                    exception = e
                else:
                    data.extend(res)
                    break
                finally:
                    if attempts_left == 0:
                        raise exception
                    print(f'Downloaded {len(data)}')


def get_thngs(host, api_key,collection_id=None):
    data = []
    loop = None
    try:
        loop = uvloop.new_event_loop()
        asyncio.set_event_loop(loop)
        if collection_id:
            url = "https://{host}/collections/{collection_id}/thngs?perPage=100".format(host=host,collection_id=collection_id)
        else:
            url = "https://{host}/thngs?perPage=100".format(host=host)
        loop.run_until_complete(main(url, api_key, data))
    except aiohttp.client_exceptions.ClientConnectorError as e:
        print(e, file=sys.stderr)
    finally:
        loop.close()
    return data





def get_property_events(host, api_key, thng_id, thng_prop):
    loop = None
    data = []
    try:
        loop = uvloop.new_event_loop()
        asyncio.set_event_loop(loop)
        url = 'https://{host}/thngs/{thng_id}/properties/{thng_prop}?perPage=100'.format(host=host, thng_id=thng_id,
                                                                                         thng_prop=thng_prop)
        loop.run_until_complete(main(url, api_key, data))
    except aiohttp.client_exceptions.ClientConnectorError as e:
        print(e, file=sys.stderr)
    finally:
        loop.close()
    return data


def mortion_property_value(*data):
    for d in data:
        if type(d['value']) is str:
            try:
                d['value'] = ujson.loads(d['value'])
                if type(d['value']) is list and d['value']:
                    yield d
                else:
                    print('empty {}'.format(d))
                    continue
            except ValueError as e:
                print(e, file=sys.stderr)


def evt_training_data(host, api_key, thng_prop, collection_id):
    for thng in get_thngs(host, api_key,collection_id):
        if thng_prop in thng['properties']:
            yield thng['id'], get_property_events(host, api_key, thng['id'], thng_prop)

