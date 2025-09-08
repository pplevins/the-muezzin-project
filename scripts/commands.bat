@REM Setting up the kafka container - for local running
@REM (for containerization need to set a network and environment variables)
docker run -d -p 9092:9092 --name broker apache/kafka:latest

@REM Setting the elastic-search and kibana stack in the compose.yaml
docker compose -f compose.yaml up -d

@REM Setting MongoDB container for the binary WAV files
docker run --name mongodb -p 27017:27017 -d mongodb/mongodb-community-server

@REM Getting the project requirements (navigate to the project directory first)
pip freeze > requirements.txt