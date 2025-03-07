# Configuração de login personalizada

Estas são as opções personalizadas para configuração de login da plataforma.

$$note
Pode levar alguns minutos para refletir as alterações.
$$

A configuração a seguir é necessária para permitir que o OpenMetadata atualize as configurações de login.

$$section

### Máximo de tentativas de login sem sucesso $(id="maxLoginFailAttempts")

Tentativas de login com falha permitidas ao utilizador. Padrão: `3`.
$$

$$section

### Tempo de bloqueio de acesso $(id="accessBlockTime")

Tempo de bloqueio de acesso ao utilizador ao exceder tentativas com falha (em segundos). Padrão: `600`.
$$

$$section

### Tempo de expiração do token JWT $(id="jwtTokenExpiryTime")

Tempo de expiração do token Jwt para login em segundos. Padrão: `3600`.
$$