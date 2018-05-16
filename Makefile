IMG_NAME := bufferapp/24x-to-datadog

.PHONY: all
all:
	docker build -t $(IMG_NAME) -f Dockerfile .
	docker run -v $(PWD):/app -it --rm --env-file .env $(IMG_NAME)

run:
	docker run -v $(PWD):/app -it --rm --env-file .env $(IMG_NAME)

.PHONY: push
push:
	docker push $(IMG_NAME)

.PHONY: deploy
deploy:
	docker build -t $(IMG_NAME) -f Dockerfile .
	docker push $(IMG_NAME)
