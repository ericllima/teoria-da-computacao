# Máscaras de Validação com Expressões Regulares

Trabalho da disciplina **Teoria da Computação** (PPGCC/UFPA). Validação de cinco campos de formulário (nome, e-mail, senha, CPF e telefone) por meio de expressões regulares em Python.

## Arquivos

| Arquivo | Conteúdo |
|---|---|
| `mascaras.py` | As cinco máscaras, a função `valida` e uso pela linha de comando |
| `testes.py` | 115 casos de teste (aceitos e rejeitados), cada um com o motivo |

## Requisitos

Python 3.9 ou superior. Não há dependências externas: só módulos da biblioteca padrão (`re`, `sys`, `unittest`).

## Uso

Pela linha de comando, passando o campo e a cadeia entre aspas:

```
python mascaras.py cpf "123.456.789-09"
python mascaras.py email "T@teste.br"
```

```
[cpf] '123.456.789-09': ACEITA
[email] 'T@teste.br': REJEITADA
```

Os campos disponíveis são `nome`, `email`, `senha`, `cpf` e `telefone`. Sem argumentos, o programa mostra a instrução de uso.

Como módulo:

```python
from mascaras import valida_cpf

valida_cpf("123.456.789-09")   # True
valida_cpf("123.456.789-0")    # False
```

## Testes

```
python testes.py                 # tabela com todos os campos
python testes.py cpf             # apenas um campo
python -m unittest testes -v     # mesma bateria no formato unittest
```

Resultado esperado: `RESUMO GERAL: 115/115 casos conforme o esperado.`

## Regras de cada campo

| Campo | Regra |
|---|---|
| Nome | Nome e sobrenome separados por um espaço; inicial maiúscula e demais letras minúsculas |
| E-mail | Letras minúsculas, um único `@`, ao menos uma letra antes e depois dele, subníveis opcionais separados por ponto (como `.com.br`), terminando em `.br` |
| Senha | Exatamente 8 símbolos entre letras e dígitos, com ao menos uma maiúscula e um dígito |
| CPF | Formato `xxx.xxx.xxx-xx`, com `x` sendo dígito |
| Telefone | `(xx) 9xxxx-xxxx`, `(xx) 9xxxxxxxx` ou `xx 9xxxxxxxx`, com `x` sendo dígito |

## Decisões de projeto

- **`fullmatch`:** a cadeia inteira precisa pertencer à linguagem, sem aceitar sobras no início ou no fim.
- **`[0-9]` em vez de `\d`:** em Python 3, `\d` aceita dígitos de outros sistemas de escrita, o que fugiria do alfabeto N.
- **CPF:** valida só o formato, sem conferir os dígitos verificadores.
- **E-mail:** aceita subníveis no domínio (como `.com.br`), pois o enunciado só exige terminar em `.br`. Já `.com` sozinho é rejeitado, porque a regra do campo manda terminar em `.br`.
- **Alfabetos estritos:** nomes com acento são rejeitados, conforme os alfabetos Σ e Γ definidos no enunciado.