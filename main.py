import os
import requests
import datadog

config = {
    'api_url'   : 'https://www.site24x7.com/api/',
    'zoho_token': os.environ["ZOHO_TOKEN"],
    'dd_api_key': os.environ["DATADOG_API_KEY"],
    'dd_app_key': os.environ["DATADOG_APP_KEY"],
    'monitoring_id': os.environ["MONITORING_ID"]
}

headers = {
    'Accept': 'application/json; version=2.0',
    'Authorization': 'Zoho-authtoken {}'.format(config['zoho_token'])
}

stats = None

'''
    Endpoint returns response time for each location you setup
'''
def get_response_times():
    response = requests.get(config['api_url'] + 'current_status/' + config['monitoring_id'], headers=headers)
    monitoring_response = response.json()

    for location in monitoring_response['data']['locations']:
        tag = ['location:' + str(location['location_name'])]
        stats.gauge('buffer.health.24x7_latency', location['attribute_value'], tags=tag)

'''
    Endpoint returns the uptime according a given period
    https://www.site24x7.com/help/api/#summary-by-monitor
'''
def get_uptimes():
    periods = [
        "0", #last 1 hour
        "1", #last 24 hours
        "2", #last 7 days
        "5"  #last 30 days
    ]

    for period in periods:
        response = requests.get(config['api_url'] + 'reports/summary/' + config['monitoring_id'] + '?unit_of_time=1&period=' + period, headers=headers)
        r = response.json()
        tag = ['period:' + str(r['data']['info']['period_name'])]
        stats.gauge('buffer.health.24x7_availability', r['data']['summary_details']['availability_percentage'], tags=tag)

    return

def process():
    get_response_times()
    get_uptimes()

def _init_datadog():
    dd_options = {
    'api_key': config['dd_api_key'],
    'app_key': config['dd_app_key']
    }

    datadog.initialize(**dd_options)
    stats = datadog.ThreadStats()
    stats.start()
    return stats

if __name__ == "__main__":
    stats = _init_datadog()
    process()
