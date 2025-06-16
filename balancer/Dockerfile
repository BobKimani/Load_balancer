FROM python:3.9-slim
WORKDIR /app
COPY . .
RUN pip install flask requests
CMD ["python", "load_balancer.py"]
