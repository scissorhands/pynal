from requester import Requester
from dbconnector import Connector
import json
import datetime as dt


class Etl:
	def __init__(self):
		self.req = Requester()
		self.connector = Connector()

	def get_report_dictionary(self, report):
		columnHeader = report.get('columnHeader', {})
		return {
			'columnHeader': columnHeader,
			'dimensionHeaders': columnHeader.get('dimensions', []),
			'metricHeaders': columnHeader.get('metricHeader', {}).get('metricHeaderEntries', []),
			'rows': report.get('data', {}).get('rows', [])
		}

	def formatted_output(self, input):
		stats = []
		for report in input.get('reports', []):
			rdictionary = self.get_report_dictionary(report)
			for row in rdictionary['rows']:
				stat = {}
				dimensions = row.get('dimensions', [])
				dateRangeValues = row.get('metrics', [])
				for header, dimension in zip(rdictionary['dimensionHeaders'], dimensions):
					hd = header.replace('ga:', '')
					if(hd == 'date'):
						dimension = dt.datetime.strptime(dimension, '%Y%m%d').strftime('%Y-%m-%d')
					stat[hd] = dimension
				for i, values in enumerate(dateRangeValues):
					for metricHeader, value in zip(rdictionary['metricHeaders'], values.get('values') ):
						stat[metricHeader.get('name').replace('ga:', '')] = value
				stats.append(stat) 
		return stats

	def retrieve_all_stats(self, destroy_after=True):
		self.retrieve_hostname_stats(False)
		self.retrieve_city_stats(False)
		self.retrieve_region_stats(False)
		self.retrieve_devices_stats(False)
		if (destroy_after):
			self.connector.serv_destory()


	def retrieve_hostname_stats(self, destroy_after=True):
		print('getting hostname stats')
		report = self.req.get_hostname_stats( '2017-01-01' )
		stats = self.formatted_output(report)
		for row in stats:
			self.connector.insert_ignore("analytics_hostname_stats",row)
		if (destroy_after):
			self.connector.serv_destory()

	def retrieve_city_stats(self, destroy_after=True):
		print('getting city stats')
		report = self.req.get_city_stats( '2017-01-01' )
		stats = self.formatted_output(report)
		for row in stats:
			self.connector.insert_ignore("analytics_city_stats",row)
		if (destroy_after):
			self.connector.serv_destory()

	def retrieve_region_stats(self, destroy_after=True):
		print('getting region stats')
		report = self.req.get_region_stats( '2017-01-01' )
		stats = self.formatted_output(report)
		for row in stats:
			self.connector.insert_ignore("analytics_region_stats",row)
		if (destroy_after):
			self.connector.serv_destory()

	def retrieve_devices_stats(self, destroy_after=True):
		print('getting devices stats')
		report = self.req.get_devices_stats( '2017-01-01' )
		stats = self.formatted_output(report)
		for row in stats:
			self.connector.insert_ignore("analytics_device_stats",row)
		if (destroy_after):
			self.connector.serv_destory()

def main():
	etl = Etl()
	etl.retrieve_all_stats()

if __name__ == '__main__':
	main()