find -name "migrations" -not -path "./venv/*" | xargs rm -r
find -name "__pycache__" -not -path "./venv/*" | xargs rm -r
