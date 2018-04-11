from urlparse import urlparse
from threading import Thread
import BeautifulSoup
import configparser
import requests
import logging
import time
import os
import sys


class Verifier(object):
    """
    Class reads configuration file, loads data about websites,
    and verify a content of websites.
    """
    def __init__(self, config_path="config.ini"):
        """
        @param config_path: path to the configuration file
        @type config_path: string
        """
        self.config_path = config_path
        # Configuration of logging:
        self.FORMAT = '%(message)s'
        logging.basicConfig(level=logging.INFO, format=self.FORMAT)

    def check_branch_text(self, tree_branch, tag):
        """
        Checks if particular tag of XML tree branch is a string (non-empty).

        @param tree_branch: element (branch) of the XML tree
        @type tree_branch: BeautifulSoup XML element
        @param tag: tag of the XML tree
        @type tag: string
        @return: True if tag is a (non-empty) string.
        """
        if(tree_branch.find(tag) is not None
                and tree_branch.find(tag).text is not None
                and tree_branch.find(tag).text.strip() is not ''):
            return True
        else:
            return False

    def load_website_list(self, config_path):
        """
        Loads list of websites to verify from configuration file.

        @param config_path: path to the configuration file
        @type config_path: string
        @return: List of dictionaries for each website with its data.
        """
        print "Loading website list..."
        conf_file = open(config_path)
        # Load configuration file with BeautifulSoup:
        tree = BeautifulSoup.BeautifulSoup(conf_file.read())
        config_data = []
        # Iterate over all 'website' XML elements:
        for website in tree.findAll('website'):
            # Validate if all 'website' tags are given properly:
            if(self.check_branch_text(website, 'url')
                    and urlparse(website.find('url').text.strip()).scheme
                    and self.check_branch_text(website, 'id')
                    and self.check_branch_text(website, 'content')):
                tmp_url = urlparse(website.find('url').text)
                # Append data from configuration file
                config_data.append({'url': tmp_url.geturl(),
                                    'id': website.find('id').text,
                                    'content': website.find('content').text})
        conf_file.close()
        print "Loading completed."
        return config_data

    def verify_website(self, site_data):
        """
        Verify content of one website.

        @param site_data: data for one website from configuration file
        @type site_data: dictionary
        @return: dictionary with results obtained for one website
        """
        # Send 'get' request:
        req = requests.get(site_data['url'])
        result = "'Content not found'"
        # Check if response is a success:
        if(str(req.status_code).startswith("2")):
            # Parse HTML of response with BeautifulSoup:
            soup = BeautifulSoup.BeautifulSoup(req.text)
            # Find 'div' with 'id' for website from configuration file:
            id_content = soup.find("div", {"id": site_data['id']})
            if(id_content):
                # Find 'content' in element with chosen 'id':
                content = id_content.find(text=site_data['content'])
                if(content):
                    result = "'Content OK'"
        report = {'code': req.status_code, 'time': req.elapsed,
                  'result': result}
        return report

    def verify_and_log(self, site_data):
        """
        Verify content of one website and write the result in a log file.

        @param site_data: data for one website from configuration file
        @type site_data: dictionary
        """
        # Verify content of one website:
        report = self.verify_website(site_data)
        # Write the result in a log file:
        logging.info(' '.join([site_data['url'], str(report['code']),
                     str(report['time']), report['result']]))

    def run_verification(self, website_list, config_period, log_path):
        """
        Start verification of all websites from configuration file in
        separate threads.

        @param website_list: List of dictionaries with websites' data.
        @type website_list: list of dictionaries
        @param config_period: time (in seconds) of verification period
        @type config_period: integer
        @param log_path: path to the log file
        @type log_path: string
        """
        # Open log file:
        file_handler = logging.FileHandler(log_path)
        file_handler.setFormatter(logging.Formatter(self.FORMAT))
        logging.getLogger().addHandler(file_handler)
        # Verify websites every given time until programme stops:
        while(True):
            time.sleep(config_period)
            threads = []
            # Write information about verification time:
            logging.info(time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()))
            # Run verification of each website in separate thread:
            for i, wl in enumerate(website_list):
                th = Thread(target=self.verify_and_log, args=(wl,))
                th.setDaemon(True)
                threads.append(th)
                print "Start " + str(i)
                th.start()
            # Quit each thread after it is finished:
            for i, th in enumerate(threads):
                th.join()
                print "Stop " + str(i)

    def load_config(self):
        """
        Load data from configuration file.
        @return: dictionary with data from configuration file
        """
        print "Loading configuration file..."
        config_path = self.config_path
        # If there is no configuration file in given path, then check
        # if this path is not a name of a file in the same folder:
        if(not os.path.isfile(self.config_path)):
            config_path = os.path.join(os.path.dirname(__file__),
                                       self.config_path)
            if(not os.path.isfile(config_path)):
                print "Configuration file not found"
                return
        # Parse configuration file with ConfigParser:
        config = configparser.ConfigParser()
        config.read(config_path)
        website_list = config['DEFAULT']['WEBSITES']
        # If there is no file with websites' data in given path, then check
        # if this path is not a name of a file in the same folder:
        if(not os.path.isfile(website_list)):
            website_list = os.path.join(os.path.dirname(__file__),
                                        website_list)
            if(not os.path.isfile(website_list)):
                print "File with a list of websites not found."
                return {}
        log_file = config['DEFAULT']['LOG']
        # If path of log file is not given, then set default:
        if(not log_file):
            log_file = os.path.join(os.path.dirname(__file__), "websites.log")
        # Check if time period is an integer:
        try:
            period = int(config['DEFAULT']['PERIOD'])
        except ValueError:
            print "Period is not an integer."
            return {}
        print "Loading completed."
        # Create dictionary with data from configuration file:
        config_data = {'website_list': website_list, 'period': period,
                       'log_file': log_file}
        return config_data

    def start_verifier(self):
        """
        Start the whole verifier.
        """
        # Load data from configuration file:
        config_data = self.load_config()
        # Loads a list of websites to verify from configuration file:
        website_list = self.load_website_list(config_data['website_list'])
        if(config_data):
            print "Starting verifier."
            self.run_verification(website_list, config_data['period'],
                                  config_data['log_file'])
        else:
            print "Verifier not started"


if __name__ == "__main__":
    # Start verifier with default configuration file path if not given:
    if(len(sys.argv) == 1):
        Verifier().start_verifier()
    else:
        Verifier(sys.argv[1]).start_verifier()
