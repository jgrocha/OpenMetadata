# Configuração de e-mail

O OpenMetadata tem capacidade de enviar e-mails em várias etapas, como Inscrição, Esqueceu a palavra-passe, Redefinir palavra-passe, Alterar atualizações de eventos.

A configuração a seguir é necessária para permitir que o OpenMetadata envie e-mails.

$$section

### Nome de Utilizador $(id="username")

Nome de utilizador da conta SMTP.
$$

$$section

### Palavra-passe $(id="password")

Palavra-passe a ser usada com o nome de utilizador para enviar e-mails.
$$

$$section

### E-mail do Remetente $(id="senderEmail")

E-mail do remetente (pode ser o mesmo que `username`, mas no Amazon SES pode ser diferente)
$$

$$section

### Endpoint do Servidor $(id="serverEndpoint")

Endpoint do servidor SMTP (Ex. smtp.gmail.com)
$$

$$section

### Porta do Servidor SMTP $(id="serverPort")

Porta do servidor SMTP, isso depende da estratégia de transmissão abaixo.
A seguir está o mapeamento entre a porta e a estratégia de transmissão.

**SMTP:**- Se a porta SMTP for 25, use isto

**SMTPS:**- Se a porta SMTP for 465, use isto

**SMTP_TLS:**- Se a porta SMTP for 587, use isto
$$

$$section

### Entidade de e-mail $(id="emailingEntity")

Isto define a entidade que vai enviar o e-mail. Por padrão, é `OpenMetadata`.

Se o nome da sua organização for `JohnDoe`, configurá-lo atualizará a linha de assunto, a linha de conteúdo para que os e-mails tenham `JohnDoe` no lugar de `OpenMetadata`.

$$

$$section

### Ativar servidor SMTP $(id="enableSmtpServer")

Verdadeiro ou Falso, para controlar se a configuração SMTP está ativada.
$$

$$section

### URL de Apoio $(id="supportUrl")

Nos e-mails é criado um link de URL de apoio para permitir aos utilizadores o contactarem em caso de problemas.

Se tiver os seus canais/grupos internos, isso pode ser atualizado aqui.

Padrão: `https://slack.open-metadata.org`.

$$

$$section

### Estratégia de transmissão $(id="transportationStrategy")

Valores possíveis: `SMTP`, `SMTPS`, `SMTP_TLS`. Depende de acordo com a `porta` acima.

$$