# MaxMilhas Challenge
This is my solution for the challenge proposed by MaxMilhas company.

## Challenge
Build a blacklist to store CPFs (Cadastro De Pessoa Fisica) that is a number that identify Brazillian taxpayers.
  - The application should provide REST API to query a blacklist and check if a CPF is blacklisted.
  - A view to:
    - query the blacklist
    - Add a CPF to the blacklist
    - Remove a CPF from the blacklist
  - Endpoint with server information:
    - uptime
    - number of blacklist queries
    - number of CPFs in the blacklist

## Solution
It was used Django as a framework to build a solution that is organized into three apps:
  - **cpf**: Contains models, validation and formating methods for CPF
  - **api**: Provide endpoints that allow interaction with the app
  - **cpf_site**: Implement a view to allow interaction with the app on a webbrowser

### API
API endpoints:

|   cpf-blacklist   | path                                 | description                                         |
|:-----------------:|--------------------------------------|-----------------------------------------------------|
|        GET        | /api/v1/cpf-blacklist/               | Lists all the CPFs in the blacklist                 |
|        POST       | /api/v1/cpf-blacklist/               | Insert a CPF to the blacklist (provides validation) |
|        GET        | /api/v1/cpf-blacklist/check-cpf/     | Check if a CPF is in the blacklist                  |
|       DELETE      | /api/v1/cpf-blacklist/{cpf__number}/ | Remove a CPF from the blacklist                     |
|        GET        | /api/v1/cpf-blacklist/{cpf__number}/ | Get a single instance of a CPF in the blacklist     |

|   server-status    | path                                | description                                         |
|:-----------------:|--------------------------------------|-----------------------------------------------------|
|        GET        | /api/v1/server-status/               | View server information                             |

For the full interactive API documentation run the app and go [here](http://localhost:8000/api/v1/docs/).

### Running
To run the app make sure you have [Docker](https://docs.docker.com/engine/installation/) and [Docker-compose](https://docs.docker.com/compose/install/) installed.

  1. clone this repo
  2. cd into the root of this project
  3. `docker-compose up`
  4. done! open a webbrowser and go [here](http://localhost:8000)
  5. optionally you can create a admin user to interact with admin pages:

      - `docker-compose run web ./manage.py createsuperuser` and follow the instructions

#### Running Tests
Running tests: `docker-compose run web ./manage.py test`

### Modeling
A model CPF store the number, it also contains CPF validation and formating methods. Another model CPFBlacklist stores a one to one relationship with CPF, it also includes a timestamp of the time the CPF number was blacklisted.

Using a single model with a boolean field to represent if it is blacklisted or not was considered, but since CPF usually represents a person, and may have other related information (that may be added in the future), it was decided that is best not no mix the two domains, and that also allows for extra information related to blacklist to be stored for example a timestamp.

### Tools
  - [Django](https://www.djangoproject.com/): Python web framework
  - [Django-REST](http://www.django-rest-framework.org/): Django plugin for building REST APIs
  - [Django-REST-Swagger](http://marcgibbons.com/django-rest-swagger/): Documentation generator for Django-REST APIs
  - [Django-Bootstrap3](https://django-bootstrap3.readthedocs.io/en/latest/): Tranform django templates into Bootsprap code
  - [Postgresql](https://www.postgresql.org/): Relational database


## Original challenge instructions
### Instruções do teste

Desenvolva uma aplicação em linguagem Python que seja acessível localmente e verifique se um determinado número de CPF está em uma Blacklist. A aplicação deve:

  - [x] Ser acessível como serviço através de um endpoint e retorne a situação, por exemplo: http://127.0.0.1:5000/consulta?cpf=00000000000
  - [x] Ser acessível via browser e oferecer um formulário para consulta apresentando FREE se o CPF não estiver na Blacklist, BLOCK se o CPF estiver na Blacklist e exibir opções para inclusão e remoção em ambos os cenários.
  - [x] Aceitar uma rota de suporte (exemplo: http://127.0.0.1:5000/status) retornando as informações de uptime do servidor, quantidade de consultas realizadas desde o último restart e quantidade de CPFs na blacklist.

### Requisitos obrigatórios
  - As chamadas diretas ao endpoint devem retornar em formato JSON.
  - Validação do CPF/máscara na consulta e inclusão.
  - Utilização da linguagem e framework/pacotes Python na construção dos recursos.
  - Criação de um arquivo README descrevendo as dependências e a estrutura do projeto.
  - Utilização de containers Docker para construção do ambiente (incluir Dockerfile e qualquer outra dependência para execução no projeto).

### Requisitos opcionais/provocações
  - Criação de testes unitários.
  - Utilização de banco de dados embutido.
  - Adição de outras rotas/funcionalidades que agreguem valor ao projeto.
  - Tratamento de mensagens de erro.
