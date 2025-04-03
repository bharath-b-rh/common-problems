export GOOS=linux

all: build

.PHONY: build
build:
	mkdir -p bin
	go build -o bin/problems *.go
