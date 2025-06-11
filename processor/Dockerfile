# Use Python slim
FROM python:3.9-slim

# Cria diretório de trabalho
WORKDIR /app

# Copia requirements e instala deps
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código do serviço
COPY . .

# Expõe a porta gRPC padrão (ajuste conforme cada serviço)
EXPOSE 50052

# Comando de inicialização (ajuste o nome do arquivo)
CMD ["python", "processor_server.py"]