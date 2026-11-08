FROM python:3.14

WORKDIR /usr/app

RUN pip install --no-cache-dir uv

COPY dist/chat_app-0.1.0.tar.gz .

RUN uv pip install --system ./chat_app-0.1.0.tar.gz

EXPOSE 8080

CMD ["uvicorn", "chat_app.main:app", "--host", "0.0.0.0", "--port", "8080"]