from django.conf import settings
from verifier import Verifier
from threading import Thread
from models import Website
import logging
from django.shortcuts import render


class VerifierWebsite(Verifier):
    """
    Class reads configuration file, loads data about websites,
    verify a content of websites, and write data about the last verification
    in a database for HTML to present.
    """
    def verify_and_log(self, site_data):
        """
        Verify content of one website, write the result in a log file,
        and write data about the last verification in a database for HTML
        to present.

        @param site_data: data for one website from configuration file
        @type site_data: dictionary
        """
        # Verify content of one website:
        report = self.verify_website(site_data)
        # Write the result in a log file:
        logging.info(' '.join([site_data['url'], str(report['code']),
                     str(report['time']), report['result']]))
        # Write data about the last verification in a database:
        website = Website.objects.get(pk=site_data['pk'])
        website.time = str(report['time'])
        website.code = report['code']
        website.result = report['result']
        website.save()

    def start_web_verifier(self):
        """
        Start the whole verifier for HTML presentation.
        """
        # Load data from configuration file:
        config_data = self.load_config()
        # Loads a list of websites to verify from configuration file:
        website_list = self.load_website_list(config_data['website_list'])
        # Delete all website objects in a database if exist. New verification
        # is starting:
        Website.objects.all().delete()
        # Create a database object for each website:
        for wl in website_list:
            website = Website.objects.create(url=wl['url'],
                                             id_tag=wl['id'],
                                             content=wl['content'])
            # Add information about website's database pk into a dictionary
            # with its data:
            wl['pk'] = website.id
        if(config_data):
            # Starting thread that will start smaller threads for each website:
            print "Starting verifying deamon."
            th = Thread(target=self.run_verification, args=(website_list,
                        config_data['period'], config_data['log_file'],))
            th.setDaemon(True)
            th.start()
        else:
            print "Verifying deamon not started"


def home(request):
    """
    Open main HTML passing the time (in seconds) of verification period.
    """
    return render(request, 'home.html', {'period': settings.CONFIG_PERIOD})
