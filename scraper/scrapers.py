from facebook_scraper import get_posts

"""Module for scrapers implementations
    
Scrapers are meant to scrape some kind of data;

Todo:
    * add an interface class for the concrete scraper classes

"""

class SimpleScraper:
    """ Simple implementation of a scraper.

    It uses the facebook_scraper library to scrape from facebook.
    target post ID and cookies from the facebook session are required for the class to work properly

    """

    def __init__(self):
        """
            Args:
                _target (str): ID of the target post
                _cookies (str): path to the json file containing the cookies
                post (dict): dictionary containing the scraping results

        """

        self._target = None
        self._cookies = None
        self.post = None

    def set_target(self, target):
        self._target = target
        return self

    def set_cookies(self, cookies):
        self._cookies = cookies
        return self

    def scrape(self):
        """Performs the actual scraping.

            Todo:
                * refactor so the options are not hard coded, but configurable

        """

        self.post = next(
            get_posts(
                post_urls=[self._target],
                cookies=self._cookies,
                options={
                    "reactions": True,
                    "comments": "generator",
                    "comment_reactions": False,
                    "comment_reactors": False
                    }
                )
            )