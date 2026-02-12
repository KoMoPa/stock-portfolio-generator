# stock-portfolio-generator
A stock portfolio generator (and mock bank account tracker) developed with Python and Django.

before each session run:
source .venv/bin/activate
git pull origin main
pip install > requirements.txt
docker build -t stock-portfolio-generator .

then you can run this for local dev with migrations:
docker run --env-file .env -p 8000:8000 stock-portfolio-generator

or local dev without migrations:
python manage.py runserver