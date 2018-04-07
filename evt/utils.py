import io

import requests

from evt.api import get_account_info


def get_app_key_context(host: str, api_key: str) -> dict:
    account = get_account_info(host, api_key)
    if account['actor']['type'] != 'app':
        raise Exception('This key is an {}. Use an app key or trusted app key instead'.format(account['actor']['type']))
    else:
        return dict(account_id=account['account'], project_id=account['project'], app_id=account['actor']['id'])


def deploy_reactor_script(host: str, operator_api_key: str, project_id: str, app_id: str, bundle: io.BytesIO):
    url = 'https://{host}/projects/{project_id}/applications/{app_id}/reactor/script'.format(
        host=host,
        project_id=project_id,
        app_id=app_id)
    headers = {"Authorization": operator_api_key}
    # fp = open('./bundle.zip','rb')
    files = {'file': bundle}
    res = requests.put(url,
                       headers=headers,
                       files=files)
    return res
