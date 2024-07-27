# seed

### setup:

`` $ find . | grep -E "(__pycache__|\.pyc|\.pyo$)" | xargs sudo rm -rf ``

`` $ chmod +x src/entrypoint.sh ``

`` $ docker-compose up ``

### development (only with tests):

### In another tab

`` $ docker-compose exec fastapi bash ``

`` $ doit all ``

### To generate migration:

make sure that all models are present in db/alembic_classes.py - mapper_classes

`` $ doit migration -m "<message>"``
