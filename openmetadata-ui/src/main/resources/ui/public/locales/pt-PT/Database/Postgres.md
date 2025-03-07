# Postgres

Nesta seção, fornecemos guias e referências para usar o conector PostgreSQL.

## Requisitos

$$note
Note que o OpenMetadata apenas suporta versões oficialmente suportadas do Postgres. Pode verificar a lista de versões [aqui](https://www.postgresql.org/support/versioning/).
$$

### Profiler & Data Quality

Executing the profiler Workflow or data quality tests, will require the user to have `SELECT` permission on the tables/schemas where the profiler/tests will be executed. More information on the profiler workflow setup can be found [here](https://docs.open-metadata.org/how-to-guides/data-quality-observability/profiler/workflow) and data quality tests [here](https://docs.open-metadata.org/connectors/ingestion/workflows/data-quality).

### Linhagem & Uso

Ao extrair informações de linhagem e uso do Postgres, a pesquisa é feita com base na tabela `pg_stat_statements`. Pode encontrar mais informações sobre isso no [site oficial](https://www.postgresql.org/docs/current/pgstatstatements.html#id-1.11.7.39.6).

Outra consideração interessante aqui é explicada na seguinte [questão do StackOverflow](https://stackoverflow.com/questions/50803147/what-is-the-timeframe-for-pg-stat-statements).

Em resumo:
-A tabela `pg_stat_statements` não tem dados de tempo.
-Serão mostradas todas as consultas da última redefinição (pode-se chamar `pg_stat_statements_reset()`).

Então, ao extrair dados de uso e linhagem, a duração do log de consulta não terá impacto, apenas o limite de consulta.

-Para uso e linhagem, conceda a permissão   `pg_read_all_stats` ao seu utilizador.

```sql
GRANT pg_read_all_stats TO your_user;
```

Pode encontrar mais informações sobre o conector PostgrSQL na [documentação](https://docs.open-metadata.org/connectors/database/postgres).

## Detalhes de Ligação

$$section
### Esquema $(id="scheme")

Opções de esquema do driver SQLAlchemy.
$$

$$section
### Nome de Utilizador $(id="username")

Nome de utilizador para ligar-se ao Postgres. Este utilizador deve ter permissões para ler todos os metadados no Postgres.
$$


$$section
### Configuração de Autenticação $(id="authType")
Existem 3 tipos de configuração de Autenticação:
- Basic Auth.
- IAM based Auth.
- Azure based Auth.

O utilizador pode autenticar a instância de MySQL/Postgres com o tipo de autenticação `Basic Authentication` (ou seja, usando apenas a Palavra-passe) **ou** utilizando `IAM based Authentication` para se ligar aos serviços de AWS **ou** usando `Azure Based Authentication` para se ligar aos serviços de Azure.
$$

## Basic Auth
$$section
### Palavra-passe $(id="password")

Palavra-passe para ligar-se à base de dados em questão. 
$$

## IAM Auth Config

$$section
### ID da Chave de Acesso de AWS $(id="awsAccessKeyId")

Quando interage com AWS, especifica as suas credenciais de segurança de AWS para verificar a sua identidade e se tem permissão para aceder aos recursos que está a solicitar. AWS utiliza estas credenciais de segurança para autenticar e autorizar os seus pedidos ([documentação](https://docs.aws.amazon.com/IAM/latest/UserGuide/security-creds.html)).

As chaves de acesso consistem em duas partes:
1.Um ID de chave de acesso (por exemplo, `AKIAIOSFODNN7EXAMPLE`),
2.E uma chave secreta de acesso (por exemplo, `wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY`).

Deve usar tanto o ID da chave de acesso como a chave secreta de acesso em conjunto para autenticar os seus pedidos.

Pode encontrar mais informações sobre como gerir as suas chaves de acesso [aqui](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html).
$$

$$section
### Chave Secreta de Acesso de AWS $(id="awsSecretAccessKey")

Chave secreta de acesso (por exemplo, `wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY`).
$$

$$section
### Região de AWS $(id="awsRegion")

Cada Região de AWS é uma área geográfica separada onde AWS agrupa os seus centros de dados ([documentação](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Concepts.RegionsAndAvailabilityZones.html)).

Como AWS pode ter instâncias em várias regiões, é necessário saber a região à qual pertence o serviço que deseja se ligar.

Note que a Região de AWS é o único parâmetro obrigatório aquando a configuração de uma ligação. Ao ligar-se aos serviços programaticamente, existem diferentes maneiras de usar as configurações de AWS. Pode encontrar mais informações sobre como configurar as suas credenciais [aqui](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/credentials.html#configuring-credentials).
$$

$$section
### Token de Sessão de AWS $(id="awsSessionToken")

Se estiver a usar credenciais temporárias para aceder aos seus serviços, precisará de informar o ID da Chave de Acesso de AWS e a Chave Secreta de Acesso de AWS. Além disso, estas incluirão um Token de Sessão de AWS. 

Pode encontrar mais informações sobre [Usar credenciais temporárias com os recursos de AWS](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp_use-resources.html).
$$

$$section
###URL Endpoint$(id="endPointURL")

Para se ligar programaticamente a um serviço de AWS, utiliza-se um endpoint. Um *endpoint* é o URL do ponto de entrada para um serviço da web de AWS. Os SDKs e a Interface de Linha de Comando de AWS (AWS CLI) utilizam automaticamente o endpoint padrão para cada serviço numa região específica de AWS. No entanto, pode especificar um endpoint alternativo para as suas solicitações de API. 

Encontre mais informações sobre [Endpoints de serviços de AWS](https://docs.aws.amazon.com/general/latest/gr/rande.html).
$$

$$section
### Nome do Perfil $(id="profileName")

Um perfil nomeado é uma coleção de configurações e credenciais que se pode aplicar a um comando de AWS CLI. Quando se especifica um perfil para executar um comando, as configurações e credenciais desse perfil são utilizadas para executar o comando. Vários perfis nomeados podem ser guardados nos ficheiros de configuração e credenciais. 

Pode preencher este campo caso queira usar um perfil diferente de `default`.

Encontre mais informações sobre [Perfis nomeados para AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-profiles.html).
$$

$$section
### `AssumeRole` de ARN $(id="assumeRoleArn")

Geralmente, usa-se `AssumeRole` dentro da sua conta ou para acesso entre contas. Neste campo, definirá o `ARN` (Amazon Resource Name) da política da outra conta.

Um utilizador que deseja ter acesso a uma função de uma outra conta também deve ter permissões atribuídas pelo responsável/administrador dessa conta. O administrador deve adicionar uma política que permita ao utilizador chamar `AssumeRole` para o `ARN` da função na outra conta.

Este é um campo obrigatório se pretender `AssumeRole`.

Encontre mais informações [AssumeRole](https://docs.aws.amazon.com/STS/latest/APIReference/API_AssumeRole.html).
$$

$$section
### Nome de Sessão de AssumeRole $(id="assumeRoleSessionName")

Um identificador para a sessão da função assumida. Use o nome da sessão da função para identificar exclusivamente uma sessão quando a mesma função for assumida por diferentes principais ou por diferentes razões.

Por padrão, será usado o nome `OpenMetadataSession`.

Encontre mais informações [Nome da sessão de função](https://docs.aws.amazon.com/STS/latest/APIReference/API_AssumeRole.html#:~:text=An%20identifier%20for%20the%20assumed%20role%20session.).
$$

$$section
### Identidade de Origem da Função $(id="assumeRoleSourceIdentity")

A Identidade de Origem é a identidade do principal (utilizador, serviço, aplicação ou conta) que está a invocar a operação `AssumeRole` para assumir uma função. Esta informação pode ser utilizada nos logs do AWS CloudTrail para identificar de forma precisa quem ou o que executou ações utilizando a função.

Encontre mais informações [Source Identity](https://docs.aws.amazon.com/STS/latest/APIReference/API_AssumeRole.html#:~:text=Required%3A%20No-,SourceIdentity,-The%20source%20identity).
$$

## Azure Auth Config

$$section
### ID do Cliente $(id="clientId")

Este é um identificador único para a conta de serviço. Para obter esta chave, procure o valor associado à chave `client_id` no ficheiro da chave da conta de serviço.

$$

$$section
### Client Secret $(id="clientSecret")
Para obter  `client secret`, siga os seguintes passos:

1.Faça login no [Microsoft Azure](https://ms.portal.azure.com/#allservices).
2.Pesquise por `Registos de Aplicações` e selecione `Link de Registos de Aplicações`.
3.Selecione a aplicação `Azure AD` que está a ser usado para esta ligação.
4.Em `Gerir`, selecione `Certificados e segredos`.
5.Em `Client secrets`, selecione `Novo client secret`.
6.Na janela pop-up `Adicionar um client secret`, forneça uma descrição para o secret da sua aplicação. Escolha a data de expiração da aplicação e selecione `Adicionar`.
7.Na seção `Client secrets`, copie a string na coluna `Valor` do secret client recém-criado.

$$

$$section
### Tenant ID $(id="tenantId")

Para obter o tenant ID, siga estes passos:

1. Inicie sessão em [Microsoft Azure](https://ms.portal.azure.com/#allservices).
2. Pesquise por `Registo de Aplicações` e selecione `Link de Registos de Aplicações`.
3. Selecione a aplicação `Azure AD` que está a utilizar para o Power BI.
4. Na seção `Visão Geral`, copie o `ID do Diretório (Tenant ID)`.
$$

$$section
### Nome da Conta de Armazenamento $(id="accountName")

Nome da conta de armazenamento.

$$

$$section
### Nome do Cofre de Chaves $(id="vaultName")

Nome do cofre de chaves.
$$

$$section
### Âmbito $(id="scopes")

Para permitir que o OpenMetadata utilize as APIs de autenticação de Trino através da sua aplicação Azure AD, será necessário adicionar o âmbito:
1.Inicie sessão em [Microsoft Azure](https://ms.portal.azure.com/#allservices).
2.Pesquise por `Registo de Aplicações` e selecione `Link de Registos de Aplicações`.
3.Seleciona a aplicação `Azure AD` que está a utilizar para o Trino.
4.Na seção `Expôr uma API`, copie o `URI de ID da Aplicação`
5.Certifique-se de que o URI termina com `/.default`, caso contrário, adicione manualmente esta terminação.
$$

$$section
$$section
### Host Port $(id="hostPort")

Este parâmetro especifica Host e porta da instância de MySQL. Deve ser especificado como uma string no formato `hostname:port`. Exemplo:`localhost:5432`.

Se estiver a executar a ingestão do OpenMetadata num ambiente Docker e os seus serviços estiverem alojados no `localhost`, utilize então: `host.docker.internal:5432`.
$$

$$section
### Base de Dados $(id="database")

Base de dados Postgres à qual irá ligar-se.  Se pretende fazer ingestão todas as bases de dados, selecione a opção `ingestAllDatabases`.
$$

$$section
### Modo SSL $(id="sslMode")

Modo SSL para se ligar à base de dados PostgreSQL. Exemplos:  `prefer`, `verify-ca`, etc.

$$note
Se estiver a usar `IAM auth`, selecione `allow` (recomendado) ou outra opção, dependendo do seu caso de uso.
$$

$$section
### SSL CA $(id="caCertificate")
O SSL CA usado para validação SSL (`sslrootcert`).

$$note
Apenas Postgres necessita de CA Certificate.
$$
$$section
### Nome de Classificação $(id="classificationName")

Por padrão, as etiquetas no OpenMetadata são classificadas sob o nome `PostgresPolicyTags`. No entanto, você pode criar um nome de classificação personalizado de sua escolha para essas etiquetas. Depois de fazer ingestão dos dados do Postgres, o nome de classificação personalizado ficará visível na lista Classificações, sob a entidade Governar.
$$

$$section
### Fazer ingestão de todas bases de dados $(id="ingestAllDatabases")

Se pretende fazer ingestão todas as bases de dados, selecione a opção `ingestAllDatabases`. Caso contrário, o fluxo irá proceder à ingestão de apenas da base de dados indicada acima.
$$

$$section
### Opções de ligação $(id="connectionOptions")

Opções de ligação adicionais para criar o URL que pode ser enviado ao serviço durante a ligação.
$$

$$section
### Argumentos de ligação $(id="connectionArguments")

Argumentos de ligação adicionais, como configurações de segurança ou protocolo, que podem ser enviados ao serviço durante a ligação.
$$
