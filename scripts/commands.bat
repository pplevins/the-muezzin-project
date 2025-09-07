@REM Setting up the kafka container - for local running
@REM (for containerization need to set a network and environment variables)
docker run -d -p 9092:9092 --name broker apache/kafka:latest