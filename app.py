import string

from flask import Flask, render_template, request

from controllers import get_movies, get_reviews
from models import db, ma, MoviesSchema, ReviewsSchema

import tensorflow as tf
import pandas as pd

from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer

from nltk import pos_tag, WordNetLemmatizer

from nltk.corpus import wordnet, stopwords

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
        name = request.form.get('name')
        review_txt = request.form.get('review')

        df = pd.DataFrame({"review": [review_txt]})

        # Clean Data
        content = df['review'].apply(lambda x: clean_text(x))
        print(content)

        # Import Model
        model = tf.keras.models.load_model('movie_review_model.sav')

        # Preparing the tokenizer
        tokenizer = Tokenizer(num_words=100)
        encoded_text = tokenizer.texts_to_sequences([content[0]])
        max_length = 2
        padded_text = pad_sequences(encoded_text, maxlen=max_length, padding='post')

        # Predict
        prediction = model.predict(padded_text)
        # prediction = scaler.inverse_transform(prediction)
        print(prediction)

    return render_template("review.html", movie=movie)


def get_wordnet_pos(pos_tag):
    if pos_tag.startswith('J'):
        return wordnet.ADJ
    elif pos_tag.startswith('V'):
        return wordnet.VERB
    elif pos_tag.startswith('N'):
        return wordnet.NOUN
    elif pos_tag.startswith('R'):
        return wordnet.ADV
    else:
        return wordnet.NOUN


def clean_text(text):
    # lower text
    text = text.lower()
    # tokenize text and remove puncutation
    text = [word.strip(string.punctuation) for word in text.split(" ")]
    # remove words that contain numbers
    text = [word for word in text if not any(c.isdigit() for c in word)]
    # remove stop words
    stop = stopwords.words('english')
    text = [x for x in text if x not in stop]
    # remove empty tokens
    text = [t for t in text if len(t) > 0]
    # pos tag text
    pos_tags = pos_tag(text)
    # lemmatize text
    text = [WordNetLemmatizer().lemmatize(t[0], get_wordnet_pos(t[1])) for t in pos_tags]
    # remove words with only one letter
    text = [t for t in text if len(t) > 1]
    # join all
    text = " ".join(text)
    return text


if __name__ == '__main__':
    app.run()
