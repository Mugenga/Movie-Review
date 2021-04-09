from models import Movies, MoviesSchema, Reviews, ReviewsSchema


def get_movies(movies_schema: MoviesSchema):
    movies = Movies.query.all()
    result = movies_schema.dump(movies)
    return result


def get_reviews(movie_id):
    return Movies.query.order_by("reviews.id desc").get(movie_id)

#
# def get_featured_services(services: ServicesSchema):
#     all_products = Services.query.filter(Services.featured == 1).limit(5).all()
#     result = services.dump(all_products)
#     return result


# def get_properties(services: ServicesSchema, page, per_page, cat_id):
#     filter_data = {'category_id': cat_id}
#     filter_data = {key: value for (key, value) in filter_data.items()
#                    if value}
#     all_products = Services.query.filter_by(**filter_data).paginate(
#         page, per_page, False)
#     result = services.dump(all_products.items)
#     return result
#
#
# def get_service(user_id):

