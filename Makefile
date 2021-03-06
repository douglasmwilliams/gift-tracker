PYTHON          = python
APPENGINE       = /mnt/src/google_appengine
APP_ID          = gift-queue
EMAIL           = fjania@gmail.com
SERVE_PORT      = 9091
SERVE_ADDRESS   = 0.0.0.0
DATASTORE_PATH  = ./datastore

help:
	@echo "AppEngine make file. Options are:"
	@echo " test       Runs the test suite"
	@echo " coverage   Runs the test suite and prints a coverage report"
	@echo " deploy     Deploys the current project to AppEngine"
	@echo " rollback   Rolls back a unclosed update to the application"
	@echo " serve      Runs the development web server"
	@echo " console    Opens a development console to your remote application"
	@echo "            (Only works if you've enabled the /remote_api URL)"
	@echo " project    Creates a new project"
	@echo "            (Usage: make project name=yourprojectname)"

test:
	@nosetests --with-gae --with-isolation $(dir)

coverage:
	@nosetests --with-gae --with-isolation --with-coverage $(dir)

deploy:
	@$(PYTHON) $(APPENGINE)/appcfg.py -e $(EMAIL) update .

rollback:
	@$(PYTHON) $(APPENGINE)/appcfg.py -e $(EMAIL) rollback .

serve:
	@$(PYTHON) $(APPENGINE)/dev_appserver.py \
	-a $(SERVE_ADDRESS) \
	-p $(SERVE_PORT) \
	--datastore_path=$(DATASTORE_PATH) \
	--disable_static_caching \
	.

console:
	@$(PYTHON) -c "import code, getpass; \
from google.appengine.ext.remote_api import remote_api_stub; \
auth = lambda: ('$(EMAIL)', getpass.getpass('Password: ')); \
remote_api_stub.ConfigureRemoteDatastore('$(APP_ID)', '/remote_api', auth, '$(APP_ID).appspot.com'); \
code.interact('App Engine console for $(APP_ID)', None, locals());"

project:
ifndef name
	@echo "You must define a project name!"
else
	@mkdir scripts
	@mkdir $(name)
	@mkdir $(name)/handlers
	@mkdir $(name)/handlers/tests
	@mkdir $(name)/library
	@mkdir $(name)/library/tests
	@mkdir $(name)/models
	@mkdir $(name)/models/tests
	@mkdir $(name)/static
	@mkdir $(name)/static/media
	@mkdir $(name)/static/templates
	@touch $(name)/__init__.py
	@touch $(name)/handlers/__init__.py
	@touch $(name)/handlers/tests/__init__.py
	@touch $(name)/library/__init__.py
	@touch $(name)/library/tests/__init__.py
	@touch $(name)/models/__init__.py
	@touch $(name)/models/tests/__init__.py
	@curl --silent -L http://appengine.google.com/favicon.ico > $(name)/static/media/favicon.ico
	@echo "application: $(name)" >> app.yaml
	@echo "version: 1" >> app.yaml
	@echo "runtime: python" >> app.yaml
	@echo "api_version: 1" >> app.yaml
	@echo "" >> app.yaml
	@echo "" >> app.yaml
	@echo "handlers:" >> app.yaml
	@echo "- url: /remote_api" >> app.yaml
	@echo "  script: \$$PYTHON_LIB/google/appengine/ext/remote_api/handler.py" >> app.yaml
	@echo "  login: admin" >> app.yaml
	@echo "" >> app.yaml
	@echo "- url: /_ah/queue/deferred" >> app.yaml
	@echo "  script: \$$PYTHON_LIB/google/appengine/ext/deferred/handler.py" >> app.yaml
	@echo "  login: admin" >> app.yaml
	@echo "" >> app.yaml
	@echo "- url: /favicon.ico" >> app.yaml
	@echo "  static_files: $(name)/static/media/favicon.ico" >> app.yaml
	@echo "  upload: $(name)/static/media/favicon.ico" >> app.yaml
	@echo "queue:" >> queue.yaml
	@echo "- name: default" >> queue.yaml
	@echo "  rate: 5/s" >> queue.yaml
	@echo "  bucket_size: 5" >> queue.yaml
	@echo "cron:" >> cron.yaml
endif

helipad-project: project
	@curl --silent -OL http://github.com/jgeewax/helipad/raw/master/helipad.py
	@curl --silent -OL http://github.com/jgeewax/helipad/raw/master/jinja2
