from flask import Flask, render_template, request

from controllers import get_movies, get_reviews
from models import db, ma, MoviesSchema, ReviewsSchema

app = Flask(__name__)

# Get Config File
app.config.from_object("config")
# Register DB
db.init_app(app)
ma.init_app(app)

movies_schema = MoviesSchema(many=True)
reviews_schema = ReviewsSchema(many=True)


@app.route('/')
def hello_world():
    movies = get_movies(movies_schema)
    return render_template("index.html", movies=movies)


@app.route('/review/<movie_id>', methods=["POST", "GET"])
def review(movie_id):
    movie = get_reviews(movie_id)
    if request.method == 'POST':
        names = request.form.get('name')
        email = request.form.get('review')

    return render_template("review.html", movie=movie)


if __name__ == '__main__':
    app.run()
