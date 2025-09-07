@REM Setting up the kafka container - for local running
@REM (for containerization need to set a network and environment variables)
docker run -d -p 9092:9092 --name broker apache/kafka:latest

@REM Setting the elastic-search and kibana stack in the compose.yaml
docker compose -f compose.yaml up -d