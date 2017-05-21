ship:
	python setup.py sdist bdist_wheel
	twine upload dist/*

demo:
	python demo.py
