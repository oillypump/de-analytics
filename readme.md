# Dashboard Analytics

- [ ] definiskan apa project ini,
- [ ] definisikan bagaimana cara kerja project ini

[de_analytics_dashboard](http://35.223.23.31:3000/public/dashboard/53ca46a7-2745-406e-ac8e-482846b61675)

<<<<<<< HEAD
## to do
[] create dashboard wordcloud yang isinya 
[] tarik ulang data content pass date untuk wordcloud
[X] scrip counter nama tokoh berhasil running, tinggal penyesuaian input dan outputnya,
[] tarik ulang table data untuk content
=======
### to do
- [ ] create dashboard wordcloud yang isinya 
- [ ] tarik ulang data content pass date untuk wordcloud
- [ ] jelaskan penggunaan google
- [ ] jelaskan penggunaan prefect
- [ ] jelaskan docker  

>>>>>>> 37d5a90c122f771856d5f7db92cb6445d6b58870

## dataflow

![df](pict/dateng_proj-Dataflow.drawio.png)

## architecture

![df](pict/dateng_proj-architecture.drawio1.png)

# Technology Used

## python

to generate what existing libs
```
pip freeze >> requirements.txt
```

## google 

### google vm

```
export GOOGLE_APPLICATION_CREDENTIALS="<path/to/your/service-account-authkeys>.json"
gcloud auth application-default login
```

```
ssh-keygen -t rsa -f ~/.ssh/KEY_FILENAME -C USERNAME -b 2048
```

### google bucket


## prefect 

1. prefect agent running di local
2. prefect cloud running di cloud menggantikan prefect UI, 


syntax :

```
prefect server start
prefect agent start -q 'default'
```

```
nohup prefect server start > server.logs
nohup prefect agent start -q 'default' > agent.logs

```
*Note* prefect server tidak digunakan karena sudah digantikan oleh prefect cloud

## docker 

### 1. metabase
### 2. postgresql

If you see that folder pg_data is empty after running the container, try these:

Deleting the folder and running Docker again (Docker will re-create the folder)
Adjust the permissions of the folder by running 
```
sudo chmod a+rwx {your_folder_name}
```

### 3. pgadmin

syntax for pgadmin after docker compose up:

```
sudo chown 5050:5050 data_pgadmin
```

### misc


```
gcsfuse -o allow_other  -file-mode=777 -dir-mode=777 test_bucket_00 /data/cloud/tb-00
```