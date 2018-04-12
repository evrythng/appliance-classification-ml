# -*- coding: utf-8 -*-

import asyncio
import sys
from typing import List, Dict, Coroutine
from urllib.parse import unquote_plus

import aiohttp
import requests
import uvloop

ATTEMPTS = 6


async def _get_everything(url: str, session: aiohttp.ClientSession, headers: Dict):
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


async def _main(url: str, api_key: str, data: List):
    headers = {"Authorization": api_key, "Content-Type": "application/json"}
    async with aiohttp.ClientSession() as session:
        while url:
            attempts_left = ATTEMPTS
            exception = None
            while attempts_left > 0:
                try:
                    url, res = await _get_everything(url, session, headers)
                    # asyncio.sleep(0.01)
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


def _async_runtime(fn_async: Coroutine):
    loop = None
    try:
        loop = uvloop.new_event_loop()
        loop.run_until_complete(fn_async)
    except aiohttp.client_exceptions.ClientConnectorError as e:
        print(e, file=sys.stderr)
    finally:
        loop.close()


def get_actions(host: str, operator_api_key: str, action_type: str) -> List:
    data = []
    url = "https://{}/actions/{}?perPage=100".format(host, action_type)
    _async_runtime(_main(url, operator_api_key, data))
    return data


def get_thngs(host: str, api_key: str, collection_id=None):
    data = []
    if collection_id:
        url = "https://{host}/collections/{collection_id}/thngs?perPage=100".format(host=host,
                                                                                    collection_id=collection_id)
    else:
        url = "https://{host}/thngs?perPage=100".format(host=host)
    _async_runtime(_main(url, api_key, data))
    return data


def get_property_events(host: str, api_key: str, thng_id: str, thng_property: str, begin=None, end=None) -> List:
    data = []
    if begin and end:
        url = f"https://{host}/thngs/{thng_id}/properties/{thng_property}?filter=timestamp={begin}..{end}&perPage=100"
    else:
        url = f"https://{host}/thngs/{thng_id}/properties/{thng_property}"
    _async_runtime(_main(url, api_key, data))
    return data


def list_properties(host: str, api_key: str, thng_id: str) -> Dict:
    res = requests.get(f"https://{host}/thngs/{thng_id}",
                       headers={"Authorization": api_key, "Content-Type": "application/json"})
    thng = res.json()
    if thng:
        return thng['properties']
    else:
        raise Exception(f'thng {thng_id} not found')


def get_account_info(host: str, api_key: str) -> Dict:
    headers = {"Authorization": api_key, "Content-Type": "application/json"}
    res = requests.get("https://{}/access".format(host), headers=headers)
    if not res.json():
        raise Exception('API key not found')
    return res.json()