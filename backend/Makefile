dev:
	uv run uvicorn app.main:app --host 0.0.0.0 --port 8002 --workers 1 --reload

# make db_migrate m="<message>"
db_auto_migrate:
	uv run alembic revision -m "$(m)" --autogenerate

db_migrate:
	uv run alembic revision -m "$(m)"

db_upgrade_one:
	uv run alembic upgrade head

db_upgrade_all:
	uv run alembic upgrade heads

# make db_upgrade r=<revision>
db_upgrade:
	uv run alembic upgrade $(r)

db_downgrade:
	uv run alembic downgrade $(r)

db_stamp:
	uv run alembic stamp $(r)
db_history:
	uv run alembic history

db_current:
	uv run alembic current

db_sql:
	uv run alembic upgrade $(x):$(y) --sql > $(z)

polling:
	uv run python -m app.bot.polling