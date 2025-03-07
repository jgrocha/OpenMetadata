# Configuração da Aplicação Search Indexing

Este esquema define a configuração da aplicação de Reindexação de Pesquisa.

$$section
### Tamanho do lote $(id="batchSize")

Número máximo de entidades de eventos em um lote (padrão 100).

$$

$$section
### Tamanho da carga útil $(id="payLoadSize")

Número máximo de entidades de eventos em um lote (padrão 100).

$$

$$section
### Número de processos do produtor $(id="producerThreads")

Número de processos a serem usados ​​para reindexação.

$$

$$section
### Número de processos do consumidor $(id="consumerThreads")

Número de processos a serem usados ​​para reindexação.

$$

$$section
### Tamanho da fila a ser usado. $(id="queueSize")

Tamanho da fila a ser usado internamente para reindexação.

$$

$$section
### Máximo de solicitações simultâneas $(id="maxConcurrentRequests")

Número máximo de solicitações simultâneas para o índice de pesquisa.

$$

$$section
### Máximo de tentativas $(id="maxRetries")

Número máximo de tentativas para uma solicitação com falha.

$$

$$section
### Backoff inicial em milissegundos $(id="initialBackoff")

Tempo de backoff inicial em milissegundos.

$$

$$section
### Máximo de backoff em milissegundos $(id="maxBackoff")

Tempo máximo de backoff em milissegundos.

$$

$$section
### Entidades $(id="entities")

Lista de entidades que precisa reindexar.

$$

$$section
### Recriar índices $(id="recreateIndex")

$$

$$section
### Idioma do índice de pesquisa $(id="searchIndexMappingLanguage")

Recriar índices com idioma atualizado.

$$