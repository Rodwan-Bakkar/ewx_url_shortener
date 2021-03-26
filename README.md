
This is a simple URL shortener.

Easy steps to spin it up in your machine for development:
- create a virtual environment in the root folder: virtualenv -p python3 .venv
- activate the virtual environment: source .venv/bin/activate 
- install all the requirements: pip install -r requirements.txt
- install the project in editable mode: pip install e .
- run the following command: ewx_url_short
- redis should be installed and run on localhost, port 6379

This projects allow you to choose your own database by implementing the StorageBase 
abstract class, a redis implementations is provided. If you implement your own, 
plug it in by instantiating it in app.py and passing it as dependency to the necessary classes

For testing:
you can run all the tests by: python -m unittest discover tests




