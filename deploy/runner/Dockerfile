# Образ песочницы для кода учеников: Python + библиотеки для тем о тестировании.
# Собирается командой `python -m app.cli sandbox-check` (её вызывают install.sh и update.sh).
# Меняешь список библиотек — подними номер версии в runner.DEFAULT_IMAGE.
FROM python:3.12-slim
RUN pip install --no-cache-dir "pytest==9.*" "pytest-xdist==3.*" "pydantic==2.*"
