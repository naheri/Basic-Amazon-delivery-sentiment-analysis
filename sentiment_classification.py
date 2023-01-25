
import pymysql
from transformers import AutoModelForSequenceClassification
from transformers import AutoTokenizer, AutoConfig
import numpy as np
import pandas as pd
from scipy.special import softmax
import csv
import urllib.request
from config import *

# Preprocess text (username and link placeholders)
def preprocess(text):
    new_text = []
    for t in text.split(" "):
        t = '@user' if t.startswith('@') and len(t) > 1 else t
        t = 'http' if t.startswith('http') else t
        new_text.append(t)
    return " ".join(new_text)

tweets = []
sentiments = []
MODEL = "cardiffnlp/twitter-roberta-base-sentiment-latest"
tokenizer = AutoTokenizer.from_pretrained(MODEL)
config = AutoConfig.from_pretrained(MODEL)
# PT
model = AutoModelForSequenceClassification.from_pretrained(MODEL)


# Connect to the database
connection = pymysql.connect(host=host,
                             user=user,
                             password=password,
                             database=database,
                             cursorclass=pymysql.cursors.DictCursor)

# Create a cursor object to execute queries
cursor = connection.cursor()

# Execute a SELECT query to retrieve all rows from the table
cursor.execute("SELECT * FROM tweets")

# Fetch all the rows as a list of dictionaries
rows = cursor.fetchall()

# Iterate through each row
for row in rows:

    #model.save_pretrained(MODEL)
    text = row['tweet']
    tweets.append(text)
    text = preprocess(text)
    encoded_input = tokenizer(text, return_tensors='pt')
    output = model(**encoded_input)
    scores = output[0][0].detach().numpy()
    scores = softmax(scores)

    ranking = np.argsort(scores)
    ranking = ranking[::-1]
    for i in range(scores.shape[0]):
        l = config.id2label[ranking[i]]
        s = scores[ranking[i]]

    max_label = config.id2label[ranking[0]]
    print(max_label)
    sentiments.append(max_label)

dataframe = pd.DataFrame({'tweets': tweets, 'sentiments': sentiments})
with connection.cursor() as cursor:
    cursor.execute("SELECT date FROM tweets")
    result = cursor.fetchall()
    date_df = pd.DataFrame(result, columns=["date"])

date_df["date"] = date_df["date"].dt.date.apply(lambda x: x.strftime("%Y-%m-%d"))


print(date_df.head())
dataframe = pd.concat([dataframe, date_df], axis=1)
print(dataframe.head())
print('Done !')

# Close the cursor and connection
cursor.close()
connection.close()
