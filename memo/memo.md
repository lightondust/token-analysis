https://codechacha.com/ja/ubuntu-install-python39/

```
sudo apt update
sudo apt install software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt install python3.9
```

```
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python3.9 -
```


# make streamlit a service
```
[Unit]
Description=token analysis
After=network.target

[Service]
WorkingDirectory=/home/ubuntu/token-analysis/token_analysis
ExecStart=/home/ubuntu/.cache/pypoetry/virtualenvs/token-analysis-azVAQTvs-py3.9/bin/python /home/ubuntu/.cache/pypoetry/virtualenvs/token-analysis-azVAQTvs-py3.9/bin/streamlit run app.py --server.port 8501
User=ubuntu

[Install]
WantedBy=multi-user.target
```

```
sudo systemctl daemon-reload
sudo systemctl start token_analysis.service
sudo systemctl enable token_analysis.service
```