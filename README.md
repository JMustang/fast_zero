# Tutorial de Python com FastAPI

## Baseado no tutorial do **dunossauro**.

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

Acesse http://localhost:8000 no seu navegador e você deve ver a mensagem "Olá Mundo!" no formato JSON.

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

### Escrevendo o teste

Agora, vamos escrever nosso primeiro teste com Pytest.

Para testar o FastAPI, precisamos de um cliente de teste. Isso pode ser obtido no módulo fastapi.testclient com o objeto TestClient, que precisa receber nosso app como parâmetro:

```py
# crie uma arquivo no diretorio tests
# tests/test_app.py
# E adicione o codigo
from fastapi.testclient import TestClient
from fast_zero.app import app

client = TestClient(app)
```

Só o fato de termos definido um cliente, já nos mostra uma cobertura bastante diferente.

execute o comando task test, no terminal:

```bash
task test
```

se apresentar algum erro de formatação execute, task format novamente,
em seguida execute o teste.

```bash
---------- coverage: platform darwin, python 3.11.2-final-0 ----------
Name                    Stmts   Miss  Cover
-------------------------------------------
fast_zero/__init__.py       0      0   100%
fast_zero/app.py            5      1    80%
-------------------------------------------
TOTAL                       5      1    80%
```

Devido ao fato de não ter coletado nenhum teste, o pytest ainda retornou um "erro". Para ver a cobertura, precisaremos executar novamente o post_test manualmente:

vamos executar novamente o comando task post_test:

```bash
task post_test
```

No navegador, podemos ver que a única linha não "testada" é aquela onde temos a lógica do endpoint:

![Alt text](https://fastapidozero.dunossauro.com/assets/02_navegador_com_pagina_de_cobertura_com_estrutuda_de_testes.png)

No verde vemos o que foi executado quando chamamos o teste, no vermelho o que não foi.

Para resolver isso, temos que criar um teste de fato, fazendo uma chamada para nossa API usando o cliente de teste que definimos:

```py
from fastapi.testclient import TestClient

from fast_zero.app import app

def test_root_deve_retornar_200_e_ola_mundo():
    client = TestClient(app)
    response = client.get('/')

    assert response.status_code == 200
    assert response.json() == {'message': 'Olá Mundo!'}
```

Esse teste faz uma requisição GET no endpoint / e verifica se o código de status da resposta é 200 e se o conteúdo da resposta é {'message': 'Olá Mundo!'}.

uma mensagem como essa deve ser apresentada:

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

Dessa forma, temos um teste que coletou 1 item (1 teste). Esse teste foi aprovado e a cobertura não deixou de abranger nenhuma linha de código.

Como conseguimos coletar um item, o post_test foi executado e também gerou um HTML com a cobertura atualizada.

![Alt text](https://fastapidozero.dunossauro.com/assets/02_navegador_com_pagina_de_cobertura_com_teste.png)
