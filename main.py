
import os
import requests
import datadog

config = {
    'api_url'   : 'https://www.site24x7.com/api/',
    'zoho_token': os.environ["ZOHO_TOKEN"],
    # 'dd_api_key': os.environ["DATADOG_API_KEY"],
    # 'dd_app_key': os.environ["DATADOG_APP_KEY"],
    'statd_endpoint': os.environ["STATD_ENDPOINT"], # we use the dd agent to send metric to dd
    'monitoring_id': os.environ["MONITORING_ID"], # we use the dd agent to send metric to dd
}

def process():
    headers = {
        'Accept': 'application/json; version=2.0',
        'Authorization': 'Zoho-authtoken {}'.format(config['zoho_token'])
    }
    response = requests.get(config['api_url'] + 'current_status/' + config['monitoring_id'], headers=headers)
    monitoring_response = response.json()
    for location in monitoring_response['data']['locations']:
        print(location)

def _init_datadog():
    options = {
        # 'api_key': config['dd_api_key'],
        # 'app_key': config['dd_app_key'],
        'statsd_host': config['statd_endpoint']
    }
    datadog.initialize(**options)
    stats = datadog.ThreadStats()
    stats.start()
    return stats

if __name__ == "__main__":
    stats = _init_datadog()
    process()
