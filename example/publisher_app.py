from gulpster.publisher import Publisher

class App(object):
	def main(self):
		publisher = Publisher()

		publisher.connect()
		publisher.start_publishing()

	def run(self):
		self.main()

App().run()
