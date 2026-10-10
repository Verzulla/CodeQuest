# Образ песочницы для кода учеников: Python + библиотеки для тем о тестировании.
# Собирается командой `python -m app.cli sandbox-check` (её вызывают install.sh и update.sh).
# Меняешь список библиотек — подними номер версии в runner.DEFAULT_IMAGE.
FROM python:3.12-slim
RUN pip install --no-cache-dir \
    "pytest==9.*" "pytest-xdist==3.*" "pydantic==2.*" "allure-pytest==2.*" \
    "requests==2.*" "responses==0.*" "httpx==0.*" "jsonschema==4.*" "pyyaml==6.*"
# pwfake — учебная реализация Playwright API без браузера (темы про UI-тесты)
COPY pwfake /tmp/pwfake
RUN pip install --no-cache-dir /tmp/pwfake && rm -rf /tmp/pwfake
# kafkafake — учебная Kafka в памяти с API confluent-kafka (тема «Kafka для тестировщика»)
COPY kafkafake /tmp/kafkafake
RUN pip install --no-cache-dir /tmp/kafkafake && rm -rf /tmp/kafkafake
