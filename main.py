import json
import logging
import speedtest
import tweepy


class Logger:
    def __init__(self, name, *args, **kwargs):
        self._logger = logging.getLogger(name)
        self._logger.setLevel(kwargs.get("level", logging.INFO))
        self.add_stream_handler()

    def set_level(self, level):
        self._logger.setLevel(level)

    def add_stream_handler(self):
        self._stream_handler = logging.StreamHandler()
        self._stream_handler.setLevel(logging.INFO)
        self._stream_formatter = logging.Formatter("%(levelname)s - %(message)s")
        self._stream_handler.setFormatter(self._stream_formatter)
        self._logger.addHandler(self._stream_handler)

    def add_file_handler(self, filepath):
        self._file_handler = logging.FileHandler(filepath)
        self._file_handler.setLevel(logging.INFO)
        self._file_formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        self._file_handler.setFormatter(self._file_formatter)
        self._logger.addHandler(self._file_handler)

    def info(self, message):
        self._logger.info(message)

    def warn(self, message):
        self._logger.warning(message)

    def error(self, message):
        self._logger.error(message)


def speedtester():
    s_test = speedtest.Speedtest()
    s_test.get_servers()
    s_test.get_best_server()

    s_test.download()
    s_test.upload()

    return s_test.results


if __name__ == "__main__":
    log = Logger(__name__)
    log.add_file_handler("test.log")
    with open("keys.json", "r") as file:
        keys = json.load(file)

    auth = tweepy.OAuthHandler(keys.get("consumer_key"), keys.get("consumer_secret"))
    auth.set_access_token(keys.get("access_token"), keys.get("access_token_secret"))

    api = tweepy.API(auth)

    log.info("Running Speed Test")

    results = speedtester()
    url = results.share()

    log.info(
        "Download:{:.2f} Mbps\tUpload:{:.2f} Mbps".format(
            results.download / 1e6, results.upload / 1e6
        )
    )

    if (results.download / 1e6) < 34:
        log.error("Download speed is below the minimum Guaranteed speed")
        print(
            "Hey @bt_uk, why was my internet speed {0:.2f} Mbps down? Can I "
            "claim your stay fast guarantee of 34 Mbps for £20 please? {1} "
            "#btinfinity #speedtest".format(results.download / 1e6, url)
        )
        api.update_status(
            "Hey @bt_uk, why was my internet speed {0:.2f} Mbps down? Can I "
            "claim your stay fast guarantee of 34 Mbps for £20 please? {1} "
            "#btinfinity #speedtest".format(results.download / 1e6, url)
        )
    elif 34 <= results.download / 1e6 < 40:
        log.warning("Download speed is low but not low enough for BT to fix it")
    else:
        log.info("Download speed is good")

    log.info("Speed Test Completed")
