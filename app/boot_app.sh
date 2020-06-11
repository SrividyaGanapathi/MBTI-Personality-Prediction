#!/usr/bin/env bash
#winpty docker run -it -e AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY -e AWS_DEFAULT_REGION=$AWS_DEFAULT_REGION -e MYSQL_USER=$MYSQL_USER -e MYSQL_PASSWORD=$MYSQL_PASSWORD -p 3000:3000  --mount type=bind,source="$(pwd)/data",target=/app/data --name testapp mbti_app app.py

winpty docker run -it --env AWS_ACCESS_KEY_ID --env AWS_SECRET_ACCESS_KEY  --env MYSQL_HOST --env MYSQL_PORT --env MYSQL_USER --env MYSQL_PASSWORD -p 3000:3000  --mount type=bind,source="$(pwd)/data",target=/app/data --name testapp mbti_app app.py