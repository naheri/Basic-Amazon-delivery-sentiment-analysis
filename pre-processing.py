
import pymysql
from transformers import AutoModelForSequenceClassification
from transformers import AutoTokenizer, AutoConfig
import numpy as np
from scipy.special import softmax
from config import *


# Preprocess text (username and link placeholders)
def preprocess(text):
    new_text = []
    for t in text.split(" "):
        t = '@user' if t.startswith('@') and len(t) > 1 else t
        t = 'http' if t.startswith('http') else t
        new_text.append(t)
    return " ".join(new_text)
MODEL = "mrm8488/bert-tiny-finetuned-sms-spam-detection"
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
    text = row['tweet']
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
        print(f"{i+1}) {l} {np.round(float(s), 4)}")
        # get the max label
        max_label = config.id2label[ranking[0]]
        print(max_label)
    if max_label == 'LABEL_1':
        # Execute a DELETE query to delete the row
        cursor.execute("DELETE FROM tweets WHERE id = %s", row['id'])
        # Commit the changes to the database
        connection.commit()

print('Done')
# Close the cursor and connection
cursor.close()
connection.close()

