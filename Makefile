.PHONY: run lint fmt

run:
	streamlit run app.py

lint:
	pysen run lint

fmt:
	pysen run format
	autoflake -ri --remove-all-unused-imports --ignore-init-module-imports --remove-unused-variables .