import urlparse
import scraperwiki
import lxml.html

USER_AGENT = "https://morph.io/mgax/cdep-committees"

CHAMBERS = {
    1: 'senate',
    2: 'cdep',
    0: 'common',
}


def scrape_page(leg, cam):
    url = ('http://www.cdep.ro/pls/parlam/structura2015.co?'
           'leg={}&cam={}'.format(leg, cam))
    html = scraperwiki.scrape(url, user_agent=USER_AGENT).decode('ISO-8859-2')
    root = lxml.html.fromstring(html)

    for a_node in root.cssselect('.grupuri-parlamentare-list a'):
        href = a_node.attrib['href']
        if href.startswith('/pls/parlam/structura2015.co?'):
            qs = urlparse.parse_qs(urlparse.urlparse(href).query)
            data = {
                'cam': cam,
                'cam_code': CHAMBERS[cam],
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

    for leg in [2016, 2012, 2008, 2004, 2000, 1996, 1992, 1990]:
        for cam in [2, 1, 0]:
            scrape_page(leg, cam)


if __name__ == '__main__':
    main()
