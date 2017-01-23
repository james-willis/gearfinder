from lxml import html
import requests
import sys

_FREE_AND_FOR_SALE_URL = 'http://www.mountainproject.com' \
                         '/v/for-sale--for-free--want-to-buy/103989416'
_MOUNTAIN_PROJECT_URL = 'http://www.mountainproject.com'
_POSTS_PER_PAGE = 25


class Post:
    def __init__(self, title='', link='', age="5 minutes ago"):
        self.title = title
        self.link = link
        self.age = age

    def is_match(self, parameters):
        """
        Determines if a post contains one of the search parameters and is new (< 5
        minutes of age), and is not a buyer thread
        :param parameters: a list of strs containing the search parameters
        :return: a bool indicating if the post is a match
        """
        title = str(self.title).lower()

        # 'wtb' and 'iso' indicate prospective buyers; not what we want
        if 'wtb' in title \
                or 'iso ' in title \
                or 'iso: ' in title \
                or 'sold ' in title:
                # or self.age != 'moments ago': #comment out to show all posts that match
            return False
        for param in parameters:
            param = param.lower()
            if param in title:
                return True
        return False


def main():
    search_terms = sys.argv[1:]
    matches = get_matching_posts(search_terms)
    write_links(matches)


def get_matching_posts(parameters):
    """
    This function scans The Mountain Project's For Sale forum for new posts
    that meet any of the search parameters

    :param url: the URL of the forum
    :param parameters: a list of strs representing each search parameter
    :return: a list of Posts that match at least one search parameter
    """
    url = _FREE_AND_FOR_SALE_URL
    page = requests.get(url)
    tree = html.fromstring(page.content)
    posts = []

    for i in range(1, _POSTS_PER_PAGE):  # Xpath uses 1 indexed arrays
        post = Post()

        post_root = '(//tr[@bgcolor=\'#ffffff\' or @bgcolor=\'#f2f2f2\'])[{}]'.format(i)
        post.title = tree.xpath(post_root + '/td[3]/b/a/text()')[0]
        post.link = _MOUNTAIN_PROJECT_URL + tree.xpath(post_root + '/td[3]/b/a/attribute::href')[0]
        post.age = tree.xpath(post_root + "/td[7]/small/text()")[0]

        if post.is_match(parameters):
            posts.append(post)

    return posts


def write_links(matches):
    root_domain = _MOUNTAIN_PROJECT_URL
    for match in matches:
        link = '<a href=\"{}{}\">{}</a>'.format(root_domain, match.link, match.title)
        print(link)


if __name__ == "__main__":
    main()
