from requester import Requester
import json
import datetime as dt


class Etl:
	def __init__(self):
		self.req = Requester()

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

	def retrieve_hostname_stats(self):
		report = self.req.get_hostname_stats()
		stats = self.formatted_output(report)
		print(stats)

	def retrieve_city_stats(self):
		report = self.req.get_city_stats()
		stats = self.formatted_output(report)
		print(stats)

	def retrieve_region_stats(self):
		report = self.req.get_region_stats()
		stats = self.formatted_output(report)
		print(stats)

def main():
	etl = Etl()
	etl.retrieve_region_stats()

if __name__ == '__main__':
	main()