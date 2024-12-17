FROM python:3.9-slim

WORKDIR /app

COPY extract_temp.py .

RUN pip install requests

CMD ["python", "extract_temp.py"]