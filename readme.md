## changeme

ini nambah


gcsfuse -o allow_other  -file-mode=777 -dir-mode=777 test_bucket_00 /data/cloud/tb-00

```
prefect api key
pnu_FJ0dVjfh2T91niQMlySjhwqFNM4jvY0xpSeY
pnu_R3eC1ZtFElDACh7svO654YLRhQ1Cvh1jmq4l
```

```
sudo chown 5050:5050 data_pgadmin
```

If you see that ny_taxi_postgres_data is empty after running the container, try these:

Deleting the folder and running Docker again (Docker will re-create the folder)
Adjust the permissions of the folder by running ```sudo chmod a+rwx ny_taxi_postgres_data```



# google 


```
export GOOGLE_APPLICATION_CREDENTIALS="<path/to/your/service-account-authkeys>.json"
gcloud auth application-default login
```

```
ssh-keygen -t rsa -f ~/.ssh/KEY_FILENAME -C USERNAME -b 2048
```


pip freeze >> requirements.txt


# prefect 

```
prefect server start
prefect agent start -q 'default'
```

```
nohup prefect server start > server.logs
nohup prefect agent start -q 'default' > agent.logs

```
