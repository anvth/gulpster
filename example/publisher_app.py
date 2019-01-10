from gulpster.event import Event
from gulpster.publisher.blocking import Publisher


class App(object):
    def main(self):
        publisher = Publisher()
        publisher.connect()

        evt = Event("com.home.test", {})
        publisher.start_publishing(evt)

    def run(self):
        self.main()


if __name__ == '__main__':
    App().run()
