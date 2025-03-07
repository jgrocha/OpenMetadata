# Metadata

Configuração do fluxo de metadados do serviço de fluxos.

## Configuração

$$section

### Padrão de filtro do fluxo $(id="pipelineFilterPattern")

Os padrões de filtro do fluxo são usados ​​para controlar se os fluxos devem ser incluídos como parte da ingestão de metadados.

**Incluír**: Inclui explicitamente Fluxos adicionando uma lista de expressões regulares ao campo `Includes`. O OpenMetadata incluirá todos os Fluxos com nomes que correspondem a uma ou mais das expressões regulares fornecidas. Todos os outros Fluxos serão excluídos.

Por exemplo, para incluir apenas os Fluxos cujo nome começa com a palavra `demo`, adicione o padrão regex no campo de inclusão como `^demo.*`.

**Excluír**: Exclui explicitamente Fluxos adicionando uma lista de expressões regulares ao campo `Excludes`. O OpenMetadata excluirá todos os Fluxos com nomes que correspondam a uma ou mais das expressões regulares fornecidas. Todos os outros Fluxos serão incluídos.

Por exemplo, para excluir todos os Fluxos com o nome contendo a palavra `demo`, adicione o padrão regex no campo de exclusão como `.*demo.*`.

Veja este [documento](https://docs.open-metadata.org/connectors/ingestion/workflows/metadata/filter-patterns/database#database-filter-pattern) para mais exemplos.
$$

$$section
### Nome do Serviço de Base de dados $(id="dbServiceNames")

Ao processar Fluxos, podemos extrair informações sobre as tabelas de entrada e saída.

Para criar a linhagem entre as tabelas de entrada e saída, precisamos saber onde procurar por essas tabelas.

Pode inserir uma lista de Serviços de Bases de dados que contêm as tabelas de entrada e saída.
$$

$$section
### Ativar Logs de Debug $(id="enableDebugLog")

Selecione `Enable Debug Log` para ativar o debug no logging. Pode verificar esses logs no separador de Ingestão do serviço e aprofundar-se em qualquer erros que possa encontrar.
$$

$$section
### Incluír Linhagem $(id="includeLineage")

Selecione `Include Lineage` para controlar se a linhagem entre fluxos e fontes de dados deve ser incluída como parte da ingestão de metadados.
$$

$$section
### Incluír Etiquetas $(id="includeTags")

Selecione `Include tags` para controlar a inclusão de etiquetas durante a ingestão de metadados.
$$

$$section
### Incluír Fluxos não implementados $(id="includeUnDeployedPipelines")

Selecione 'Include UnDeployed Pipelines' para controlar se os fluxos não implementados devem ser incluídos como parte da ingestão de metadados.
$$

$$section
### Marcar Fluxos Apagados $(id="markDeletedPipeline")

Configuração opcional para um 'soft delete' de fluxos do OpneMetadata se a fonte dos mesmo estiver apagada. Depois de apagar, todas as entidades associadas a esse fluxo como linhagem, etc., serão apagadas.
$$

$$section
### Substituir Metadados $(id="overrideMetadata")

Selecione `Override Metadata` para controlar controlar se deve substituir os metadados existentes no servidor OpenMetadata pelos metadados obtidos da fonte.

Se a opção estiver `ativada`, os metadados obtidos da fonte substituirão os metadados existentes no OpenMetadata.

Se a opção estiver `desativada`, os metadados obtidos da fonte não substituirão os metadados existentes no servidor OpenMetadata. Nesse caso, os metadados serão atualizados apenas para campos que não têm valor adicionado no OpenMetadata.

Isso é aplicável para campos como descrição, etiquetas, proprietário e Nome de Exibição.

$$

$$section
### Número de tentativas $(id="retries")

Quantidade de vezes para repetir o fluxo de trabalho caso ele termine com uma falha.
$$