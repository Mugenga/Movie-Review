from flask import Flask
from marshmallow import Schema, fields, pre_load, validate, ValidationError
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

ma = Marshmallow()
db = SQLAlchemy()


class Movies(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True)
    movie_name = db.Column(db.String(150), nullable=False)
    image_url = db.Column(db.String(150), unique=True, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    Reviews = db.relationship('Reviews', backref=db.backref('movies', lazy=True))


class Reviews(db.Model):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True)
    reviewer_name = db.Column(db.String(150), nullable=False)
    review = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'), nullable=True)

    def __init__(self, reviewer_name, review, rating, movie_id):
        self.reviewer_name = reviewer_name
        self.review = review
        self.rating = rating
        self.movie_id = movie_id


class MoviesSchema(ma.Schema):
    class Meta:
        fields = ('id', 'movie_name', 'image_url', 'rating')


class ReviewsSchema(ma.Schema):
    class Meta:
        fields = ('id', 'reviewer_name', 'review', 'rating', 'movie_id')
