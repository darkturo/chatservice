.PHONY: all clean clean_db
all: build
	docker run -v `pwd`:/opt/chatservice -p 8080:8080 chatservice env PYTHONPATH=/opt/chatservice/lib python /opt/chatservice/server.py

build: Dockerfile
	docker build . --tag chatservice
	touch $@

clean: clean_db
	find -name "*.pyc" -delete
	rm build

clean_db:
	rm /tmp/chat.test.db
