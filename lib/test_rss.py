import feedparser
import yaml


class RssTester:

    def __init__(self):
        self.__dbm = DBManager()
        self.__config = self._read_sources()
        logging.info('Config are loaded')

    def _read_sources(self):
        with open("sources.yaml", "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)

        feeds = config["feeds"]
        return feeds


if __name__ == '__main__':
    rssto = RssTester()

