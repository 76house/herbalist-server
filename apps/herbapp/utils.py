# coding: utf-8

import os
import string
import ntpath
import glob
import urllib
from lxml import html
from django.conf import settings


# ------------------------------------------------------------------------------

# get common page from wikipedia
def fetch_from_wikipedia(url, translated_names, supported_languages):

    page = html.fromstring(urllib.urlopen(url).read().decode('utf-8'))
    texts = page.xpath("//text")

    if len(texts) > 0:
        text = texts[0].text

        # get family
        if translated_names['family'] == "":
            start = text.find("include=")
            if start > 0:
                stop = text.find(" (APG)", start)
                if stop > start:
                    translated_names['family'] = text[start + 8 : stop]
            else:
                start = text.find("Familia:")
                if start > 0:
                    start = text.find("[[:Category:", start)
                    if start > 0:
                        stop = text.find("|", start)
                        if stop > start:
                            translated_names['family'] = text[start + 12 : stop]
          
      
        # get herb name translations
        for language in supported_languages:
            if (language not in translated_names) or (len(translated_names[language]) < 2):
                start = text.find("[[%s:" % language)
                if start > 0:
                    stop = text.find("]]", start)
                    if stop > start:
                        translated_names[language] = text[start + 5 : stop]

    else:
        print "Page", url, "contains no usable data"


# ------------------------------------------------------------------------------

region_data_cache = {}

# get herb distribution info from region data
def fetch_from_region_data(botanical_names, region_data):

    if not any(region_data_cache):
        # initialize the cache
        static_root = settings.STATIC_ROOT
        if not settings.PRODUCTION:
            # devel environment: use local static dir
            for p in settings.STATICFILES_DIRS:
                if p[0] == "herbapp":
                    static_root = p[1]
                    break

        print "Initializing region data cache..."
        file_pattern = os.path.join(static_root, 'regions', 'region_*.txt')
        print "File pattern:", file_pattern
        for name in glob.glob(file_pattern):
            with open(name, 'rt') as f:
                herbnames = f.read().splitlines()
                key = ntpath.basename(name).replace("region_", "").replace(".txt", "")
                region_data_cache[key] = herbnames

    # search in region data cache
    if any(region_data_cache):
        for bn in botanical_names:
            herbname = bn.lower().strip()
            for key, herbnames in region_data_cache.items():
                if herbname in herbnames:
                    (region, index) = key.split("_")
                    if index not in region_data[region]:
                        region_data[region].append(index)
    else:
        print "Region data cache contains no usable data"


