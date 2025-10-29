docker compose up -d
docker compose exec py python -m src.generate_data
docker compose exec py python -m src.seed_loader
docker compose exec py python -m src.gds_train
docker compose exec py python -m src.recommend


