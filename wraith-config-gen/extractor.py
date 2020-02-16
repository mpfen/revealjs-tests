#!/usr/bin/python3
# Copyright (C) 2019 Michael Pfennings
# SPDX-License-Identifier: GPL-3.0-or-later

import argparse
import os
import shutil
from ruamel.yaml import YAML
from slugify import slugify
from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

from webdrivermanager import ChromeDriverManager


def main(target_url, file, headless):
    target_url = sanitize_url(target_url)

    browser_options = Options()
    # Chrome wird headless und mit gemutetem Sound ausgeführt
    if not headless:
        browser_options.add_argument("--headless")
        browser_options.add_argument("--mute-audio")

    # installiert chromedriver in python venv
    cdd = ChromeDriverManager()
    cdd.download_and_install()
    driver = webdriver.Chrome(options=browser_options)

    # sendet bei jedem actions.perform() die Taste 'n'
    # n ist der shortcut für nächste Seite in Reveal.js
    actions = ActionChains(driver)
    actions.send_keys('n')

    # Präsentation aufrufen und Titel auslesen
    driver.get(target_url)
    sleep(2)
    title = driver.title
    print(title)

    urls = []
    urls.append(driver.current_url)
    # bricht ab wenn sich die URL nicht mehr ändert
    while True:
        actions.perform()
        sleep(1)

        if driver.current_url != urls[-1]:
            urls.append(driver.current_url)
            # zum testen;
            if driver.current_url == 'http://localhost:8080/howto.html#/slide-usage':
                break
        else:
            break
    driver.close()
    print('urls extracted')

    if file:
        save_to_file(target_url, urls, title)
    else:
        create_wraith_files(title, target_url, urls)


# Speichert gesammelte URLS in Datei
def save_to_file(target_url, urls, title):
    path = slugify(title) + '.txt'
    text = ''

    print('saving to file: ' + path )
    with open(path, 'w') as file:
        text = '\n'.join(urls)
        file.write(text)


# Erzeugt Ordnerstruktur und history.yaml aus den gesammelten Urls
def create_wraith_files(title, target_url, urls):
    yaml = YAML()
    config_path = slugify(title)
    paths = ''

    # yaml für pages im Format:
    # page#: Fragmentbezeicher
    print('creating config in folder: ' + config_path + '/')
    for i in range(len(urls)):
        wraith_url = urls[i].replace(target_url, '')
        paths += '  page' + str(i) + ': "' + wraith_url + '"\n'

    # Kopiert Templatedateien
    if not os.path.exists(config_path):
        os.makedirs(config_path)
        shutil.copytree('./templates/configs', config_path + '/configs')
        shutil.copytree('./templates/javascript', config_path + '/javascript')


    # history.yaml einlesen
    yaml_path = config_path + '/configs/history.yaml'
    with open(yaml_path, 'r') as file:
        history_content = yaml.load(file)

    # Domain und Pages hinzufügen
    domain = 'page1: "' + target_url + '"'
    history_content['domains'] = yaml.load(domain)
    history_content['paths'] = yaml.load(paths)

    # geänderte history.yaml speichern
    with open(yaml_path, 'w') as file:
        yaml.dump(history_content, file)


# Um die Konfigurationsdatei zu erstellen brauchen wir eine
# URL ohne Fragmentbezeicher
def sanitize_url(url):
    url = url.split('#')[0]
    return(url)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('url', help='url of the revealjs presentation', type=str)
    parser.add_argument('-f', '--file', help='save urls to file', action='store_true')
    parser.add_argument('-v', '--verbose', help='toogle off headless mode',
                        action='store_true')
    args = parser.parse_args()
    main(args.url, args.file, args.verbose)
