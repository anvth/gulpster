from gulpster.publisher.ioloop import Publisher


class App(object):
    def main(self):
        publisher = Publisher()
        try:
            publisher.run()
        except KeyboardInterrupt as e:
            publisher.stop()

    def run(self):
        self.main()


if __name__ == '__main__':
    App().run()
