# Propriedade personalizada

O OpenMetadata suporta propriedades personalizadas nos ativos de dados.

$$section
### Nome $(id="name")

O nome deve começar com uma letra minúscula, como é preferível no formato camelCase. Letras maiúsculas e números podem ser incluídos no nome do campo; mas espaços, sublinhados e pontos não são suportados.
$$

$$section
### Nome de Exibição $(id="displayName")

Nome de exibição que identifica esta propriedade personalizada.
$$

$$section
### Tipo $(id="propertyType")

Selecione o Tipo de propriedade preferencial entre as opções fornecidas.
$$

$$section
### Descrição $(id="description")

Descreva a sua propriedade personalizada para fornecer mais informações à sua equipa.
$$

$$section
### Valores de enumeração $(id="enumConfig")

Adicione a lista de valores para a propriedade de enumeração.
$$

$$section
### Seleção múltipla $(id="multiSelect")

Ative a seleção múltipla de valores para a propriedade enum.
$$

$$section
### Formato $(id="formatConfig")

Para especificar um formato para o tipo `date` ou `dateTime`, por exemplo, pode usar o seguinte padrão: `dd-MM-aaaa` ou `dd-MM-aaaa HH:mm:ss`.
$$

**Formatos de data suportados**

- `aaaa-MM-dd`
- `dd MMM aaaa`
- `MM/dd/aaaa`
- `dd/MM/aaaa`
- `dd-MM-aaaa`
- `aaaaDDD`
- `d MMMM aaaa`

**Formatos de data e hora suportados**

- `MMM dd HH:mm:ss aaaa`
- `aaaa-MM-dd HH:mm:ss`
- `MM/dd/aaaa HH:mm:ss`
- `dd/MM/aaaa HH:mm:ss`
- `dd-MM-aaaa HH:mm:ss`
- `aaaa-MM-dd HH:mm:ss.SSS`
- `aaaa-MM-dd HH:mm:ss.SSSSSS`
- `dd MMMM aaaa HH:mm:ss`

**Formatos de hora suportados**

- `HH:mm:ss`

$$section
### Tipos de Referência de Entidade $(id="entityReferenceConfig")

Selecione o tipo de referência para seu tipo de valor de propriedade personalizado.
$$