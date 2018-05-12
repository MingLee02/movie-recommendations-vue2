from imdb import IMDb


def recommend_film(items=None):
    ia = IMDb()
    recommend_list = []
    for item in items:
        movies = ia.search_movie(item)
        for movie in movies:
            if movie.data['title'].upper() == item.upper() and movie.data['kind'] == 'movie':
                foo = ia.get_movie(movie.movieID)
                if foo['rating'] >= 8:
                    recommend_list.append({
                        'title': foo['title'],
                        'rating': foo['rating'],
                        'genres': foo['genres'],
                        'languages': foo['languages'],
                        'plot_outline': foo['plot outline']
                    })
                break
    return recommend_list


def main():
    recommend_film()


if __name__ == '__main__':
    main()
