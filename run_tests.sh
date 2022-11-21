echo "is_testing = True" > config.py
coverage run --source=app -m unittest ./unittests/test_unit.py && coverage report -m
