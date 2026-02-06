# stock-portfolio-generator
A stock portfolio generator (and mock bank account tracker) developed with Python and Django.

docker build -t stock-portfolio-generator .

docker run --env-file .env -p 8000:8000 stock-portfolio-generator