# token-analysis
analysis blockchain tokens

## env

use python3.9 and poetry
```
poetry install
```

start
```
streamlit run app.py
```

## config and data

### config

(optional) coinmarketcap api key, make file `./config/coinmarketcap.json`, in format `./config/coinmarketcap_sample.json`

### data

put coinmarket data under folder `./data/coinmarket`

data: 

https://graph-pub.s3.ap-northeast-1.amazonaws.com/token-analysis/coinmarket.zip

put model under `./data/models`

model:

https://graph-pub.s3.ap-northeast-1.amazonaws.com/token-analysis/models.zip
