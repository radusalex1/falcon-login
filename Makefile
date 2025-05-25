init: # initializeaza backendul
	@uv venv
	@uv sync

table: # this is working strange
	@aws dynamodb create-table --cli-input-json file://table_structure/users.json --endpoint-url http://localhost:8000 --region=localhost

run-db: # asta ca sa se creeze db si tabel
	@docker-compose up --build -d && echo "wait 5 seconds for services to be up" && sleep 5
	$(MAKE) table

run-backend: #porneste backendul
	@uv run python3 main.py

run-all: # merge partial
	@docker-compose -f "docker-compose.yml" up -d --build

stop-dynamodb: # opreste baza de date
	@docker stop accu_wather_dynamodb

remove-all: # nu este completa
	@docker system prune