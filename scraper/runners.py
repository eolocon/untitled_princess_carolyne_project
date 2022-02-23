from streamers import SimpleStreamer
from scrapers import SimpleScraper
from custom_types import Post, Comment, Reply
import json
import utils
import time

"""Module for runners implementations
    
Runners are meant to run a specific scraping service;
a runner implementation should have just one public method: run.

Todo:
    * add an interface class for the concrete runner classes

"""

class SimpleRunner:
    """SimpleRunner is a simple implementation of a runner.

    It uses a scraper (from the module scrapers.py) for data scraping
    and a streamer (from the module streamers.py ) for streaming data to an external client.

    """

    def __init__(self, host, port):
        """
            Args:
                host (str): streamer's destination host address
                port (str): streamer's destination host port

            Attributes:
                _scraper (obj): a scraper
                _streamer (obj): a streamer
                _SLEEPING_TIME (int): parameter to regulate the scraping rate

            Todo:
                * the attributes values are hard coded; refactor to modify this
        """

        self._scraper = SimpleScraper()
        self._streamer = SimpleStreamer(host, port)
        self._SLEEPING_TIME = 2

    def run(self, targets, cookies):
        """Runs the scraping service

        This method iteratively scrapes data using _scraper, and consumes them using _streamer

        """
        targets = utils.parse_list(targets)
        
        self._streamer.create_connection()

        self._scraper.set_cookies(cookies)

        for target in targets:
            self._scraper.set_target(target)
            self._scraper.scrape()

            post = Post(**self._scraper.post)
            comments = self._scraper.post["comments_full"]
        
            self._consume(post)

            for comment in comments:

                # replies = comment["replies"]
                comment = Comment(**comment)
                comment.parent_document_id = post.document_id
                
                self._consume(comment)

                # for reply in replies:

                #     reply = Reply(**reply)
                #     reply.parent_document_id = comment.document_id
                    
                #     self._consume(reply)
    
    def _consume(self, to_consume):
        """ This method just use _streamer to send data to the streamer's destination """
        
        self._streamer.send(to_consume)
        # print("")
        # print(to_consume)
        # print("")
        time.sleep(self._SLEEPING_TIME)
        
        
       