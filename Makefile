#
# Author: Samuel M.H. <samuel.mh@gmail.com>
# Description:
#    Make-based utility to manage the project.
#    Idea taken from:
#     - http://marmelab.com/blog/2016/02/29/auto-documented-makefile.html

#
### PRECONFIG
#

PYTHON_VERSION := 3.5


#
### PATHS
#
LIBRARY = img_downloader


#Don't touch
PATH_PROJECT = $(shell dirname $(abspath $(lastword $(MAKEFILE_LIST))))
PATH_VENV = $(PATH_PROJECT)/venv
PATH_LIBRARY = $(PATH_PROJECT)/$(LIBRARY)


#
### Autodocumenting thing, don't touch
#
.PHONY: help

.DEFAULT_GOAL := help

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'



#
### Install the project
#
install: ## Create a development environment (virtualenv).
	@echo "Create the environment in "$(PATH_PROJECT)
	@virtualenv -p python$(PYTHON_VERSION) $(PATH_VENV)
	@echo "Install requirements"
	$(PATH_VENV)'/bin/pip' install -r $(PATH_PROJECT)'/deploy/requirements.txt'
	@echo "Create symbolic links"
	# Link to project
	@ln -s $(PATH_PROJECT) $(PATH_VENV)'/'
	# Link code to project library so it is in the PYTHONPATH
	@ln -s $(PATH_LIBRARY) $(PATH_VENV)'/lib/python$(PYTHON_VERSION)/site-packages/'
	# Download the gecko driver (firefox) for selenium
	@echo "Downloading the selenium driver for firefox (gecko)"
	wget https://github.com/mozilla/geckodriver/releases/download/v0.23.0/geckodriver-v0.23.0-linux64.tar.gz
	tar -xzvf geckodriver-v0.23.0-linux64.tar.gz
	rm geckodriver-v0.23.0-linux64.tar.gz
	@echo "Done"



#
### Run things
#

dl_google: ## Download from Google Images. Params: query=<your query>
	$(PATH_VENV)'/bin/python' -m $(LIBRARY).google "$(query)"
