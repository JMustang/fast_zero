# Tutorial de Python com FastAPI

## Baseado no tutorial do **dunossauro**

Link da fonte: [Tutorial FastAPI do dunossauro](https://fastapidozero.dunossauro.com/)

### Instalação do Python 3.11

Se você precisar reconstruir o ambiente usado neste curso, é recomendado que você use o pyenv.

Caso tenha problemas durante a instalação, o pyenv conta com dois assistentes simplificados para sua configuração. Para Windows, use o pyenv-windows. Para GNU/Linux e MacOS, use o pyenv-installer.

### Instalando o Pyenv

Copie e cole o seguinte comando no terminal:

```bash
curl -L https://github.com/pyenv/pyenv-installer/raw/master/bin/pyenv-installer | bash
```

Abra o arquivo .**zshrc** e adicione:

```bash
export PYENV_ROOT="$HOME/.pyenv"

export PATH="$PYENV_ROOT/bin:$PATH"

if command -v pyenv 1>/dev/null 2>&1; then

eval "$(pyenv init --path)"

fi
```

Navegue até o diretório onde você fará os exercícios e executará os códigos de exemplo no seu terminal e digite os seguintes comandos:

```bash
pyenv update
pyenv install 3.11:latest
```

Certifique-se de que a versão do Python 3.11 esteja instalada:

```bash
pyenv versions
* system (set by /home/USUARIO/.pyenv/version)
  3.10.12
  3.11.4
  3.12.0b1
```

### Poetry

Após instalar o Python, o próximo passo é instalar o Poetry, um gerenciador de pacotes e dependências para Python. O Poetry facilita a criação, o gerenciamento e a distribuição de pacotes Python.

Recomenda-se usar o **pipx** para a instalação:

```bash
pipx install poetry
```

### Criação do Projeto FastAPI e Instalação das Dependências

Agora que temos o Python e o Poetry prontos, vamos começar a criar nosso projeto FastAPI.

Para começar, vamos criar um novo projeto usando o poetry:

```bash
poetry new nome_do_diretorio
# Navegue até o diretório
cd nome_do_diretorio
```

Uma estrutura como a seguinte será criada:

```bash
.
├── fast_zero
│  └── __init__.py
├── pyproject.toml
├── README.md
└── tests
   └── __init__.py
```

Para garantir que a versão que instalamos com pyenv seja usada em nosso projeto criado com poetry, devemos informar ao pyenv qual versão do Python será usada nesse diretório:

```bash
pyenv local 3.11.4
```

Além disso, devemos dizer ao poetry que usaremos essa versão em nosso projeto. Para isso, vamos modificar o arquivo de configuração do projeto, o pyproject.toml, na raiz do projeto:

```toml
[tool.poetry.dependencies]
python = "3.11.*"
```

Em seguida, inicializaremos um novo projeto Python com Poetry e instalaremos as dependências necessárias, FastAPI e Uvicorn:

```bash
# O comando poetry install adiciona um arquivo chamado poetry.lock, que funciona como o package.json do Node.js
poetry install

# Adiciona as bibliotecas FastAPI e Uvicorn ao projeto
poetry add fastapi uvicorn
```

### Primeira Execução de um "Hello, World!"

Para garantir que tudo está configurado corretamente, vamos criar um pequeno programa "Hello, World!" com FastAPI. Primeiro, crie um novo arquivo chamado `app.py` no diretório `fast_zero` e adicione o seguinte código:

```python
from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def read_root():
    return {'message': 'Olá Mundo!'}
```

Agora, podemos iniciar nosso servidor FastAPI com os seguintes comandos:

```bash
# O comando poetry shell ativa o ambiente virtual
poetry shell

# O uvicorn cria um servidor local para testar a API
uvicorn fast_zero.app:app --reload
```

Acesse <http://localhost:8000> no seu navegador e você deve ver a mensagem "Olá Mundo!" no formato JSON.

Claro, aqui está o texto melhorado:

### Instalando as Ferramentas de Desenvolvimento

As ferramentas de desenvolvimento escolhidas podem variar de acordo com as preferências pessoais. Nesta aula, usaremos algumas ferramentas que são particularmente úteis para demonstrar certos conceitos:

- **taskipy**: Ferramenta para automatizar alguns comandos e simplificar o fluxo.
- **ruff**: Um linter que ajuda a identificar possíveis problemas no código.
- **blue**: Um formatador de código amigável e de fácil utilização.
- **isort**: Uma ferramenta para organizar os imports de forma alfabética e organizada.
- **pytest**: Uma ferramenta para executar testes de forma eficiente.

Para instalar as dependências, podemos usar um grupo específico do poetry, focado no ambiente de desenvolvimento, para que essas ferramentas não sejam usadas em produção:

```bash
poetry add --group dev pytest pytest-cov taskipy blue ruff httpx isort
```

### Configurando as Ferramentas de Desenvolvimento

Após a instalação das dependências, precisamos configurar todas as ferramentas de desenvolvimento no arquivo `pyproject.toml`.

#### Ruff

Começando pelo `ruff`, vamos definir o comprimento de linha para 79 caracteres (conforme sugerido na PEP 8) e, em seguida, informaremos que o diretório do ambiente virtual e as migrações de banco de dados devem ser ignorados:

```toml
[tool.ruff]
line-length = 79
exclude = ['.venv', 'migrations']
```

#### Isort

Para evitar conflitos de formatação entre o `isort` e o `blue`, definiremos o `black` como perfil de formatação a ser seguido, já que o `blue` é um fork dele. Como o `black` utiliza 88 caracteres por linha, vamos alterar para 79, que é o padrão que o `blue` segue e que também estamos seguindo:

```toml
[tool.isort]
profile = "black"
line_length = 79
extend_skip = ['migrations']
```

#### Pytest

Configuraremos o `pytest` para reconhecer o caminho base para execução dos testes na raiz do projeto:

```toml
[tool.pytest.ini_options]
pythonpath = "."
```

#### Blue

Configuraremos o `blue` para excluir o caminho das migrações quando essas forem utilizadas:

```toml
[tool.blue]
extend-exclude = '(migrations/)'
```

#### Taskipy

Para simplificar a execução de certos comandos, vamos criar algumas tarefas com o `Taskipy`:

```toml
[tool.taskipy.tasks]
lint = 'ruff . && blue --check . --diff'
format = 'blue . && isort .'
run = 'uvicorn fast_zero.app:app --reload'
pre_test = 'task lint'
test = 'pytest -s -x --cov=fast_zero -vv'
post_test = 'coverage html'
```

Os comandos definidos fazem o seguinte:

- `lint`: executa o `ruff` para verificar se não há problemas no código e se está em conformidade com a PEP-8.
- `format`: formata o código usando `blue` e `isort`.
- `run`: executa o servidor de desenvolvimento do FastAPI.
- `pre_test`: executa a camada de lint antes de executar os testes.
- `test`: executa os testes com o `pytest` de forma detalhada e adiciona nosso código como base de cobertura.
- `post_test`: gera um relatório de cobertura após os testes.

Para executar um comando, basta usar a palavra `task` seguida do nome da tarefa específica que criamos acima.

### Os efeitos das Configurações de Desenvolvimento

Se você tiver copiado o código que usamos para definir `fast_zero/app.py`, pode testar os comandos que criamos para o `taskipy`:

```bash
task lint
```

Se o seu código tiver algum erro de formatação da PEP-8, o `blue` informará:

```bash
--- fast_zero/app.py    2023-07-12 21:40:14.590616 +0000
+++ fast_zero/app.py    2023-07-12 21:48:17.017190 +0000
@@ -1,7 +1,8 @@
 from fastapi import FastAPI

 app = FastAPI()

+
 @app.get('/')
 def read_root():
     return {'message': 'Olá Mundo!'}
```

Para corrigir isso, podemos usar o comando de formatação de código:

```bash
task format
```

Será exibida a seguinte mensagem:

```bash
reformatted fast_zero/app.py

All done! ✨ 🍰 ✨
1 file reformatted, 2 files left unchanged.
Skipped 2 files
```

### Pytest: Testando o "Hello, World!"

Antes de mergulharmos na dinâmica dos testes, é essencial compreender o impacto que eles têm no nosso código. Um bom ponto de partida é analisar a cobertura dos testes. Vamos executar os testes.

```bash
task test
```

Você receberá uma resposta como esta:

```bash
All done! ✨ 🍰 ✨
3 files would be left unchanged.
===================================== test session starts ======================================
platform darwin -- Python 3.11.2, pytest-7.4.3, pluggy-1.3.0 -- /Users/junior/Library/Caches/pypoetry/virtualenvs/fast-zero-bfgtZX6i-py3.11/bin/python
cachedir: .pytest_cache
rootdir: /Users/junior/Documents/www/python/FastAPI/fast_zero
configfile: pyproject.toml
plugins: cov-4.1.0, anyio-3.7.1
collected 0 items
/Users/junior/Library/Caches/pypoetry/virtualenvs/fast-zero-bfgtZX6i-py3.11/lib/python3.11/site-packages/coverage/control.py:883: CoverageWarning: No data was collected. (no-data-collected)
  self._warn("No data was collected.", slug="no-data-collected")


---------- coverage: platform darwin, python 3.11.2-final-0 ----------
Name                    Stmts   Miss  Cover
-------------------------------------------
fast_zero/__init__.py       0      0   100%
fast_zero/app.py            5      5     0%
-------------------------------------------
TOTAL                       5      5     0%
```

As primeiras duas linhas são referentes ao comando `pre_test` do `taskipy`, que executa o `blue` e o `ruff` antes de cada teste. As linhas seguintes são referentes ao `pytest`, que informou que não foram coletados itens, ou seja, nenhum teste foi executado.

A parte crucial dessa mensagem está na tabela gerada pelo `coverage`. Ela indica que temos 5 linhas de código (`Stmts`) no arquivo `fast_zero/app.py` e nenhuma delas está coberta pelos nossos testes, como pode ser observado na coluna `Miss`.

Como nenhum teste foi encontrado, o `pytest` retornou um "erro". Isso implica que nossa tarefa `post_test` não foi executada. Podemos executá-la manualmente:

```bash
task post_test
```

Isso gera um relatório de cobertura de testes no formato HTML. Podemos abrir esse arquivo em nosso navegador e entender exatamente quais linhas do código não estão sendo testadas.

![Coverage Report](https://fastapidozero.dunossauro.com/assets/02_navegador_com_pagina_inicial_do_coverage.png)

Ao clicar no arquivo `fast_zero/app.py`, podemos visualizar em vermelho as linhas que não estão sendo testadas.

![Coverage Report Without Tests](https://fastapidozero.dunossauro.com/assets/02_navegador_com_pagina_de_cobertura_sem_testes.png)

Isso indica que precisamos criar testes para cobrir todo esse arquivo.

### Escrevendo o Teste

Agora, vamos criar nosso primeiro teste com Pytest.

Para testar o FastAPI, precisamos de um cliente de teste. Podemos obtê-lo no módulo `fastapi.testclient` com o objeto `TestClient`, que precisa receber nosso `app` como parâmetro. Vamos criar um arquivo no diretório `tests` chamado `test_app.py` e adicionar o seguinte código:

```python
from fastapi.testclient import TestClient
from fast_zero.app import app

client = TestClient(app)
```

O simples fato de definirmos um cliente já reflete uma cobertura significativamente diferente. Execute o comando `task test` no terminal:

```bash
task test
```

Se algum erro de formatação for apresentado, execute `task format` novamente e, em seguida, execute o teste.

```bash
---------- coverage: platform darwin, python 3.11.2-final-0 ----------
Name                    Stmts   Miss  Cover
-------------------------------------------
fast_zero/__init__.py       0      0   100%
fast_zero/app.py            5      1    80%
-------------------------------------------
TOTAL                       5      1    80%
```

Como nenhum teste foi coletado, o pytest ainda retorna um "erro". Para ver a cobertura, precisaremos executar manualmente o `post_test` novamente. Execute o comando `task post_test`:

```bash
task post_test
```

No navegador, podemos observar que a única linha não "testada" é aquela que contém a lógica do endpoint.

![Coverage Report with Test Structure](https://fastapidozero.dunossauro.com/assets/02_navegador_com_pagina_de_cobertura_com_estrutuda_de_testes.png)

Os trechos em verde mostram o que foi executado durante o teste, enquanto os trechos em vermelho indicam o que não foi testado.

Para resolver isso, precisamos criar um teste de fato, fazendo uma chamada para nossa API usando o cliente de teste que definimos. Adicione o seguinte teste:

```python
from fastapi.testclient import TestClient
from fast_zero.app import app

def test_root_deve_retornar_200_e_ola_mundo():
    client = TestClient(app)
    response = client.get('/')

    assert response.status_code == 200
    assert response.json() == {'message': 'Olá Mundo!'}
```

Esse teste realiza uma requisição GET no endpoint `/` e verifica se o código de status da resposta é 200 e se o conteúdo da resposta é {'message': 'Olá Mundo!'}.

Você deve ver uma mensagem como esta:

```bash
collected 1 item

tests/test_app.py::test_root_deve_retornar_200_e_ola_mundo PASSED

---------- coverage: platform darwin, python 3.11.2-final-0 ----------
Name                    Stmts   Miss  Cover
-------------------------------------------
fast_zero/__init__.py       0      0   100%
fast_zero/app.py            5      0   100%
-------------------------------------------
TOTAL                       5      0   100%


====================================== 1 passed in 0.40s =======================================
```

Agora temos um teste que coletou 1 item (1 teste). Este teste foi aprovado e a cobertura abrangeu todas as linhas de código.

Como conseguimos coletar um item, o `post_test` foi executado e também gerou um HTML com a cobertura atualizada.

![Coverage Report with Test](https://fastapidozero.dunossauro.com/assets/02_navegador_com_pagina_de_cobertura_com_teste.png)

Certamente, aqui está o texto melhorado:

### Estrutura de um Teste

Agora que elaboramos nosso teste de forma intuitiva, é essencial compreender o propósito de cada etapa do teste. Essa compreensão é crucial, pois pode nos auxiliar a escrever testes no futuro com mais confiança e eficácia. Para entender o método por trás da nossa abordagem, vamos explorar a estratégia conhecida como AAA, que divide o teste em três fases distintas: Arrange, Act e Assert.

Vamos analisar o teste que desenvolvemos e compreender as etapas que tomamos para testar o endpoint:

```python
from fastapi.testclient import TestClient
from fast_zero.app import app

def test_root_deve_retornar_200_e_ola_mundo():
    client = TestClient(app)  # Arrange

    response = client.get('/')  # Act

    assert response.status_code == 200  # Assert
    assert response.json() == {'message': 'Olá Mundo!'}  # Assert
```

Com base neste código, podemos identificar as três fases:

Fase 1 - Preparação (Arrange)
Nesta etapa inicial, preparamos o ambiente para o teste. No exemplo, a linha com o comentário "Arrange" não é o próprio teste; ela configura o ambiente para a execução do teste. Estamos preparando um cliente de testes para fazer uma requisição à aplicação.

Fase 2 - Ação (Act)
Aqui ocorre a etapa principal do teste, que consiste em chamar o Sistema Sob Teste (SUT). No nosso caso, o SUT é a rota / e a ação é representada pela linha `response = client.get('/')`. Estamos exercitando a rota e armazenando a resposta na variável response. Nesta fase, o código de teste interage diretamente com a parte do sistema que queremos avaliar, a fim de observar seu comportamento.

Fase 3 - Verificação (Assert)
Esta etapa envolve a verificação se tudo ocorreu como esperado. É fácil identificar onde fazemos essa verificação, pois essa linha sempre contém a palavra reservada `assert`. A verificação é booleana; ou está correta ou não está. Portanto, um teste sempre deve incluir um `assert` para verificar se o comportamento esperado está correto.

Agora que compreendemos o propósito de cada linha de teste de forma específica, podemos nos orientar de maneira clara ao escrever testes no futuro. Cada uma das linhas usadas tem uma razão de ser no teste, e conhecer essa estrutura não apenas nos proporciona uma compreensão mais profunda do que estamos fazendo, mas também nos dá confiança para explorar e elaborar testes mais complexos.

```bash
# Comando para criar o .gitignore no projeto
ignr -p python > .gitignore
```

## Alembic

Instalando o Alembic, que é uma ferramenta de migração de banco de dados para SQLAlchemy.

```bash
poetry add alembic
```

Após a instalação do Alembic, precisamos iniciá-lo em nosso projeto.
O comando de inicialização criará um diretório migrations e um arquivo de configuração alembic.ini:
Comando:

```bash
alembic init migrations
```

Para criar a migração, utilizamos o seguinte comando:

```bash
alembic revision --autogenerate -m "create users table"
```

A flag "**--autogenerate**", busca informações do model para criar as migrations, por tanto se não que adicionar tudo que tem no model, use
com parcimônia

Para aplicar as migrações, usamos o comando upgrade do CLI Alembic.
O argumento head indica que queremos aplicar todas as migrações que ainda não foram aplicadas:

```bash
alembic upgrade head
```

## Autenticação e Autorização com JWT

### O que é um JWT

O JWT é um padrão (RFC 7519) que define uma maneira compacta e autônoma de transmitir informações entre as partes de maneira segura. Essas informações são transmitidas como um objeto JSON que é digitalmente assinado usando um segredo (com o algoritmo HMAC) ou um par de chaves pública/privada usando RSA, ou ECDSA.

Um JWT consiste em três partes:

1.Header: O cabeçalho do JWT consiste tipicamente em dois componentes: o tipo de token, que é JWT neste caso, e o algoritmo de assinatura, como HMAC SHA256 ou RSA. Essas informações são codificadas em Base64Url e formam a primeira parte do JWT.

```py
{
   "alg": "HS256",
   "typ": "JWT"
}
```

2.Payload: O payload de um JWT é onde as reivindicações (ou declarações) são armazenadas. As reivindicações são informações que queremos transmitir e que são relevantes para a interação entre o cliente e o servidor. As reivindicações são codificadas em Base64Url e formam a segunda parte do JWT.

```py
{
  "sub": "teste@test.com",
  "exp": 1690258153
}

```

3.Signature: A assinatura é utilizada para verificar que o remetente do JWT é quem afirma ser e para garantir que a mensagem não foi alterada ao longo do caminho. Para criar a assinatura, você precisa codificar o cabeçalho, o payload, e um segredo utilizando o algoritmo especificado no cabeçalho. A assinatura é a terceira parte do JWT. Uma assinatura de JWT pode ser criada como se segue:

```py
HMACSHA256(
    base64UrlEncode(header) + "." +
    base64UrlEncode(payload),
 nosso-segredo
)
```

Essas três partes são separadas por pontos (.) e juntas formam um token JWT.
Formando a estrutura: HEADER.PAYLOAD.SIGNATURE que formam um token

É importante ressaltar que, apesar de a informação em um JWT estar codificada, ela não está criptografada. Isso significa que qualquer pessoa com acesso ao token pode decodificar e ler as informações nele. No entanto, sem o segredo usado para assinar o token, eles não podem alterar as informações ou forjar um novo token. Portanto, não devemos incluir informações sensíveis ou confidenciais no payload do JWT.

### Como funciona o JWT

Em uma aplicação web, o processo de autenticação geralmente funciona da seguinte maneira:

1.O usuário envia suas credenciais (e-mail e senha) para o servidor em um endpoint de geração de token (/token por exemplo);
2.O servidor verifica as credenciais e, se estiverem corretas, gera um token JWT e o envia de volta ao cliente;
3.Nas solicitações subsequentes, o cliente deve incluir esse token no cabeçalho de autorização de suas solicitações. Como, por exemplo: Authorization: Bearer <token>;
4.Quando o servidor recebe uma solicitação com um token JWT, ele pode verificar a assinatura e se o token é válido e não expirou, ele processa a solicitação.

## Dockerizando a nossa aplicação

Docker é uma plataforma aberta que permite automatizar o processo de implantação,
escalonamento e operação de aplicações dentro de contêineres.
Ele serve para "empacotar" uma aplicação e suas dependências em um contêiner virtual que pode ser executado em qualquer sistema operacional que suporte Docker.
Isso facilita a implantação,
o desenvolvimento e o compartilhamento de aplicações,
além de proporcionar um ambiente isolado e consistente.

## Criando Dockerfile

Para criar um container Docker,
escrevemos uma lista de passos de como construir o ambiente para execução da nossa aplicação em um arquivo chamado Dockerfile.
Ele define o ambiente de execução,
os comandos necessários para preparar o ambiente e o comando a ser executado quando um contêiner é iniciado a partir da imagem.

Uma das coisas interessantes sobre Docker é que existe um Hub de containers prontos onde a comunidade hospeda imagens "prontas",
que podemos usar como ponto de partida. Por exemplo,
a comunidade de python mantém um grupo de imagens com o ambiente python pronto para uso.
Podemos partir dessa imagem com o python já instalado adicionar os passos para que nossa aplicação seja executada.

Aqui está um exemplo de Dockerfile para executar nossa aplicação:

```dockerfile
FROM python:3.11-slim
ENV POETRY_VIRTUALENVS_CREATE=false

WORKDIR app/
COPY . .

RUN pip install poetry

RUN poetry config installer.max-workers 10
RUN poetry install --no-interaction --no-ansi

EXPOSE 8000
CMD [ "poetry", "run", "uvicorn", "--host", "0.0.0.0", "fast_zero.app:app" ]
```

1. FROM python:3.11-slim: define a imagem base para nosso contêiner.
   Estamos usando a versão slim da imagem do Python 3.11,
   que tem tudo que precisamos para rodar nossa aplicação.

2. ENV POETRY_VIRTUALENVS_CREATE=false:
   define uma variável de ambiente que diz ao Poetry para não criar um ambiente virtual.
   (O container já é um ambiente isolado)

3. RUN pip install poetry: instala o Poetry,
   nosso gerenciador de pacotes.

4. WORKDIR app/: define o diretório em que executaremos os comandos a seguir.

5. COPY . .: copia todos os arquivos do diretório atual para o contêiner.

6. RUN poetry config installer.max-workers 10: configura o Poetry para usar até 10 workers ao instalar pacotes.

7. RUN poetry install --no-interaction --no-ansi: instala as dependências do nosso projeto sem interação e sem cores no output.

8. EXPOSE 8000: informa ao Docker que o contêiner escutará na porta 8000.

9. CMD [ "poetry", "run", "uvicorn", "--host", "0.0.0.0", "fast_zero.app:app" ]: define o comando que será executado quando o contêiner for iniciado.

Entendendo melhor esse último comando:

- poetry run define o comando que será executado dentro do ambiente virtual criado pelo Poetry.
- uvicorn é o servidor ASGI que usamos para rodar nossa aplicação.
- --host define o host que o servidor escutará. Especificamente, "0.0.0.0" é um endereço IP que permite que o servidor aceite conexões de qualquer endereço de rede disponível, tornando-o acessível externamente.
- fast_zero.app:app define o <módulo python>:<objeto> que o servidor executará.

## Ciando uma imagem no Docker

Para criar uma imagem Docker a partir do Dockerfile, usamos o comando docker build. O comando a seguir cria uma imagem chamada "fast_zero":

```bash
docker build -t "fast_zero" .
```

Este comando lê o Dockerfile no diretório atual (indicado pelo .) e cria uma imagem com a tag "fast_zero", (indicada pelo -t).

Então verificaremos se a imagem foi criada com sucesso usando o comando:

```bash
docker images
```

Este comando lista todas as imagens Docker disponíveis no seu sistema.
