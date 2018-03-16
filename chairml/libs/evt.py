# -*- coding: utf-8 -*-

from typing import Callable, Iterable, Union, Optional, List, AnyStr, Dict, BinaryIO
import asyncio
from urllib.parse import unquote_plus
import aiohttp
import uvloop
import sys
import requests
import io

ATTEMPTS = 6

def list_properties(host: str, api_key: str, thng_id: str) -> Dict:
    res = requests.get(f"https://{host}/thngs/{thng_id}",
                       headers={"Authorization": api_key, "Content-Type": "application/json"})
    thng = res.json()
    if thng:
        return thng['properties']
    else:
        raise Exception(f'thng {thng_id} not found')

def get_account_info(host, api_key):
    headers = {"Authorization": api_key, "Content-Type": "application/json"}
    res = requests.get("https://{}/access".format(host), headers=headers)
    if not res.json():
        raise Exception('API key not found')
    return res.json()


def get_app_key_context(host: str, api_key: str)->dict:
    account = get_account_info(host, api_key)
    if account['actor']['type']!='app':
        raise Exception('This key is an {}. Use an app key or trusted app key instead'.format(account['actor']['type']))
    else:
        return dict(account_id=account['account'], project_id=account['project'], app_id=account['actor']['id'])


def deploy_reactor_script(host: str, operator_api_key: str, project_id: str, app_id: str, bundle: io.BytesIO):
    url = 'https://{host}/projects/{project_id}/applications/{app_id}/reactor/script'.format(
        host=host,
        project_id=project_id,
        app_id=app_id)
    print(url)
    headers = {"Authorization": operator_api_key}
    # fp = open('./bundle.zip','rb')
    files = {'file':bundle}
    res = requests.put(url,
                       headers=headers,
                       files=files)
    return res

async def get_everythng(url: str, session: aiohttp.ClientSession, headers: Dict):
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


async def main(url: str, api_key: str, data: List):
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


def get_thngs(host, api_key, collection_id=None):
    data = []
    loop = None
    try:
        loop = uvloop.new_event_loop()
        asyncio.set_event_loop(loop)
        if collection_id:
            url = "https://{host}/collections/{collection_id}/thngs?perPage=100".format(host=host,
                                                                                        collection_id=collection_id)
        else:
            url = "https://{host}/thngs?perPage=100".format(host=host)
        loop.run_until_complete(main(url, api_key, data))
    except aiohttp.client_exceptions.ClientConnectorError as e:
        print(e, file=sys.stderr)
    finally:
        loop.close()
    return data


async def get_thng(api_key, thng_id):
    headers = {"Authorization": api_key, "Content-Type": "application/json"}
    async with aiohttp.ClientSession() as session:

        async with session.get(
                url="https://api.evrythng.com/thngs/%s" % thng_id,
                headers=headers) as resp:

            try:
                data = await resp.json()

                if 200 <= resp.status < 300:
                    return data
            except aiohttp.ClientConnectorError as e:
                print(e, file=sys.stderr)
            except TimeoutError as e:
                print(e, file=sys.stderr)
    return []


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


def get_properties(host, api_key, thng_id, thng_property, begin, end):
    data = []
    loop = None
    try:
        loop = uvloop.new_event_loop()
        asyncio.set_event_loop(loop)
        url = f"https://{host}/thngs/{thng_id}/properties/{thng_property}?filter=timestamp={begin}..{end}&perPage=100"

        loop.run_until_complete(main(url, api_key, data))
    except aiohttp.client_exceptions.ClientConnectorError as e:
        print(e, file=sys.stderr)
    finally:
        loop.close()
    return data

def list_properties(host, api_key, thng_id):
    res = requests.get(f"https://{host}/thngs/{thng_id}",
                       headers={"Authorization": api_key, "Content-Type": "application/json"})
    thng = res.json()
    if thng:
        return thng['properties']
    else:
        raise Exception(f'thng {thng_id} not found')

def evt_training_data(host, api_key, thng_prop, collection_id):
    for thng in get_thngs(host, api_key, collection_id):
        if thng_prop in thng['properties']:
            yield thng['id'], get_property_events(host, api_key, thng['id'], thng_prop)
