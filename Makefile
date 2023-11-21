.PHONY: all lint

all_tests: lint unittest integrationtest

help:
	@echo "Please use 'make <target>' where <target> is one of:"
	@echo "  lint			to run flake8 on all Python files"
	@echo "  unittest		to run unit tests on SpikingAI"
	@echo "  integrationtest		to run integration tests"

lint:
	@flake8 SpikingAI

unittest:
	@py.test -m "not integration" --cov-append --cov-report xml --cov-report term-missing --cov=SpikingAI SpikingAI

performancetest:
	@py.test -m "integration" --cov-append --cov-report xml --cov-report term-missing --cov=SpikingAI SpikingAI
