from lxml import html
import requests

_FREE_AND_FOR_SALE_URL = 'http://www.mountainproject.com' \
                         '/v/for-sale--for-free--want-to-buy/103989416'
_MOUNTAIN_PROJECT_URL = 'http://www.mountainproject.com'
_NEW_POST_TEXT = 'moments ago'
_POSTS_PER_PAGE = 25


class Post:
    def __init__(self, title='', link='', age=""):
        self.title = title
        self.link = link
        self.age = age

    def is_match(self, parameters):
        """
        Determines if a post title contains one of the search parameters, and is not a buyer thread
        :param parameters: a list of strings containing the search parameters
        :return: a bool indicating if the post is a match
        """
        title = str(self.title).lower()

        # 'wtb' and 'iso' indicate prospective buyers; not what we want
        if 'wtb' in title \
                or 'iso ' in title \
                or 'iso: ' in title \
                or 'sold ' in title:
            return False
        for param in parameters:
            param = param.lower()
            if param in title:
                return True
        return False

    def is_new_match(self, parameters):
        # TODO fix this, returns any post recently replied to
        """
        Determines if a post contains one of the search parameters and is new (< 5
        minutes of age), and is not a buyer thread
        :param parameters: a list of strs containing the search parameters
        :return: a bool indicating if the post is a match
                """
        return self.is_match(parameters) and self.age == _NEW_POST_TEXT


def get_forum_page(pg_num):
    """
    This function returns the  the Mountain Project html of a given page of post listings from the Free and For Sale
    forum
    :param pg_num: what page number of results is being requested
    :return: an html object of the requested page of posts from Mountain Project's Free and for Sale forum
    """

    url = _FREE_AND_FOR_SALE_URL + '__' + str(pg_num)
    page = requests.get(url)
    return html.fromstring(page.content)


def get_matching_posts(parameters, tree, flags=''):
    """
    This function scans The Mountain Project's For Sale forum for new posts
    whose title contains any of the search parameters.
    Flags:
    n - new posts only

    :param parameters: a list of strings representing each search parameter
    :param tree: An html tree of a page of Mountain Project for sale posts
    :param flags: flags for toggling settings on what posts to find
    :return: a list of Posts that match at least one search parameter
    """
    posts = []

    for i in range(1, _POSTS_PER_PAGE):  # Xpath uses 1 indexed arrays
        post = Post()

        post_root = '(//tr[@bgcolor=\'#ffffff\' or @bgcolor=\'#f2f2f2\'])[{}]'.format(i)
        post.title = tree.xpath(post_root + '/td[3]/b/a/text()')[0]
        post.link = _MOUNTAIN_PROJECT_URL + tree.xpath(post_root + '/td[3]/b/a/attribute::href')[0]
        post.age = tree.xpath(post_root + "/td[7]/small/text()")[0]

        if 'n' not in flags and post.is_match(parameters):
            posts.append(post)
        elif post.is_new_match(parameters):
            posts.append(post)

    return posts


def write_links(matches):
    """
    This takes in a list of Posts and prints them
    :param matches: An iterable of Posts
    :return: None
    """
    root_domain = _MOUNTAIN_PROJECT_URL
    for match in matches:
        link = '<a href=\"{}\">{}</a>'.format(match.link, match.title)
        yield link
