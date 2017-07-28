import analytics as service

class Requester:
	def __init__(self):
		self.analytics = service.initialize_analyticsreporting()

	def get_hostname_stats(self):
		return service.generic_request(self.analytics,
			[
				{'expression': 'ga:sessions'},
				{'expression': 'ga:pageViews'},
				{'expression': 'ga:avgTimeOnPage'},
				{'expression': 'ga:exits'},
				{'expression': 'ga:organicSearches'}
	       	],
	       	[
	       		{'name' : 'ga:hostname'}, 
	       		# {'name' : 'ga:pagePath'},
	       		{'name' : 'ga:date'}
	       	]
	    )

	def get_city_stats(self):
		return service.generic_request(self.analytics,
			[
				{'expression': 'ga:sessions'},
				{'expression': 'ga:pageViews'},
				{'expression': 'ga:avgTimeOnPage'},
				{'expression': 'ga:exits'},
				{'expression': 'ga:organicSearches'}
	       	],
	       	[
	       		{'name' : 'ga:hostname'},
	       		{'name' : 'ga:city'}, 
	       		{'name' : 'ga:date'}
	       	]
	    )

	def get_region_stats(self):
		return service.generic_request(self.analytics,
			[
				{'expression': 'ga:sessions'},
				{'expression': 'ga:pageViews'},
				{'expression': 'ga:avgTimeOnPage'},
				{'expression': 'ga:exits'},
				{'expression': 'ga:organicSearches'}
	       	],
	       	[
	       		{'name' : 'ga:hostname'},
	       		{'name' : 'ga:region'}, 
	       		{'name' : 'ga:date'}
	       	]
	    )