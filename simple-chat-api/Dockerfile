FROM python:3.11-alpine3.18 as base

COPY ./ /home/simple-chat-api/
WORKDIR /home/simple-chat-api/

RUN apk update && \
	apk add --update --no-cache alpine-sdk gcc libffi-dev && \
	pip install --upgrade pip && \
	pip wheel --wheel-dir=/home/simple-chat-api/wheels -r requirements.txt

FROM python:3.11-alpine3.18

COPY --from=base /home/simple-chat-api/ /home/simple-chat-api/
WORKDIR /home/simple-chat-api/

RUN apk update && \
	apk add --update --no-cache bash curl && \
	mkdir /home/assets && \
	pip install --no-index --find-links=/home/simple-chat-api/wheels -r requirements.txt && \
	rm -rf /home/simple-chat-api/wheels && chmod +x /home/simple-chat-api/imfast.sh

EXPOSE 5000

CMD ["/home/simple-chat-api/imfast.sh", "prod-run"]