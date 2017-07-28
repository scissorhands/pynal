import config
import argparse

from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

import httplib2
from oauth2client import client
from oauth2client import file
from oauth2client import tools

import json

SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
DISCOVERY_URI = ('https://analyticsreporting.googleapis.com/$discovery/rest')
KEY_FILE_LOCATION = config.key_file_location
SERVICE_ACCOUNT_EMAIL = config.service_account_email
VIEW_ID = config.view_id


def initialize_analyticsreporting():
  credentials = ServiceAccountCredentials.from_p12_keyfile(
    SERVICE_ACCOUNT_EMAIL, KEY_FILE_LOCATION, scopes=SCOPES)
  http = credentials.authorize(httplib2.Http())
  analytics = build('analytics', 'v4', http=http, discoveryServiceUrl=DISCOVERY_URI)
  return analytics


def get_report(analytics):
  return analytics.reports().batchGet(
      body={
        'reportRequests': [
        {
          'viewId': VIEW_ID,
          'dateRanges': [{'startDate': '7daysAgo', 'endDate': 'today'}],
          'metrics': [
            {'expression': 'ga:sessions'},
            {'expression': 'ga:pageViews'},
            {'expression': 'ga:avgTimeOnPage'},
            {'expression': 'ga:exits'},
            {'expression': 'ga:organicSearches'}
          ],
          'dimensions': [ 
            # {'name':'ga:pagepath'},
            {'name':'ga:hostname'},
            # {'name':'ga:city'},
            # {'name':'ga:browser'},
            # {'name':'ga:date'}
          ]
        }]
      }
  ).execute()

def generic_request(analytics, metrics, dimensions, start = '7daysAgo', end='today'):
  return analytics.reports().batchGet(
    body={
      'reportRequests': [{
        'viewId': VIEW_ID,
        'dateRanges': [{'startDate': start, 'endDate': end}],
        'metrics': metrics,
        'dimensions': dimensions
      }]
    }
  ).execute()


def print_response(response):
  for report in response.get('reports', []):
    columnHeader = report.get('columnHeader', {})
    dimensionHeaders = columnHeader.get('dimensions', [])
    metricHeaders = columnHeader.get('metricHeader', {}).get('metricHeaderEntries', [])
    rows = report.get('data', {}).get('rows', [])

    for row in rows:
      dimensions = row.get('dimensions', [])
      dateRangeValues = row.get('metrics', [])
      for header, dimension in zip(dimensionHeaders, dimensions):
        print( header + ': ' + dimension)

      for i, values in enumerate(dateRangeValues):
        print( 'Date range (' + str(i) + ')')
        for metricHeader, value in zip(metricHeaders, values.get('values')):
          print( metricHeader.get('name') + ': ' + value)
      print()


def main():
  print()
  analytics = initialize_analyticsreporting()
  try:
    response = get_report(analytics)
    print_response(response)
  except Exception as e:
    print(e)
  finally:
    print()

if __name__ == '__main__':
  main()
