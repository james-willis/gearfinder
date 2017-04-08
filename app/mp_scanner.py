from lxml import html

import requests

_FREE_AND_FOR_SALE_URL = 'https://www.mountainproject.com/forum/103989416/for-sale-for-free-want-to-buy'
_MOUNTAIN_PROJECT_URL = 'http://www.mountainproject.com'
_NEW_POST_TEXT = 'moments ago'
_POSTS_PER_PAGE = 40
_MAX_PG_NUM = 54

class Post(object):
    """
    A class to represent a Mountain Project forum post, with the information
    and methods needed to determine if it is a match and if it is a new post
    """
    def __init__(self, title='', link='', age="", replies=0):
        self.title = title
        self.link = link
        self.age = age
        self.replies = int(replies)

    def is_match(self, parameters):
        """
        Determines if a post title contains one of the search parameters, and
        is not a buyer thread
        :param parameters: a list of strings containing the search parameters
        :return: a bool indicating if the post is a match

        >>> post = Post("abcd", "google.com", "4 hours ago", 4)
        >>> post.is_match(["c"])
        True
        >>> post.is_match(["e"])
        False
        """
        title = str(self.title).lower()

        # 'wtb' and 'iso' indicate prospective buyers, not what we want
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
        """
        Determines if a post contains one of the search parameters and is new
        (< 5 minutes of age, 0 replies), and is not a buyer thread.
        :param parameters: a list of strs containing the search parameters
        :return: a bool indicating if the post is a match
        
        >>> post = Post("abcd", "google.com", "4 mins ago", 0)
        >>>post.is_match(["c"])
        True
        >>> post.is_match(["e"])
        False
        >>> post.replies = 2
        >>> post.is_new_match(["c"])
        False

        """
        recent_reply = (self.age == _NEW_POST_TEXT or (self.age[0].isdigit() \
                        and int(self.age[0]) <= 5 \
                        and self.age[2:6] == "mins"))

        return self.is_match(parameters) and recent_reply and self.replies == 0


def get_forum_page(pg_num):
    """
    This function returns the  the Mountain Project html of a given page of
    post listings from the Free and For Sale forum
    :param pg_num: what page number of results is being requested
    :return: an html object of the requested page of posts from Mountain
        Project's Free and for Sale forum
    """
    url = _FREE_AND_FOR_SALE_URL + '?page=' + str(pg_num)
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
    post_root = "//table/tr"
    titles = tree.xpath(post_root + "/td[1]/div[1]/a/strong/text()")
    links = tree.xpath(post_root + "/td[1]/div[1]/a/attribute::href")
    ages = [x.strip() for x in tree.xpath(post_root + "/td[3]/a/text()")]
    num_replies = [int(n.strip()) for n in tree.xpath(post_root + "/td[2]/text()")]

    i = 0
    while i < len(titles):
        post = Post(titles[i], links[i], ages[i], num_replies[i])

        if 'n' not in flags and post.is_match(parameters):
            posts.append(post)
        elif post.is_new_match(parameters):
            posts.append(post)
        i += 1
    return posts


def get_all_matching_posts(parameters):
    """
    searches through all pages of Mountain Project's For Sale Forum and returns
    a list of all posts
    """
    posts = []

    # there are 40 pages of results
    for i in range(1, _MAX_PG_NUM + 1):
        posts += get_matching_posts(parameters, get_forum_page(i))
    return posts
