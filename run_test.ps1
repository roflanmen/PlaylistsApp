'is_testing = True' | Out-File -FilePath .\config.py
coverage run --source=app -m unittest discover ; if ($?) { coverage report -m }
'is_testing = False' | Out-File -FilePath .\config.py