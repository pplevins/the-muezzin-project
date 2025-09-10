@REM Setting up the kafka container - for local running
@REM (for containerization need to set a network and environment variables)
docker run -d -p 9092:9092 --name broker apache/kafka:latest

@REM Setting the elastic-search and kibana stack in the compose.yaml
docker compose -f compose.yaml up -d

@REM Setting MongoDB container for the binary WAV files
docker run --name mongodb -p 27017:27017 -d mongodb/mongodb-community-server

@REM Getting the project requirements (navigate to the project directory first)
pip freeze > requirements.txt

@REM Preparing for containerization
cd C:\Users\share\PycharmProjects\kodkode\the-muezzin-project

docker compose -f compose.yaml up -d

@REM Coping all the podcast to the docker volume
cd /podcasts
docker cp . processor:/app/data

@REM now starting the publisher
docker start the-muezzin-project-publisher-1

@REM Tagging and pushing the images to dockerhub
docker tag the-muezzin-project-publisher:latest pplevins/the-muezzin-project-publisher:latest
docker tag the-muezzin-project-processor:latest pplevins/the-muezzin-project-processor:latest
docker tag the-muezzin-project-transcriber:latest pplevins/the-muezzin-project-transcriber:latest
docker tag the-muezzin-project-classifier:latest pplevins/the-muezzin-project-classifier:latest
docker push pplevins/the-muezzin-project-publisher:latest
docker push pplevins/the-muezzin-project-processor:latest
docker push pplevins/the-muezzin-project-transcriber:latest
docker push pplevins/the-muezzin-project-classifier:latest
