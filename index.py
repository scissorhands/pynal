from __future__ import print_function
import json
from etl import Etl

def lambda_connect(event, context):
	etl = Etl()
	etl.retrieve_all_stats()
	return 'pickle rick'

if __name__ == '__main__':
	lambda_connect(None, None)