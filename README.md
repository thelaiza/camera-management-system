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


**O projeto segue uma arquitetura monolítica, onde o back-end e o front-end se comunicam diretamente, sem a necessidade de serviços independentes.**
- Simplicidade na implementação: Não exige a complexidade de microserviços
- Facilidade de manutenção: Todo o código está concentrado em um único repositório, tornando a depuração e a atualização mais simples
- Menor sobrecarga: Como o sistema não precisa escalar para múltiplos servidores ou serviços independentes, um monólito é mais eficiente nesse projeto
- Tempo de desenvolvimento reduzido: Como o foco é apresentar um sistema funcional, essa abordagem permite um desenvolvimento mais rápido


| Atividade                     | Responsável  | Prazo       |
|-------------------------------|--------------|--------------|
| Levantamento de requisitos	  | Laíza        | 11/03/2025   |
| Definição da arquitetura      | Laíza        | 11/03/2025   |
| Configuração do repositório   | Laíza        | 25/02/2025   |
| Criação do banco              | Laíza        | 31/03/2025   |
| Desenvolvimento do backend    | Laíza        | 30/04/2025   |
| Desenvolvimento do frontend   | Laíza        | 15/05/2025   |
| Testes e ajustes finais       | Laíza        | 30/05/2025   |

