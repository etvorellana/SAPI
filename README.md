# SAPI



## Atualizando dependências

A aplicação utiliza o pip-tools para gerenciamento das dependencias

### instalando pip-tools

```sh
pip install --upgrade pip  # pip-tools precisa de pip>=6.
pip install pip-tools
```

### instalando dependencias da aplicação

Rode os comandos abaixo para a instalação das dependencias listadas no arquivo **requirements.txt**

```sh
pip install -r requirements.txt
```
  
  
## Utilizando variáveis de ambiente

O projeto utiliza variáveis de ambiente através do python-dotenv.

### Adicionando variáveis ao arquivo ```.env```

Pode-se atribuir qualquer valor a variavel no arquivo ```.env```, conforme no exemplo abaixo: 

```
DEFAULT_PATH = /home/pi/Pictures/
```

### Usando variáveis do ambiente

Para utilizar as variáveis do ambiente inicializadas no arquivo ```.env```, importe o módulo ```os``` e as funções ```load_dotenv()``` e ```find_dotenv()``` do módulo ```dotenv```.  
  
Logo após, inicialize as variáveis de ambiente utilizando o comando abaixo:

```
import os
from dotenv import load_dotenv, find_dotenv
  
load_dotenv(find_dotenv())
```  
  
Por fim, resgate as variáveis utilizando o comando ```os.getenv()```.
  
```
os.getenv("DEFAULT_PATH")
```

## Criando ambiente virtual

Para criar o ambiente virtual, basta executar o script ```venv``` através do python. O código abaixo mostra como criar um ambiente virtual chamado ```rpi-cam-prototype-env```:
```
python -m venv rpi-cam-prototype-env
```

## Executando o código

Para executar o projeto, primeiramente será necessário acessar um ambiente virtual já criado:
```
source rpi-cam-prototype-env/bin/activate
```

Após isso, pode-se executar o projeto utilizando o comando:
```
python main.py --arquivo './Flow/Base da dados/Pi camera/PCB_001.png'
```