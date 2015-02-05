import boto
import time
import restart_iis
from datetime import timedelta
from datetime import datetime
from sys import exit
from boto.sqs.connection import SQSConnection
from boto.sqs.message import RawMessage

test_queue = "your-queue-name"
last_reset = datetime.now()
minutes_between_restarts = timedelta(minutes=3)
was_run_once = False

while 1:
    sqs = boto.connect_sqs('YOUR-AWS-ACCESS-KEY-ID', 'YOUR-AWS-SECRET-KEY')
    if sqs is None:
        print "Failed to connect to sqs; exiting..."
        exit(1)
    q = sqs.get_queue(test_queue)
    q.set_message_class(RawMessage)
    messages = q.get_messages()
    if len(messages) <= 0:
        print "No messages received on queue " + test_queue + ", sleeping... " + str(datetime.now())
        time.sleep(60)
    else:
        print "Deleting messages... " + str(datetime.now())
        for message in messages:
            q.delete_message(message)
        now = datetime.now()

        print "Checking whether to reset IIS... " + str(datetime.now())
        if was_run_once == False or now - last_reset > minutes_between_restarts:
            print "OK! Going to reset IIS... " + str(datetime.now())
            was_run_once = True
            print "Stopping IISAdmin... " + str(datetime.now())
            restart_iis.service_action('stop_with_deps', 'IISAdmin')
            time.sleep(10)
            print "Starting SMTP... " + str(datetime.now())
            restart_iis.service_action('start', 'Simple Mail Transfer Protocol (SMTP)')
            print "Starting W3C... " + str(datetime.now())
            restart_iis.service_action('start', 'World Wide Web Publishing Service')
            #restart_iis.service_action('start', 'HTTP SSL')
            time.sleep(10)
            last_reset = datetime.now()
            print "DONE resetting IIS... " + str(datetime.now())
        else:
            print "Skipping IIS reset...maybe too soon between resets?"




            # restart_iis.service_action('stop_with_deps', 'Simple Mail Transfer Protocol (SMTP)')
            # restart_iis.service_action('stop', 'World Wide Web Publishing Service')
            # restart_iis.service_action('stop', 'HTTP SSL')
