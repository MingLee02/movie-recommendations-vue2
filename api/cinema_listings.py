from selenium import webdriver
from imdb import IMDb
from bs4 import BeautifulSoup
import platform


def odeon_films(driver):
    movies_list = []
    movies = driver.find_elements_by_xpath("//div[@class='content-container film _DAY1']")
    items_list = []
    for movie in movies:
        foos = movie.find_elements_by_xpath("//div[@class='grad-hor']")
        for foo in foos:
            bars = foo.find_elements_by_xpath("//div[@class='presentation-info']")
            for bar in bars:
                if bar not in items_list:
                    items_list.append(bar)

    for item in items_list:
        html = item.get_attribute('outerHTML')
        soup = BeautifulSoup(html, "lxml")
        p_tags = soup.findAll('a',text=True)
        for i, p_tag in enumerate(p_tags): 
            movies_list.append(p_tag.text)

    return movies_list


def get_cinema_listings(website=None, name=None):
    movies_list = []
    movies = None
    driver = None
    print('Attempting to collect todays movie listings from {}'.format(website))

    if platform.system() == 'Windows':
        driver = webdriver.PhantomJS("phantomjs/bin/phantomjs.exe")

    if platform.system() == 'Linux':
        driver = webdriver.PhantomJS("phantomjs-linux-64/bin/phantomjs")
    driver.get(website)
 
    if 'Vue' in name or 'Vue' is name:
        print('IN')
        movies = driver.find_elements_by_xpath("//span[@rv-text='item.title']")   
    if 'Cineworld' in name or 'Cineworld' is name:
        movies = driver.find_elements_by_xpath("//h4[@class='qb-movie-name']")
    if 'Odeon' in name  or 'Odeon' is name:
        movies_list = odeon_films(driver)

    if 'Odeon' not in name and 'Odeon' is not name:
        for movie in movies:
            movies_list.append(movie.text)

    return movies_list


def main():
    get_cinema_listings()


if __name__ == '__main__':
    main()
