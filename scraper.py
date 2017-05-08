import urlparse
import scraperwiki
import lxml.html

USER_AGENT = "https://morph.io/mgax/cdep-committees"


def scrape_page(leg, cam):
    url = ('http://www.cdep.ro/pls/parlam/structura2015.co?'
           'leg={}&cam={}'.format(leg, cam))
    html = scraperwiki.scrape(url, user_agent=USER_AGENT).decode('ISO-8859-2')
    root = lxml.html.fromstring(html)

    for a_node in root.cssselect('.grupuri-parlamentare-list a'):
        qs = urlparse.parse_qs(urlparse.urlparse(a_node.attrib['href']).query)
        data = {
            'cam': cam,
            'leg': leg,
            'idc': int(qs['idc'][0]),
            'name': a_node.text_content(),
        }

        scraperwiki.sqlite.save(unique_keys=['cam', 'leg', 'idc'], data=data)


def dump():
    for record in scraperwiki.sql.select("* from data"):
        print(', '.join(u"{}: {}".format(k, v) for k, v in record.items()))


def main():
    import sys
    if sys.argv[1:] == ['dump']:
        dump()
        return

    scrape_page(2016, 2)


if __name__ == '__main__':
    main()
