.DEFAULT_GOAL := help

# Install requirements
install:
	pip install -r requirements.txt

# Validate Python code according to the style guide.
flake:
	flake8 --count --max-complexity=10 --statistics .

# Reformat Python code according to the style guide.
black:
	black .
