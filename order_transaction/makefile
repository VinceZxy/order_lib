.PHONY: help prepare-dev test lint run doc

VENV_NAME?=venv
VENV_ACTIVATE=./$(VENV_NAME)/bin/activate
PYTHON=${VENV_NAME}/bin/python3
VENV_PATH=venv

.DEFAULT: help
help: 
	@echo "make prepare-dev"
	@echo "       prepare development environment, use only once"
	@echo "make test"
	@echo "       run tests"
	@echo "make lint"
	@echo "       run pylint and mypy"
	@echo "make run"
	@echo "       run project"
	@echo "make clean"
	@echo "       clean python cache files"
	@echo "make doc"
	@echo "       build sphinx documentation"

# 安装python 和 搭建虚拟环境
prepare-dev:
	sudo yum install python36 python36-pip -y
	sudo pip3 install -i https://pypi.douban.com/simple --user virtualenv
	mkdir static logs
	python3 -m venv venv

# 进入虚拟环境
venv:
	source ${VENV_PATH}/bin/activate
dep:
	pip3 install -i https://pypi.douban.com/simple --upgrade pip
	pip3 install -i https://pypi.douban.com/simple  -r ./requirements.txt		

test: venv
	${PYTHON} -m pytest

lint: venv
	${PYTHON} -m pylint
	${PYTHON} -m mypy

run: venv
	${PYTHON} ./main.py


