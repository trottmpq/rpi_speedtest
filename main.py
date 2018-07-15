#!/usr/bin/python
import json
import logging

import speedtest
import twitter

servers=[]

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# create a file handler
handler = logging.FileHandler('hello.log')
handler.setLevel(logging.INFO)

# create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(handler)

def test():
    #run speedtest-cli
    print('running test')
    logger.info('running test')
    s = speedtest.Speedtest()
    s.get_servers(servers)
    s.get_best_server()

    s.download()
    s.upload(pre_allocate=False)
    s.results.share()

    results_dict = s.results.dict()

    logger.info('Results:\n'
                '\tTime:{}\n'
                '\tDownload:{}\n'
                '\tUpload:{}\n'.format(results_dict["timestamp"], results_dict["download"], results_dict["upload"]))
    
    # with open('keys.json') as json_file:  
    #     keys = json.load(json_file)

    # twit = twitter.Twitter(auth=twitter.OAuth(keys['access_token_key'], keys['access_token_secret'], keys['consumer_key'], keys['consumer_secret']))
    if results_dict["download"] < 50:
        status="Hey @bt_uk, why was my average internet speed between 8 - 10pm {0:.2f} Mbps down and {1:.2f} Mbps up when I pay for 50 Mbps down and 1 Mbps up? @BTCare #btinfinity #speedtest".format(results_dict["download"]/1e6, results_dict["upload"]/1e6)
    else:
        status="Hey @bt_uk, my average internet speed between 8 - 10pm {0:.2f} Mbps down and {1:.2f} Mbps up. Keep up the good work! @BTCare #btinfinity #speedtest".format(results_dict["download"]/1e6, results_dict["upload"]/1e6)

    print(status)
    # twit.statuses.update(status=status)
        
if __name__ == '__main__':
        test()
        print('completed')