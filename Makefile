python2:
	python setup.py egg_info -RDb '' sdist bdist_wheel

python3:
	python3 setup.py egg_info -RDb '' bdist_wheel

register:
	python setup.py egg_info -RDb '' register

upload:
	python setup.py egg_info -RDb '' sdist bdist_wheel upload

upload3:
	python setup.py egg_info -RDb '' sdist bdist_wheel upload
