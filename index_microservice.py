from requester import Requester
import json
req = Requester()
localTest = False

print('Loading function')


def respond(err, res=None):
    return {
        'statusCode': '400' if err else '200',
        'body': err.message if err else json.dumps(res),
        'headers': {
            'Content-Type': 'application/json',
        },
    }


def lambda_handler(event, context):
    operations = {
        'GET'
    }

    operation = event['httpMethod']
    if operation in operations:
        method = event['queryStringParameters']['method']
        api_methods = {
            'get_hostname_stats',
            'get_city_stats',
            'get_region_stats',
            'get_devices_stats'
        }
        if method in api_methods:
            stats = getattr(req,  method)()
            if(localTest):
                print(stats)
            return respond(None, stats)
        else:
            return respond(ValueError("Unsupported method '{}'".format(method)))
    else:
        return respond(ValueError('Unsupported http method "{}"'.format(operation)))

if __name__ == '__main__':
    localTest = True
    event = {
        'httpMethod': 'GET',
        'queryStringParameters': {
            'method': 'get_hostname_stats'
        }
    }
    lambda_handler(event, None)