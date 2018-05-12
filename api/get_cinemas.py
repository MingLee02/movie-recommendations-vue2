from pprint import pprint

from recommend_films import recommend_film
from cinema_listings import get_cinema_listings 

import googlemaps

from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route("/api/address/<string:postcode>/")
def get_origin(postcode):
    address = googlemaps.Client(key='AIzaSyCwDPJFF4y3udU12hdYEUx04Rss0dRN-bk')
    postcode = postcode.replace(' ', '')

    args = {
        'address': postcode
    }
    result = address.geocode(args)
    
    return jsonify(result[0])


@app.route("/api/cinema-list/<string:address>/")
def get_cinemas_list_with_distances(address):
    split_address = address.split(':')

    origin = {
        "lat": split_address[0],
        "lng": split_address[1]
    }

    cinemas = get_cinemas(origin)
    cinemas = get_distances(origin, cinemas)
    cinemas = sorted(cinemas, key=lambda d: d['distance']['value'])

    return jsonify(cinemas[:6])


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
                    'place-id': cinema['place_id'],
                    'latlng': cinema['geometry']['location'],
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


if __name__ == '__main__':
    app.run(debug=True)
