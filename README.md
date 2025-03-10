# Sistema de Monitoramento de Câmeras

## Proposta de Escopo

Este projeto tem como objetivo o desenvolvimento de um **Sistema de Monitoramento de Câmeras** que permitirá aos usuários gerenciar suas câmeras de segurança através de funcionalidades de **cadastro**, **remoção** e **visualização de logs** de transações. O sistema registrará as ações realizadas, como a adição e remoção de câmeras, e permitirá que cada usuário visualize as câmeras associadas ao seu login.

## Objetivos principais

- **Cadastro de Câmeras**: Implementar uma funcionalidade para adicionar novas câmeras ao sistema, com informações como nome, localização e outros dados relevantes.
- **Remoção de Câmeras**: Desenvolver uma interface para excluir câmeras cadastradas.
- **Logs de Transações**: Registrar logs de todas as ações realizadas, incluindo a adição e remoção de câmeras, com dados como data, hora e usuário responsável pela ação.
- **Visualização de Câmeras por Usuário**: Implementar uma funcionalidade que permita que os usuários visualizem quantas câmeras estão associadas ao seu login.
- **Autenticação de Usuários**: Garantir que cada usuário tenha acesso restrito apenas às câmeras que ele cadastrou, por meio de um sistema de login seguro.


## Tecnologias a serem utilizadas

- **Frontend**: React
- **Backend**: Python com Django
- **Banco de Dados**: MySQL (usando MySQL Workbench para gerenciamento)
- **Autenticação**: JWT (JSON Web Tokens) para controle de sessão e autenticação de usuários
- **Outros**: Git, GitHub, Insomnia e Django REST Framework (extensão do Django para a criação de APIs RESTful) para comunicação entre frontend e backend

## Requisitos funcionais e não funcionais 

- RF1: O sistema deve permitir o cadastro de novas câmeras
- RF2: O sistema deve listar todas as câmeras cadastradas
- RF3: O sistema deve permitir a atualização das informações das câmeras
- RF4: O sistema deve permitir a remoção de câmeras cadastradas
- RF5: O sistema deve permitir o cadastro de usuários
- RF6: O sistema deve permitir que os usuários realizem login
- RF7: O sistema deve listar todos os usuários cadastrados
- RF8: O sistema deve permitir a edição das informações dos usuários
- RF9: O sistema deve permitir a exclusão de usuários
- RF10: O sistema deve registrar logs de eventos e ações realizadas
- RF11: O sistema deve permitir a visualização do histórico de alterações

- RNF1: O sistema deve permitir múltiplos usuários simultâneos sem perda de desempenho significativo
- RNF2: O sistema deve armazenar logs de atividades para auditoria e rastreamento de ações
- RNF3: O sistema deve permitir a recuperação de dados em caso de falhas ou erros críticos
- RNF4: O sistema deve suportar autenticação e controle de permissões para diferentes tipos de usuários
- RNF5: O sistema deve oferecer uma interface responsiva para funcionamento em diferentes tamanhos de tela

**O projeto segue uma arquitetura monolítica, onde o back-end e o front-end se comunicam diretamente, sem a necessidade de serviços independentes.**
- Simplicidade na implementação: Não exige a complexidade de microserviços
- Facilidade de manutenção: Todo o código está concentrado em um único repositório, tornando a depuração e a atualização mais simples
- Menor sobrecarga: Como o sistema não precisa escalar para múltiplos servidores ou serviços independentes, um monólito é mais eficiente nesse projeto
- Tempo de desenvolvimento reduzido: Como o foco é apresentar um sistema funcional, essa abordagem permite um desenvolvimento mais rápido


Atividade	Responsável	Status	Prazo
Levantamento de requisitos	[Seu Nome]	Concluído	[Data]
Definição da arquitetura	[Seu Nome]	Concluído	[Data]
Configuração do repositório GitHub	[Seu Nome]	Concluído	[Data]
Desenvolvimento do backend (Django)	[Seu Nome]	Em andamento	[Data]
Desenvolvimento do frontend (React)	[Seu Nome]	Em andamento	[Data]
Integração frontend e backend	[Seu Nome]	Pendente	[Data]
Implementação do banco de dados	[Seu Nome]	Em andamento	[Data]
Testes e ajustes finais	[Seu Nome]	Pendente	[Data]
Documentação do projeto	[Seu Nome]	Pendente	[Data]
Apresentação do projeto	[Seu Nome]	Pendente	[Data]

| Atividade                     | Responsável  | Status       | Prazo       |
|-------------------------------|--------------|--------------|--------------|
| Levantamento de requisitos	  | Laíza        | Concluído    | 11/03/2025   |
| Definição da arquitetura      | Laíza        | Concluído    | 11/03/2025   |
| Configuração do repositório   | Laíza        | Concluído    | 25/02/2025   |
| Criação do banco              | Laíza        | Em andamento | 31/03/2025   |
| Desenvolvimento do backend    | Laíza        | Em andamento | 30/04/2025   |
| Desenvolvimento do frontend   | Laíza        | Pendente     | 15/05/2025   |
| Testes e ajustes finais       | Laíza        | Pendente     | 30/05/2025   |

