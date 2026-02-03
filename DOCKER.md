# For Docker Dev Run These 2
docker build -t stock-portfolio-generator .

docker run --env-file .env -p 8000:8000 stock-portfolio-generator

# For Local Dev Run
source .venv/bin/activate
python manage.py runserver

# When to use which:
Docker: Testing in the same environment as each other, before sharing code
venv: Day-to-day development, faster startup, no rebuild needed for code changes

## *Both connect to the same Supabase database.*