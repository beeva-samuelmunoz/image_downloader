# -*- coding: utf-8 -*-


import json
import time

from selenium import webdriver

from .img_downloader import ImgDownloader
from . import utils



class Google(ImgDownloader):

    URL = 'https://www.google.com/search?q="{}"&source=lnms&tbm=isch'

    def _get_links(self, query):
        driver = webdriver.Firefox(executable_path=self.PATH_DRIVER)
        driver.get(self.URL.format(query))
        # Load the complete page
        def exhaust_autoscroll(driver, n_times, wait_seconds):
            for _ in range(n_times):
                # Go to the end of the page (auto-load)
                driver.execute_script("window.scrollBy(0, 1000000)")
                time.sleep(wait_seconds)
        try:
            exhaust_autoscroll(driver, 5, 1)
            driver.find_element_by_id("smb").click()  # Load more images!
            exhaust_autoscroll(driver, 5, 1)
        except Exception as e:
            print ("Exception when loading: {}".format(e))
        urls_imgs = []
        for meta_img in [
            json.loads(x.get_attribute('innerHTML'))
            for x in
            driver.find_elements_by_xpath('//div[contains(@class,"rg_meta")]')
        ]:
            urls_imgs.append({
                'url': meta_img['ou'],
                'type': meta_img['ity']
            })
        driver.quit()
        return urls_imgs


if __name__ == "__main__":
    args = utils.get_args()
    if not args.path:
        import os
        args.path = os.path.join("data","{}-google".format(args.query))

    dl = Google()
    dl.download_imgs(
        query=args.query,
        path_data=args.path
    )
