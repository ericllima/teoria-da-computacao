"""
Máscaras de validação por expressões regulares.

Disciplina: Teoria da Computação (PPGCC/UFPA)

Alfabetos considerados:
    Σ = {a, ..., z}   ->  [a-z]
    Γ = {A, ..., Z}   ->  [A-Z]
    N = {0, ..., 9}   ->  [0-9]

Observações de implementação:
    * Usa-se [0-9] em vez de \\d porque, em Python 3, \\d casa dígitos
      Unicode de outros sistemas de escrita, o que extrapolaria o alfabeto N.
    * Usa-se fullmatch, que exige que a cadeia INTEIRA pertença à linguagem
      (equivale a ancorar o padrão com ^ e \\Z).
"""

import re

# --------------------------------------------------------------------------
# Padrões (um por campo)
# --------------------------------------------------------------------------

# Nome: Γ Σ* ' ' Γ Σ*   (nome e sobrenome não vazios, separados por 1 espaço)
NOME = re.compile(r"[A-Z][a-z]* [A-Z][a-z]*")

# E-mail: Σ+ '@' Σ+ '.br'!
EMAIL = re.compile(r"[a-z]+@[a-z]+(\.[a-z]+)*\.br")

# Senha: tamanho 8 sobre Σ ∪ Γ ∪ N, com pelo menos um Γ e pelo menos um N.
# Os lookaheads (?=...) verificam as duas exigências sem consumir símbolos;
# em seguida, [A-Za-z0-9]{8} impõe o alfabeto e o comprimento.
SENHA = re.compile(r"(?=.*[A-Z])(?=.*[0-9])[A-Za-z0-9]{8}")

# CPF: xxx.xxx.xxx-xx, com x ∈ N (apenas o formato, sem dígitos verificadores)
CPF = re.compile(r"[0-9]{3}\.[0-9]{3}\.[0-9]{3}-[0-9]{2}")

# Telefone: três formatos possíveis, com x ∈ N
#   (xx) 9xxxx-xxxx  |  (xx) 9xxxxxxxx  |  xx 9xxxxxxxx
TELEFONE = re.compile(
    r"\([0-9]{2}\) 9[0-9]{4}-[0-9]{4}"
    r"|\([0-9]{2}\) 9[0-9]{8}"
    r"|[0-9]{2} 9[0-9]{8}"
)

MASCARAS = {
    "nome": NOME,
    "email": EMAIL,
    "senha": SENHA,
    "cpf": CPF,
    "telefone": TELEFONE,
}


# --------------------------------------------------------------------------
# Funções de validação
# --------------------------------------------------------------------------

def valida(campo: str, texto: str) -> bool:
    """Retorna True se `texto` pertence à linguagem do `campo`."""
    return MASCARAS[campo].fullmatch(texto) is not None


def valida_nome(texto: str) -> bool:
    return valida("nome", texto)


def valida_email(texto: str) -> bool:
    return valida("email", texto)


def valida_senha(texto: str) -> bool:
    return valida("senha", texto)


def valida_cpf(texto: str) -> bool:
    return valida("cpf", texto)


def valida_telefone(texto: str) -> bool:
    return valida("telefone", texto)


# --------------------------------------------------------------------------
# Uso pela linha de comando:  python mascaras.py <campo> "<texto>"
# --------------------------------------------------------------------------

def main(argv: list[str]) -> int:
    if len(argv) != 3 or argv[1] not in MASCARAS:
        print(f"Uso: python {argv[0]} <{'|'.join(MASCARAS)}> \"<texto>\"")
        return 2
    campo, texto = argv[1], argv[2]
    ok = valida(campo, texto)
    print(f"[{campo}] {texto!r}: {'ACEITA' if ok else 'REJEITADA'}")
    return 0 if ok else 1