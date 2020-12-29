import tensorflow as tf
import pandas as pd
import re
import string

# Get csv file and load into pandas data frame
df = pd.read_csv('../../data/files/news.csv', header=None)
df.columns = ['date', 'title']


@tf.keras.utils.register_keras_serializable()
def custom_standardization(input_data):
    lowercase = tf.strings.lower(input_data)
    stripped_html = tf.strings.regex_replace(lowercase, '<br />', ' ')
    return tf.strings.regex_replace(stripped_html, '[%s]' % re.escape(string.punctuation), '')


export_model = tf.keras.models.load_model('../../data/models/text_classification_export')

sentiment_function_export_model = lambda title: (export_model.predict([title])[0])[0]

df['sentiment_score'] = df['title'].apply(sentiment_function_export_model)

# Remove unnecessary columns
del df['title']

df.to_csv('../../data/files/news_with_scores_export_model.csv', index=False)
