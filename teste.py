"""
Bateria de testes das máscaras de validação (mascaras.py).

Cada caso é uma tripla (cadeia, esperado, motivo):
    esperado = ACEITA  (A) -> a cadeia deve pertencer à linguagem do campo
    esperado = REJEITA (R) -> a cadeia NÃO deve pertencer à linguagem
    motivo   = justificativa curta, útil para a seção de testes do relatório

Uso:
    python testes.py              -> tabela com todos os campos
    python testes.py cpf          -> tabela só do campo indicado
    python -m unittest testes -v  -> mesma bateria no formato unittest
"""

import sys
import unittest

from mascaras import MASCARAS, valida

A = True    # a cadeia deve ser aceita
R = False   # a cadeia deve ser rejeitada

CASOS = {
    # ------------------------------------------------------------------
    "nome": [
        ("Alan Turing",      A, "exemplo do enunciado"),
        ("Noam Chomsky",     A, "exemplo do enunciado"),
        ("Ada Lovelace",     A, "exemplo do enunciado"),
        ("Maria Silva",      A, "nome comum, iniciais maiúsculas"),
        ("A B",              A, "menor cadeia válida: uma maiúscula em cada parte"),
        ("Alan",             R, "exemplo do enunciado: falta o sobrenome"),
        ("1Alan",            R, "exemplo do enunciado: começa com dígito"),
        ("A1an",             R, "exemplo do enunciado: dígito no meio do nome"),
        ("alan Turing",      R, "nome começa com minúscula"),
        ("Alan turing",      R, "sobrenome começa com minúscula"),
        ("ALan Turing",      R, "maiúscula no meio do nome"),
        ("Alan TUring",      R, "maiúscula no meio do sobrenome"),
        ("Alan  Turing",     R, "dois espaços entre nome e sobrenome"),
        (" Alan Turing",     R, "espaço no início"),
        ("Alan Turing ",     R, "espaço no fim"),
        ("Alan\tTuring",     R, "tabulação no lugar do espaço"),
        ("Alan Turing Jr",   R, "três partes; o enunciado pede só nome e sobrenome"),
        ("Alan-Turing",      R, "hífen no lugar do espaço"),
        ("Alan Turing!",     R, "caractere especial"),
        ("Alan T1uring",     R, "dígito no sobrenome"),
        ("José Silva",       R, "letra acentuada fora do alfabeto Σ"),
        ("Alan Turing\n",    R, "quebra de linha no fim (padrão com $ aceitaria)"),
        ("",                 R, "cadeia vazia"),
    ],
    # ------------------------------------------------------------------
    "email": [
        ("a@a.br",           A, "exemplo do enunciado: menor e-mail válido"),
        ("divulga@ufpa.br",  A, "exemplo do enunciado"),
        ("usuario@dominio.br", A, "caso comum"),
        ("contato@empresa.br", A, "caso comum"),
        ("a@a.com.br",       A, "subnível .com antes de .br (padrão da introdução)"),
        ("aluno@ufpa.edu.br", A, "domínio com dois subníveis antes de .br"),
        ("@",                R, "exemplo do enunciado: só o arroba"),
        ("a@.br",            R, "exemplo do enunciado: nada entre @ e .br"),
        ("T@teste.br",       R, "exemplo do enunciado: maiúscula fora de Σ"),
        ("@a.br",            R, "começa com @"),
        ("a@@a.br",          R, "dois arrobas seguidos"),
        ("a@b@c.br",         R, "dois arrobas separados"),
        ("aa.br",            R, "sem arroba"),
        ("a@a.com",          R, "não termina em .br"),
        ("a@a..br",          R, "dois pontos seguidos no domínio"),
        ("a@.a.br",          R, "ponto logo depois do @"),
        ("a@abr",            R, "falta o ponto antes de br"),
        ("a@a.BR",           R, "sufixo em maiúsculas"),
        ("a@a,br",           R, "vírgula no lugar do ponto"),
        ("a b@a.br",         R, "espaço no meio"),
        ("a1@a.br",          R, "dígito antes do @"),
        ("a@a1.br",          R, "dígito depois do @"),
        ("a_b@a.br",         R, "sublinhado fora de Σ"),
        ("a.b@a.br",         R, "ponto antes do @"),
        ("a@a.br ",          R, "espaço no fim"),
        ("a@a.br\n",         R, "quebra de linha no fim"),
        ("",                 R, "cadeia vazia"),
    ],
    # ------------------------------------------------------------------
    "senha": [
        ("518R2r5e",         A, "exemplo do enunciado"),
        ("F123456A",         A, "exemplo do enunciado"),
        ("1234567T",         A, "exemplo do enunciado: maiúscula no fim"),
        ("ropsSoq0",         A, "exemplo do enunciado: dígito no fim"),
        ("Abcdefg1",         A, "uma maiúscula, um dígito, resto minúsculo"),
        ("A1234567",         A, "maiúscula no início, resto dígitos"),
        ("a1B2c3D4",         A, "alternando as três classes"),
        ("AAAAAAA1",         A, "só maiúsculas mais um dígito"),
        ("F1234567A",        R, "exemplo do enunciado: 9 símbolos"),
        ("abcdefgH",         R, "exemplo do enunciado: sem dígito"),
        ("1234567HI",        R, "exemplo do enunciado: 9 símbolos"),
        ("abcdefg1",         R, "sem maiúscula"),
        ("12345678",         R, "sem maiúscula (só dígitos)"),
        ("ABCDEFGH",         R, "sem dígito (só maiúsculas)"),
        ("abcdefgh",         R, "sem maiúscula e sem dígito"),
        ("Abc1",             R, "curta: 4 símbolos"),
        ("Abcdef1",          R, "7 símbolos"),
        ("Abcdefg12",        R, "9 símbolos"),
        ("Abcdef1!",         R, "caractere especial na 8ª posição"),
        ("Abc def1",         R, "espaço dentro da senha"),
        ("Abcdéfg1",         R, "letra acentuada fora do alfabeto"),
        ("Abcdef1\n",        R, "quebra de linha ocupando a 8ª posição"),
        ("",                 R, "cadeia vazia"),
    ],
    # ------------------------------------------------------------------
    "cpf": [
        ("123.456.789-09",   A, "exemplo do enunciado"),
        ("000.000.000-00",   A, "exemplo do enunciado: só zeros (valida só o formato)"),
        ("999.999.999-99",   A, "só noves; dígitos verificadores não são conferidos"),
        ("111.222.333-44",   A, "grupos distintos"),
        ("123.456.789-0",    R, "exemplo do enunciado: falta o último dígito"),
        ("111.111.11-11",    R, "exemplo do enunciado: grupo com 2 dígitos"),
        ("12345678909",      R, "sem pontuação"),
        ("123.456.789.09",   R, "ponto no lugar do hífen"),
        ("123-456-789.09",   R, "separadores trocados"),
        ("123.456.789-099",  R, "dígito extra no fim"),
        ("1234.56.789-09",   R, "grupos com tamanhos errados"),
        ("abc.def.ghi-jk",   R, "letras no lugar de dígitos"),
        ("123.456.789-0a",   R, "letra no último dígito"),
        ("123,456,789-09",   R, "vírgulas no lugar dos pontos"),
        (" 123.456.789-09",  R, "espaço no início"),
        ("123.456.789 -09",  R, "espaço antes do hífen"),
        ("123.456.789-",     R, "faltam os dois dígitos finais"),
        ("",                 R, "cadeia vazia"),
    ],
    # ------------------------------------------------------------------
    "telefone": [
        ("(91) 99999-9999",  A, "exemplo do enunciado: formato (xx) 9xxxx-xxxx"),
        ("(91) 999999999",   A, "exemplo do enunciado: formato (xx) 9xxxxxxxx"),
        ("91 999999999",     A, "exemplo do enunciado: formato xx 9xxxxxxxx"),
        ("(11) 98765-4321",  A, "formato 1 com outro DDD"),
        ("(21) 912345678",   A, "formato 2 com outro DDD"),
        ("00 900000000",     A, "formato 3; a máscara não verifica se o DDD existe"),
        ("(91) 59999-9999",  R, "exemplo do enunciado: não começa com 9"),
        ("99 99999-9999",    R, "exemplo do enunciado: hífen no formato sem parênteses"),
        ("(94)95555-5555",   R, "exemplo do enunciado: falta o espaço após ')'"),
        ("(91) 99999-999",   R, "um dígito a menos"),
        ("(91) 99999-99999", R, "um dígito a mais"),
        ("(91) 9999-9999",   R, "falta o nono dígito"),
        ("(91) 9999999999",  R, "um dígito a mais, sem hífen"),
        ("91999999999",      R, "sem espaço separador"),
        ("(91 999999999",    R, "parêntese aberto sem fechar"),
        ("91) 999999999",    R, "parêntese fechado sem abrir"),
        ("(9) 999999999",    R, "DDD com um dígito"),
        ("(091) 999999999",  R, "DDD com três dígitos"),
        ("(91)  99999-9999", R, "dois espaços após o parêntese"),
        ("(91) 99999 9999",  R, "espaço no lugar do hífen"),
        ("(91) 999999-999",  R, "hífen na posição errada"),
        ("(91) 99999-9999 ", R, "espaço no fim"),
        ("(ab) 999999999",   R, "letras no DDD"),
        ("",                 R, "cadeia vazia"),
    ],
}


# --------------------------------------------------------------------------
# Execução em tabela no console
# --------------------------------------------------------------------------

def rotulo(aceita: bool) -> str:
    return "ACEITA" if aceita else "REJEITADA"


def executa(campos: list[str]) -> int:
    total = acertos = 0
    for campo in campos:
        casos = CASOS[campo]
        largura = max(len(repr(t)) for t, _, _ in casos) + 2
        print(f"\n=== {campo.upper()} ===")
        print(f"  {'cadeia':<{largura}}{'esperado':<12}{'obtido':<12}"
              f"{'situacao':<10}motivo")
        ok_campo = 0
        for texto, esperado, motivo in casos:
            obtido = valida(campo, texto)
            ok = obtido == esperado
            ok_campo += ok
            print(f"  {texto!r:<{largura}}{rotulo(esperado):<12}"
                  f"{rotulo(obtido):<12}{'OK' if ok else 'ERRO':<10}{motivo}")
        n_ace = sum(1 for _, e, _ in casos if e)
        print(f"  -> {campo}: {ok_campo}/{len(casos)} conforme o esperado "
              f"({n_ace} aceitas, {len(casos) - n_ace} rejeitadas)")
        total += len(casos)
        acertos += ok_campo
    print(f"\nRESUMO GERAL: {acertos}/{total} casos conforme o esperado.")
    return 0 if acertos == total else 1


# --------------------------------------------------------------------------
# Mesma bateria no formato unittest
# --------------------------------------------------------------------------

class TestMascaras(unittest.TestCase):
    def test_todos_os_casos(self):
        for campo, casos in CASOS.items():
            for texto, esperado, motivo in casos:
                with self.subTest(campo=campo, texto=texto):
                    self.assertEqual(valida(campo, texto), esperado, motivo)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        sys.exit(executa(list(CASOS)))
    if len(sys.argv) == 2 and sys.argv[1] in MASCARAS:
        sys.exit(executa([sys.argv[1]]))
    print(f"Uso: python {sys.argv[0]} [{'|'.join(MASCARAS)}]")
    sys.exit(2)