# MSSQL

Nesta seção, fornecemos guias e referências para usar o conector MSSQL.

## Requisitos

O utilizador deve ter permissões de `SELECT` para pesquisar os metadados de tabelas e views.

```sql
-- Create a new user
-- More details https://learn.microsoft.com/en-us/sql/t-sql/statements/create-user-transact-sql?view=sql-server-ver16
CREATE USER Mary WITH PASSWORD = '********';
-- Grant SELECT on table
GRANT SELECT TO Mary;
```

### Criador de perfil & Qualidade de Dados
Executar o fluxo de trabalho do Criador de perfil ou os testes de qualidade de dados, irá exigir que o utilizador tenha permissões de `SELECT` em tabelas/esquemas onde o criador de perfil/testes serão executados. Mais informações sobre o fluxo de trabalho do criador de perfil pode ser encontrado [aqui](https://docs.open-metadata.org/how-to-guides/data-quality-observability/profiler/workflow) e sobre os testes de qualidade de dados [aqui](https://docs.open-metadata.org/connectors/ingestion/workflows/data-quality).

### Uso & Linhagem
Para o fluxo de trabalho de uso e linhagem, o utilizador precisará de ter permissões de `SELECT` da tabela de privilégios. Pode encontrar mais informações sobre o fluxo de trabalho de uso [aqui](https://docs.open-metadata.org/connectors/ingestion/workflows/usage) e de linhagem  [aqui](https://docs.open-metadata.org/connectors/ingestion/workflows/lineage).

### Ligação Remota

#### 1. SQL Server em execução

Certifique-se de que o servidor SQL ao qual está a tentar ligar-se está em execução.

#### 2. Permitir ligação remota no MSSMS (Microsoft SQL Server Management Studio)

Esta etapa permite que o servidor SQL aceite pedidos de ligação remota.

![remote-connection](/doc-images/Database/Mssql/remote-connection.png)

#### 3. Configurar Firewall do Windows

Se estiver a usar o SQL Server no Windows, será necessário configurar o firewall no computador que executa o SQL Server para permitir o acesso.

1.No menu Iniciar, selecione `Executar`, digite `WF.msc` e selecione `OK`.
2.No `Firewall do Windows com Segurança Avançada`, no painel esquerdo, clique com o botão direito do rato em `Regras de Entrada` e selecione `Nova Regra` no painel de ações.
3.Na caixa de escrita `Tipo de regra`, selecione `Porta` e depois `Avançar`.
4.Na caixa de escrita `Protocolo e Portas`, selecione `TCP`. Selecione `Portas locais específicas` e, em seguida, digite o número da porta da instância do Database Engine, como 1433 para a instância padrão. Selecione `Avançar`.
5.Na caixa de escrita `Ação`, selecione `Permitir` a ligação e depois selecione `Avançar`.
6.Na caixa de escrita `Perfil`, selecione quaisquer perfis que descrevam o ambiente de ligação do computador para quando desejar ligar-se ao ambiente da Base de Dados e, em seguida, selecione `Avançar`.
7.Na caixa de escrita `Nome`, digite um nome e uma descrição para esta regra e selecione `Concluir`.

Para detalhes, consulte este [link](https://docs.microsoft.com/en-us/sql/database-engine/configure-windows/configure-a-windows-firewall-for-database-engine-access?view=sql-server-ver15).

Pode encontrar mais informações sobre o conector MSSQL na [documentação](https://docs.open-metadata.org/connectors/database/mssql).

## Detalhes de Ligação

$$section
### Esquema $(id="scheme")
Existem três esquemas com base na necessidade do utilizador de pesquisar dados no MSSQL:
- **mssql+pytds**: Biblioteca de código aberto de alto desempenho para ligação ao Microsoft SQL Server.
- **mssql+pyodbc**: Biblioteca Python multiplataforma que usa ODBC para se ligar ao Microsoft SQL Server.
- **mssql+pymssql**: Biblioteca Python que usa FreeTDS para se ligar ao Microsoft SQL Server, com suporte para transferência de dados em massa e tempos limite de consulta.

Se estiver a ligar-se via autenticação do Windows a partir do Docker Linux, use `mssql+pymssql`.

$$

$$section
### Nome de Utilizador $(id="username")

Nome de Utilizador para ligar-se ao  MSSQL. Este utilizador deverá ter permissões de leitura de todos os metadados de MSSQL.
$$

$$section
### Palavra-passe $(id="password")

Palavra-passe para ligar-se ao MSSQL.
$$

$$section
### Host Port $(id="hostPort")
Este parâmetro especifica Host e porta da instância de MSSQL. Deve ser especificado como uma string no formato `hostname:port`. Exemplo:`localhost:1433`.

Se estiver a executar a ingestão do OpenMetadata num ambiente Docker e os seus serviços estiverem alojados no `localhost`, utilize então: `host.docker.internal:1433`.
$$

$$section
### Base de Dados $(id="database")

Base de dados MSSQL inicial à qual irá ligar-se. Se pretende fazer ingestão de todas as bases de dados, selecione a opção `ingestAllDatabases`. 
$$

$$section
### Driver $(id="driver")

Ligar-se ao MSSQL via esquema **pyodbc** requer que o driver ODBC esteja instalado. Especifique o nome do driver ODBC no campo.
Pode descarregar o driver ODBC [aqui](https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server?view=sql-server-ver16).

No caso de estar a usar Docker ou Kubernetes, esse driver está incluído por defeito para uso com a versão `ODBC Driver 18 para SQL Server`.
$$


$$section
### Ingest All Databases $(id="ingestAllDatabases")

Se pretende faser ingestão de todas as bases de dados, selecione a opção `ingestAllDatabases`. Caso contrário, o fluxo irá proceder à ingestão de apenas da base de dados indicada acima.
$$


$$section
### Opções de ligação $(id="connectionOptions")

Opções de ligação adicionais para criar o URL que pode ser enviado ao serviço durante a ligação.
$$

$$section
### Argumentos de ligação $(id="connectionArguments")

Argumentos de ligação adicionais, como configurações de segurança ou protocolo, que podem ser enviados ao serviço durante a ligação. Esses detalhes devem ser adiconados em par chave-valor.

Ao ligar-se ao MSSQL via esquema **pyodbc** são necessários os argumentos de ligação `Encrypt: No` e `TrustServerCertificate: Yes`.
$$
