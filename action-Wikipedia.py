#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from snipsTools import SnipsConfigParser
from hermes_python.hermes import Hermes
from hermes_python.ontology import *
import io
import wikipedia as wiki

CONFIG_INI = "config.ini"

# If this skill is supposed to run on the satellite,
# please get this mqtt connection info from <config.ini>
# Hint: MQTT server is always running on the master device
MQTT_IP_ADDR = "localhost"
MQTT_PORT = 1883
MQTT_ADDR = "{}:{}".format(MQTT_IP_ADDR, str(MQTT_PORT))

class Wikipedia(object):
    """Class used to wrap action code with mqtt connection
        
        Please change the name refering to your application
    """

    def __init__(self):
        # get the configuration if needed
        try:
            self.config = SnipsConfigParser.read_configuration_file(CONFIG_INI)
        except :
            self.config = None

        # start listening to MQTT
        self.start_blocking()
        
    # --> Sub callback function, one per intent
    def ask_Wiki(self, hermes, intent_message):
	wiki.set_lang("de")
        # terminate the session first if not continue
        hermes.publish_end_session(intent_message.session_id, "")
        article = intent_message.slots.article_indicator.first().value
	article = article.encode("utf-8")
	

	try:
        	summary = wiki.summary(article, sentences=2, auto_suggest=True)
        	hermes.publish_start_session_notification(intent_message.site_id, summary, "")
	except:
		hermes.publish_start_session_notification(intent_message.site_id, u'Kann Wikipediaeintrag leider nicht finden oder es bestehen mehrere Möglichkeiten.', "")

    # More callback function goes here...

    # --> Master callback function, triggered everytime an intent is recognized
    def master_intent_callback(self,hermes, intent_message):
        coming_intent = intent_message.intent.intent_name
        if coming_intent == 'Dyon:searchWikipedia':
            self.ask_Wiki(hermes, intent_message)
     

    # --> Register callback function and start MQTT
    def start_blocking(self):
        with Hermes(MQTT_ADDR) as h:
            h.subscribe_intents(self.master_intent_callback).start()
 

if __name__ == "__main__":
    Wikipedia()
