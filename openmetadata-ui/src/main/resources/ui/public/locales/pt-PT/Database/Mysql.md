# MySQL

Nesta seção, fornecemos guias e referências para usar o conector MySQL.

## Requisitos
Para extrair metadados, o nome de utilizador usado na ligação precisa ter acesso ao `INFORMATION_SCHEMA`. Por padrão, um utilizador pode ver apenas as linhas no `INFORMATION_SCHEMA` que correspondem a objetos para os quais o utilizador tem os privilégios de acesso adequados.

```SQL
-- Create user. If <hostName> is ommited, defaults to '%'
-- More details https://dev.mysql.com/doc/refman/8.0/en/create-user.html
CREATE USER '<username>'[@'<hostName>'] IDENTIFIED BY '<password>';

-- Grant select on a database
GRANT SELECT ON world.* TO '<username>';

-- Grant select on a database
GRANT SELECT ON world.* TO '<username>';

-- Grant select on a specific object
GRANT SELECT ON world.hello TO '<username>';
```

$$note
OpenMetadata suporta a versão `8.0.0` e acima de MySQL. 
$$

### Linhagem & Uso 
Para extrair a linhagem e o uso, é preciso ativar o registo de consulta no MySQL e o nome de utilizador usado na ligação necessita ter acesso ao `mysql.general_log`.

```sql
-- Enable Logging 
SET GLOBAL general_log='ON';
set GLOBAL log_output='table';

-- Grant SELECT on log table
GRANT SELECT ON mysql.general_log TO '<username>'@'<host>';
```

### Criador de Perfil & Qualidade de dados
Executar o fluxo de trabalho do Criador de perfil ou os testes de qualidade de dados, irá exigir que o utilizador tenha permissões de `SELECT` em tabelas/esquemas onde o criador de perfil/testes serão executados. O utilizador deve também ter permissões de ver informação em `tables` para todos os objetos da base de dados. Mais informações sobre o fluxo de trabalho do criador de perfil pode ser encontrado [aqui](https://docs.open-metadata.org/how-to-guides/data-quality-observability/profiler/workflow) e sobre os testes de qualidade de dados [aqui](https://docs.open-metadata.org/connectors/ingestion/workflows/data-quality).

Pode encontrar mais informações sobre o conector MySQL na [documentação](https://docs.open-metadata.org/connectors/database/mysql).

## Detalhes de Ligação

$$section
### Esquema $(id="scheme")

Opções de esquema do driver SQLAlchemy. Se não tiver certeza sobre essa configuração, pode usar o valor padrão.
$$

$$section
### Nome de Utilizador $(id="username")
Nome de utilizador para ligar-se ao MySQL. Este utilizador deve ter acesso ao `INFORMATION_SCHEMA` para extrair metadados. Outros fluxos de trabalho podem exigir permissões diferentes -- consulte a seção acima para obter mais informações.
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

$$note 
Se estiver a usar IAM auth, adicione <br />`"ssl": {"ssl-mode": "allow"}` em Argumentos de Ligação.
$$

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
### Host Port $(id="hostPort")

Este parâmetro especifica Host e porta da instância de MySQL. Deve ser especificado como uma string no formato `hostname:port`. Exemplo:`localhost:3306`.

Se estiver a executar a ingestão do OpenMetadata num ambiente Docker e os seus serviços estiverem alojados no `localhost`, utilize então: `host.docker.internal:3306`.
$$

$$section
$$section
### Nome da Base de Dados $(id="databaseName")
No OpenMetadata, a hierarquia do serviço de base de dados funciona da seguinte maneira:
```
Serviço da Base de Dados > Base de Dados > Esquema > Tabela
```
No caso de MySQL, não teremos uma Base de Dados como tal. Se quiser ver os seus dados em numa base de dados com um nome diferente de `default`, pode especificar o nome neste campo.
$$
$$

$$section
### Esquema da Base de Dados $(id="databaseSchema")
Esquema MySQL que contém as tabelas do Airflow. Este é um parâmetro opcional. Quando definido, o valor será usado para restringir a leitura de metadados a uma única base de dados (correspondente ao valor passado neste campo). Quando deixado em branco, o OpenMetadata analisará todas as bases de dados.
$$

$$section
### Certificado CA $(id="caCertificate")
O certificado CA usado para validação SSL (`ssl_ca`).
$$

$$section
### SSL Certificate $(id="sslCertificate")
O certificado SSL usado para autenticação do cliente (`ssl_cert`).
$$

$$section
### SSL Key $(id="sslKey")
A chave privada associada ao certificado SSL (`ssl_key`).
$$

$$section
### Opções de ligação $(id="connectionOptions")

Opções de ligação adicionais para criar o URL que pode ser enviado ao serviço durante a ligação.
$$

$$section
### Argumentos de ligação $(id="connectionArguments")

Argumentos de ligação adicionais, como configurações de segurança ou protocolo, que podem ser enviados ao serviço durante a ligação. Esses detalhes devem ser adiconados em par chave-valor.
$$
