# Amazon delivery sentiment analysis
## Requirements
AWS account.
## How I did it.
Using an [ec2 instance](https://aws.amazon.com/fr/ec2/) (to speed up the sentiment analysis process), I used the [snscrape](https://github.com/JustAnotherArchivist/snscrape) library to scrape tweets, I put them all in a [RDS database](https://aws.amazon.com/fr/rds/) and I pre-processed all these tweets (filter spam) using this pre-trained [model](https://huggingface.co/mrm8488/bert-tiny-finetuned-sms-spam-detection) (I know it's an SMS and not tweets spam detector but I ran a lot of tests and it turned out to be the more accurate).

Then, with the spam tweets gone, I began the sentiment analysis with this pre-trained [model](https://huggingface.co/cardiffnlp/twitter-roberta-base-sentiment-latest), 
## Results
![alt text](./plots_amazon/barplot_per_year.png)
![alt text](plots_amazon/sentiment_distribution.png)
![alt text](plots_amazon/n_wordcloud.png)
![alt text](plots_amazon/p_wordcloud.png)

## What to conclude from that ?

