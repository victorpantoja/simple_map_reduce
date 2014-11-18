
help:
	@echo ''
	@echo 'Targets:'
	@echo ''
	@echo 'test:                    Executa todos os testes do sportv'
	@echo 'clean:                   Remove os arquivos .pyc'


clean:
	@echo "Cleaning up build, *.pyc..."
	@find . -name '*.pyc' -delete


tests: clean
	@echo "Running tests..."
	@export PYTHONPATH=$PYTHONPATH:`pwd`:`pwd`/food_processor  &&  \
		cd food_processor && \
	    nosetests -s --verbose --with-coverage --cover-package=food_processor tests/*
