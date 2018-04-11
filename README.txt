AUTHOR: Paweł P. Woźniak

OBJECTIVE:

Implement a program that monitors web sites and reports their availability and 
problems on their sites. The program:

- Reads a list of web pages (HTTP URLs) and corresponding page content requirements
from a configuration file.
- Periodically makes an HTTP request to each page (possibility to tune the interval
via a setting in the configuration file).
- Verifies that the page content received from the server matches the content
requirements.
- Measures the latency (time it took for the web server to complete the whole
request).
- Writes a log file that shows the progress of the periodic checks distinguishing
between connection level problems (e.g. the web site is down, content problems or
content requirements were not fulfilled).
- Implements a single-page HTTP server interface in the same process that shows
(HTML) each monitored web site and the last checked status.

*******************************************************************************

REQUIREMENTS:

This programme was written in Python 2.7 (Linux Ubuntu). To run both
versions (command line programme and single-page HTTP server) please
install in the following order:
a) Python 2.7
b) pip
c) Requirements that are in a file 'requirements.txt'. You can install them
   using pip by typing:

    'pip install -r requirements.txt'

*******************************************************************************

CONFIGURATION FILE:

Default configuration file is in 'verifier/config.ini'. It has three
changeable parameters:

WEBSITES - path to the XML file with websites and their content to verify
PERIOD - period in seconds between verifications
LOG - path to the log file with programme's results

*******************************************************************************

XML FILE:

The data about websites and their content to verify is in 'verifier/websites.xml'.
Each website must have three information given:

<url> - website's HTTP URL
<id> - id of a <div> in which content under verification should occur
<content> - content to verify

*******************************************************************************

HOW TO RUN (COMMAND LINE PROGRAMME):

To run the programme as a command line type a command below. This will
use a 'config.ini' configuration file that is in the same directory as
'verifier.py' file.

    python verifier/verifier.py

You can also specify the path to your configuration file by giving it as
a first argument:

    python verifier/verifier.py path_to_configuration_file

*******************************************************************************

HOW TO RUN (SINGLE-PAGE HTTP SERVER):

To run the programme as a single-page HTTP server run BASH script as written 
below. This will use a configuration file to which path is given at the bottom 
of 'verifier/settings.py' file (CONFIG_DIR variable). If CONFIG_DIR contains
only a name of a configuration file, then a configuration file will be 
searched in the same directory as 'settings.py' file.

    ./runHTTPserver.sh

Single-page HTTP server should be then available by the address:

    http://127.0.0.1:8000/

Periodic website verification will be available after clicking the 
'START AUTOMATIC CHECK' button.

*******************************************************************************

DESCRIPTION HOW IT WORKS:

The command line programme ('verifier/verifier.py') performs the following tasks:
1) Load data from configuration file.
2) Load content to verify for each website from XML file.
3) Run deamon thread for each website separately every period time.
4) Verify content of website's <div> with chosen id, website's status code, 
   and website's reponse time using BeautifulSoup.
5) Write result of a verification to the log file in each thread asynchronously.

A start of the HTTP server ('runserver' command) inititates the following tasks:
1) Run a deamon thread that runs the command line programme (by class inheritance
   in 'verifier/views.py').
2) Data about every website is saved in the SQlite database.
3) The difference in the command line programme run by the HTTP server is
   that the result of the last verification is saved in the database.
4) After clicking 'START AUTOMATIC CHECK' button on the HTTP page, the
   information about the results of verification is updated every period
   time using AngularJS and 'setInterval' JavaScript function. The updated
   result is saved in the SQlite database as the last one.