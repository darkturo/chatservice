TARGET_DIR:=/opt/chatservice
GENERATED_FILES:=Readme.pdf build

.PHONY: all clean clean_db
all: build
	docker run -v `pwd`:${TARGET_DIR} -p 8080:8080 chatservice env PYTHONPATH=${TARGET_DIR}/lib python ${TARGET_DIR}/server.py

doc: build
	docker run -v `pwd`:${TARGET_DIR} chatservice pandoc -o ${TARGET_DIR}/Readme.pdf ${TARGET_DIR}/README.md

build: Dockerfile
	docker build . --tag chatservice
	touch $@

clean: clean_db
	find . -name "*.pyc" -delete
	rm -f ${GENERATED_FILES}

clean_db:
	rm -f /tmp/chat.test.db
