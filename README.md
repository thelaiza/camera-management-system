# Sistema de Monitoramento de Câmeras

## Proposta de Escopo

Este projeto tem como objetivo o desenvolvimento de um **Sistema de Monitoramento de Câmeras** que permitirá aos usuários gerenciar suas câmeras de segurança através de funcionalidades de **cadastro**, **remoção** e **visualização de logs** de transações. O sistema registrará as ações realizadas, como a adição e remoção de câmeras, e permitirá que cada usuário visualize as câmeras associadas ao seu login.

## Objetivos Principais

- **Cadastro de Câmeras**: Implementar uma funcionalidade para adicionar novas câmeras ao sistema, com informações como nome, localização e outros dados relevantes.
- **Remoção de Câmeras**: Desenvolver uma interface para excluir câmeras cadastradas.
- **Logs de Transações**: Registrar logs de todas as ações realizadas, incluindo a adição e remoção de câmeras, com dados como data, hora e usuário responsável pela ação.
- **Visualização de Câmeras por Usuário**: Implementar uma funcionalidade que permita que os usuários visualizem quantas câmeras estão associadas ao seu login.
- **Autenticação de Usuários**: Garantir que cada usuário tenha acesso restrito apenas às câmeras que ele cadastrou, por meio de um sistema de login seguro.

## Funcionalidades Previstas

- **Cadastro de Câmeras**: Interface para o usuário cadastrar informações detalhadas sobre as câmeras.
- **Remoção de Câmeras**: Funcionalidade para excluir câmeras do sistema de maneira simples e rápida.
- **Logs de Transações**: Sistema de registro de atividades (como adição e remoção de câmeras), com acompanhamento de data, hora e usuário.
- **Visualização de Câmeras**: Usuários poderão consultar a quantidade de câmeras cadastradas em sua conta e acessar suas informações.
- **Autenticação de Usuário**: Sistema de autenticação usando **JWT** (JSON Web Tokens) para garantir que apenas usuários autenticados possam acessar as funcionalidades de cadastro e remoção de câmeras.

## Tecnologias a Serem Utilizadas

- **Frontend**: React
- **Backend**: Python com Django
- **Banco de Dados**: MySQL (usando MySQL Workbench para gerenciamento)
- **Autenticação**: JWT (JSON Web Tokens) para controle de sessão e autenticação de usuários
- **Outros**: Git, GitHub, Insomnia e Django REST Framework (extensão do Django para a criação de APIs RESTful) para comunicação entre frontend e backend


