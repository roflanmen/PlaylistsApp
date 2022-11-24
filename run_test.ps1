'is_testing = True' | Out-File -FilePath .\config.py
coverage run --source=app -m unittest discover ; if ($?) { coverage report -m }