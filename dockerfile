# Use a imagem oficial do Python 3.8
FROM python:3.8

# Define o diretório de trabalho
WORKDIR /Users/erika.pimentel/Documents/localizador_escolas/app.py

# Copia os requisitos e instala as dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia todos os arquivos para o diretório de trabalho
COPY . .

# Comando para executar o script Python
CMD ["python", "app.py"]
