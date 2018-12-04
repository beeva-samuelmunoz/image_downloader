# -*- coding: utf-8 -*-
"""Abstract class to image downloader.

Inspiration taken from:
https://stackoverflow.com/questions/35809554/how-to-download-google-image-search-results-in-python
"""


import os
import urllib.request



class ImgDownloader():

    HEADERS = {
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"
    }
    EXTENSIONS = {"jpg", "jpeg", "png", "gif"}
    URL = None  # Personalize on inheritance

    def __init__(self, query_url=None, path_driver=None):
        if query_url:
            self.URL = query_url
        if path_driver:
            self.PATH_DRIVER = path_driver
        else: # In the same folder
            self.PATH_DRIVER = os.path.join(os.getcwd(), 'geckodriver')


    def download_imgs(self, query, path_data):
        """Perform an image query and download results in a folder.

        Parameters:
        query: str
            Search these images.
        path_data: str
            Where to download the images.
        """
        try:
            if not os.path.exists(path_data):
                print("Creating path {}.".format(path_data))
                os.makedirs(path_data)
            else:
                print("Warning, : path '{}' exists.".format(path_data))
            self._download_imgs(self._get_links(query), path_data)
        except Exception as e:
            print("Excepcion: {}".format(e))


    def _get_links(self, query):
        """
        """
        pass

    def _download_imgs(self, urls_imgs, path_data):
        """Download image links.

        Parameters:
        urls_imgs: [ {'url': str, 'type': str}]
            URLs of the images.
        path_data: str
            Destination folder.
        """
        img_count = 0
        downloaded_img_count = 0
        for img in urls_imgs:
            img_count += 1
            print("Downloading image {} : {}".format(img_count, img['url']))
            try:
                if img['type'] not in self.EXTENSIONS:
                    img['type'] = "jpg"
                req = urllib.request.Request(img['url'], headers=self.HEADERS)
                img['name'] = '{}_{}.{}'.format(
                    req.host,
                    os.path.basename(img['url'].split('?')[0]),
                    img['type']
                )
                raw_img = urllib.request.urlopen(req).read()
                with open(os.path.join(path_data, img['name']), "+wb") as fd:
                    fd.write(raw_img)
                downloaded_img_count += 1
            except Exception as e:
                print("Download failed: {}".format(e))
        print ("Total downloaded: {} / {}".format(downloaded_img_count, img_count))
