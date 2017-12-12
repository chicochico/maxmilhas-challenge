# MaxMilhas Challenge
This is my solution for the challenge proposed by MaxMilhas company.


## Instruções do teste

Desenvolva uma aplicação em linguagem Python que seja acessível localmente e verifique se um determinado número de CPF está em uma Blacklist. A aplicação deve:

* [x] Ser acessível como serviço através de um endpoint e retorne a situação, por exemplo: http://127.0.0.1:5000/consulta?cpf=00000000000

* [ ] Ser acessível via browser e oferecer um formulário para consulta apresentando FREE se o CPF não estiver na Blacklist, BLOCK se o CPF estiver na Blacklist e exibir opções para inclusão e remoção em ambos os cenários.

* [x] Aceitar uma rota de suporte (exemplo: http://127.0.0.1:5000/status) retornando as informações de uptime do servidor, quantidade de consultas realizadas desde o último restart e quantidade de CPFs na blacklist.

## Requisitos obrigatórios
 - As chamadas diretas ao endpoint devem retornar em formato JSON.
 - Validação do CPF/máscara na consulta e inclusão.
 - Utilização da linguagem e framework/pacotes Python na construção dos recursos.
 - Criação de um arquivo README descrevendo as dependências e a estrutura do projeto.
 - Utilização de containers Docker para construção do ambiente (incluir Dockerfile e qualquer outra dependência para execução no projeto).

## Requisitos opcionais/provocações
 - Criação de testes unitários.
 - Utilização de banco de dados embutido.
 - Adição de outras rotas/funcionalidades que agreguem valor ao projeto.
 - Tratamento de mensagens de erro.
