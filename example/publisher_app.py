from gulpster.publisher.ioloop import Publisher

class App(object):
	def main(self):
		publisher = Publisher()

		try:
			publisher.run()
		except KeyboardInterupt:
			publisher.stop()
		

	def run(self):
		self.main()

App().run()
