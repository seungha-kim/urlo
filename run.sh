mkdir -p `realpath ~/data`
docker build . -t urlo
docker kill urlo
docker rm urlo
docker run -d --name=urlo -p 8000:8000 --env-file ./env.list -v `realpath ~/data`:/app/data urlo
