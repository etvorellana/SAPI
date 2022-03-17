# SAPI


## Backend
### Atualizando dependências

A aplicação utiliza o pip-tools para gerenciamento das dependencias

### instalando pip-tools

```sh
> pip install --upgrade pip  # pip-tools precisa de pip>=6.
> pip install pip-tools
```

### instalando dependencias da aplicação

Rode os comandos abaixo para a instalação das dependencias listadas no arquivo **requirements.txt**

```sh
> cd backend
> pip install -r requirements.txt
```
  
  
### Utilizando variáveis de ambiente

O projeto utiliza variáveis de ambiente através do python-dotenv.

### Adicionando variáveis ao arquivo ```.env```

Pode-se atribuir qualquer valor a variavel no arquivo ```.env```, conforme no exemplo abaixo: 

```ini
DEFAULT_PATH = /home/pi/Pictures/
```

### Usando variáveis do ambiente

Para utilizar as variáveis do ambiente inicializadas no arquivo ```.env```, importe o módulo ```os``` e as funções ```load_dotenv()``` e ```find_dotenv()``` do módulo ```dotenv```.  
  
Logo após, inicialize as variáveis de ambiente utilizando o comando abaixo:

```py
import os
from dotenv import load_dotenv, find_dotenv
  
load_dotenv(find_dotenv())
```  
  
Por fim, resgate as variáveis utilizando o comando ```os.getenv()```.
  
```sh
> os.getenv("DEFAULT_PATH")
```

### Criando ambiente virtual

Para criar o ambiente virtual, basta executar o script ```venv``` através do python. O código abaixo mostra como criar um ambiente virtual chamado ```rpi-cam-prototype-env```:
```sh
> python -m venv rpi-cam-prototype-env
```

### Executando o código

Para executar o projeto, primeiramente será necessário acessar um ambiente virtual já criado:
```sh
> source rpi-cam-prototype-env/bin/activate
```

Após isso, pode-se executar o projeto utilizando o comando:
```sh
> python backend/main.py --arquivo './backend/Flow/Base da dados/Pi camera/PCB_001.png'
```

Para executar o servidor web do flask, execute o seguinte comando:
```sh
> flask run
```

O servidor pode ser acessado pelo endereço ```http://localhost:5000/```

### Executando em Container
```sh
> cd backend
> docker build -t sapi-backend .
> docker run -p 5000:5000 --network="host" sapi-backend
```

## Frontend

### Executando o código

Para desenvolvimento, rode:
```sh
> cd frontend
> ng serve
```
A aplicação estará disponível em `http://localhost:4200/`

### Executando em Container
```sh
> cd frontend
> docker build -t sapi-frontend .
> docker run -p 80:80 --network="host" sapi-frontend
```

## Executando com Compose
```sh
> docker-compose up --build --force-recreate -d

# Para parar os containers
> docker-compose down
```