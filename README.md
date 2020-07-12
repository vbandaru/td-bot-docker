# td-bot-docker

## pip compile

pip-compile requirements.in


### build image

docker build -t td-bot-docker-rpi:latest -f Dockerfile.rpi .

docker run -it  \
-e APCA_API_KEY_ID=$APCA_API_KEY_ID \
-e APCA_API_SECRET_KEY=$APCA_API_SECRET_KEY \
-e APCA_API_BASE_URL=$APCA_API_BASE_URL \
-e SLACK_API_TOKEN=$SLACK_API_TOKEN \
-e TZ=America/New_York \
td-bot-docker-rpi:latest /bin/bash

docker run -it  \
-e APCA_API_KEY_ID=$APCA_API_KEY_ID \
-e APCA_API_SECRET_KEY=$APCA_API_SECRET_KEY \
-e APCA_API_BASE_URL=$APCA_API_BASE_URL \
-e SLACK_API_TOKEN=$SLACK_API_TOKEN \
-e TZ=America/New_York \
-v $(pwd):/usr/app \
td-bot-docker-rpi:latest python /usr/app/alerter.py

docker run -it  \
-e APCA_API_KEY_ID=$APCA_API_KEY_ID \
-e APCA_API_SECRET_KEY=$APCA_API_SECRET_KEY \
-e APCA_API_BASE_URL=$APCA_API_BASE_URL \
-e SLACK_API_TOKEN=$SLACK_API_TOKEN \
-e TZ=America/New_York \
-v $(pwd):/usr/app \
td-bot-docker-rpi:latest python /usr/app/alerter.py

docker run -it  \
-e APCA_API_KEY_ID=$APCA_API_KEY_ID \
-e APCA_API_SECRET_KEY=$APCA_API_SECRET_KEY \
-e APCA_API_BASE_URL=$APCA_API_BASE_URL \
-e SLACK_API_TOKEN=$SLACK_API_TOKEN \
-v $(pwd):/usr/app \
td-bot-docker-ubuntu:latest python /usr/app/smoketest.py


docker run -it  \
    arm32v7/python:3.7-stretch /bin/sh

docker run -it  \
    python:3.7-stretch /bin/sh

env | grep APCA (verify)

#### clear old images

docker system prune -af


@jfh7j you asked about strategies and i am using a technology company
that crunches a lot of data and backtests
the founder is a MIT grad
they report win and loss rates and very detailed test data
today i did some day trading but that is usually my go to
you can check them out if you want
but it costs money
a sub basis
http://cmlviz.com/
its costs around 150 dollars a month