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

`sudo vim /etc/systemd/system/token_analysis.service`

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

# nginx port forward

`vim /etc/nginx/sites-available/default`
```
server {  
              listen 80; 
              server_name localhost; 
              keepalive_timeout 5; 
 
              location /tokenanalysis/ { 
                  proxy_pass http://127.0.0.1:8501/; 
              } 
              location /tokenanalysis/static { 
                  proxy_pass http://127.0.0.1:8501/static/; 
              } 
              location /tokenanalysis/healthz { 
                  proxy_pass http://127.0.0.1:8501/healthz; 
              } 
              location /tokenanalysis/vendor { 
                  proxy_pass http://127.0.0.1:8501/vendor; 
              } 
              location /tokenanalysis/stream { 
                  proxy_pass http://127.0.0.1:8501/stream; 
                  proxy_http_version 1.1; 
                  proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for; 
                  proxy_set_header Host $host; 
                  proxy_set_header Upgrade $http_upgrade; 
                  proxy_set_header Connection "upgrade"; 
                  proxy_read_timeout 86400; 
              }
}   
```