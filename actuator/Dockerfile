FROM python:3.9-slim

WORKDIR /app

# Copia e instala as dependências
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código (incluindo actuator_pb2.py e actuator_pb2_grpc.py)
COPY . .

EXPOSE 50053

CMD ["python3", "actuator_server.py"]
