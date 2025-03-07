# SQLite

Nesta seção, fornecemos guias e referências para usar o conector SQLite.

## Requirements

Pode encontrar mais informações sobre o conector SQLite na [documentação](https://docs.open-metadata.org/connectors/database/sqlite).

## Detalhes de ligação

$$section
### Esquema $(id="scheme")

Opções de esquema do driver SQLAlchemy.
$$

$$section
### Nome de Utilizador $(id="username")

Nome de Utilizador para ligar-se ao SQLite. Deixe em branco caso seja uma base de dados em memória.
$$

$$section
### Palavra-passe $(id="password")

Palavra-passe para ligar-se ao SQLite.. Deixe em branco caso seja uma base de dados em memória.
$$

$$section
### Host e Porta $(id="hostPort")

Este parâmetro especifica o host e a porta da instância SQLite. Deve ser definido como uma string no formato `hostname:port`. Por exemplo, `localhost:3306`.

Se estiver a executar a ingestão do OpenMetadata num ambiente Docker e os seus serviços estiverem alojados no `localhost`, utilize então: `host.docker.internal:3306`.

Deixe em branco para bases de dados em memória.
$$

$$section
### Base de Dados $(id="database")

Base de dados da fonte de dados. Este é um parâmetro opcional que permite restringir a leitura de metadados a uma única base de dados. Se deixado em branco, a ingestão do OpenMetadata vai tentar analisar todas as bases de dados.
$$

$$section
### Modo de Base de Dados $(id="databaseMode")

Como executar a base de dados SQLite. Por defeito é `:memory:` .
$$

$$section
### Opções de ligação $(id="connectionOptions")

Opções de ligação adicionais para criar o URL que pode ser enviado ao serviço durante a ligação.
$$

$$section
### Argumentos de ligação $(id="connectionArguments")

Argumentos de ligação adicionais, como configurações de segurança ou protocolo, que podem ser enviados ao serviço durante a ligação.
$$