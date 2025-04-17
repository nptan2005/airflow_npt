$env:AIRFLOW_HOME="D:\WorkSpace\Python\airflow-project"
 tanp
Vccb1234

Vccb#1234
win: env\Scripts\activate
docker-compose up airflow-init


docker network create --driver=bridge airflow-external-bridge

docker compose up -d
http://localhost:8080/login

docker exec -it airflow-project-airflow-scheduler-1 bash

docker ps -a
docker logs airflow-project-airflow-webserver-1

--kiem tra db
docker exec -it airflow-project-postgres-1 psql -U airflow -d airflow -c '\l'

--kiem tra network:
docker network inspect airflow-project_default

docker exec -it airflow-project-airflow-webserver-1 ping 172.26.1.32
ssh airflow@172.26.1.32
sudo ufw allow from 172.26.0.0/16 to any port 5432
netstat -tuln | grep 5432

docker network prune
airflow webserver -d

-------------------------
tat:
docker compose down


------------------
git:

git status
git add .
git add <file_name>
git commit -m "Mô tả chi tiết về thay đổi"
git push origin <branch_name>
--
git config --global user.name "Tên của bạn"
git config --global user.email "email@example.com"
git remote add origin <url_repository_git>

