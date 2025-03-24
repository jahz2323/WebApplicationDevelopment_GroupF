FROM ubuntu:latest
LABEL authors="jahziel belmonte"

ENTRYPOINT ["top", "-b"]