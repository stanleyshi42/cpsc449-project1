import sys
import http.client
import json
import urllib

def main(path):
    # Retrieve data from FOAAS API
    connection = http.client.HTTPSConnection('www.foaas.com')
    headers = {'Accept': 'application/json'}
    connection.request('GET', path, '',headers)

    foaasResponse = connection.getresponse().read()
    foaasResponse = json.loads(foaasResponse)
    foaasString = urllib.parse.quote(foaasResponse['message'])

    # Retrieve data from PurgoMalum API
    connection = http.client.HTTPSConnection('www.purgomalum.com')
    connection.request('GET', '/service/json?text='+foaasString)

    purgoResponse = connection.getresponse().read()
    purgoResponse = json.loads(purgoResponse)

    # Format and return result
    foaasResponse['message'] = purgoResponse['result']
    foaasResponse = json.dumps(foaasResponse, indent = 2)
    print(foaasResponse)
    return foaasResponse

if __name__ == '__main__':
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        print('Usage: redact URL')