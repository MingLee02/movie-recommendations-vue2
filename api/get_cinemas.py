from pprint import pprint

from recommend_films import recommend_film
from cinema_listings import get_cinema_listings 

import googlemaps


def get_origin(postcode):
    address = googlemaps.Client(key='AIzaSyCwDPJFF4y3udU12hdYEUx04Rss0dRN-bk')
    args = {
        'address': postcode
    }
    result = address.geocode(args)

    return result[0]['geometry']['location']


def get_cinemas(address):
    places = googlemaps.Client(key='AIzaSyCzNPxnqW4DqBuQY3d9cz0VzJNYTtW7bXQ')
    cinema_list = []
    num = 0

    result = places.places(
        location=address,
        query='Cinema',
        radius=10,
        type='movie_theater'
    )
    cinemas = result['results']

    for cinema in cinemas:
        if any(c in cinema['name'] for c in ['Cineworld', 'Vue', 'Odeon']):
            cinema_list.append(
                {
                    'cinema-id': num,
                    'name': cinema['name'],
                    'rating': cinema['rating'],
                    'address': cinema['formatted_address'],
                    'place-id': cinema['place_id']
                }
            )
            num += 1
    return cinema_list


def get_cinema_site(cinemaID):
    places = googlemaps.Client(key='AIzaSyCzNPxnqW4DqBuQY3d9cz0VzJNYTtW7bXQ')

    result = places.place(
        place_id=cinemaID,
    )
    return result['result']['website']

def get_distances(origin, cinemas):
    distance = googlemaps.Client(key='AIzaSyBP5NFMUwDztx4CHhIEKSv-U0W2y-6mpRM ')
    destination_list = []
    for cinema in cinemas:
        destination_list.append(cinema['address'])

    result = distance.distance_matrix(
        origins=origin,
        destinations=destination_list
    )

    item_num = 0
    for cinema in cinemas:
        cinema['distance'] = result['rows'][0]['elements'][item_num]['distance']
        item_num += 1
    
    return cinemas


def main():
    postcode = None
    selected_cinema = None
    cinema_id = None

    while not postcode:
        postcode = input('please input postcode or q to quit: ')

    if postcode == 'q':
        print('quitting App')
        return

    origin = get_origin(postcode)

    if origin:
        cinemas = get_cinemas(origin)
        cinemas = get_distances(origin, cinemas)
        cinemas = sorted(cinemas, key=lambda d: d['distance']['value'])

        for cinema in cinemas:
            print(cinema)

        while not selected_cinema:
            selected_cinema = input('please select cinema by inputting cinema id: ')

        for cinema in cinemas:
            if cinema['cinema-id'] == int(selected_cinema):
                chosen_cinema = cinema

        print('you chose {}: at {}'.format(chosen_cinema['name'], chosen_cinema['address']))
        web_address = get_cinema_site(chosen_cinema['place-id'])

        movies = get_cinema_listings(web_address, chosen_cinema['name'])

        if len(movies) > 0:
            recommended_movies = recommend_film(movies)
            print('Today Imdb Recommends')

            for movie in recommended_movies:
                pprint(movie)
        else:
            print('There are no more movies playing today')

if __name__ == '__main__':
    main()
