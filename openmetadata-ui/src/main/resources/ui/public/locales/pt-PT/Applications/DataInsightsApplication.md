# Configuração da Aplicação Data Insights

Este esquema define a configuração da aplicação Data Insights.

$$section
### Tipo de Aplicação $(id="type")

Tipo de aplicação

$$

$$section
### Tamanho do Lote $(id="batchSize")

Número máximo de eventos processados de cada vez (Padrão: 100).
$$

$$section
### Recriar o Índice de Ativos de Dados do Data Insights $(id="recreateDataAssetsIndex")

Recria o índice de Ativos de Dados no Data Insights. Útil caso tenha alterado um Tipo de Propriedade Personalizada e esteja a ter erros. Tenha em mente que a recriação do índice irá eliminar os seus Ativos de Dados, sendo necessário um processo de backfill.

$$

$$section
### Configuração backfill $(id="backfillConfiguration")

Verdadeiro ou Falso, para controlar se a configuração backfill está ativada.

$$