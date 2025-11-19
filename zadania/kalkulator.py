
operations = {}

def register(op):
    ...


@register("+")
def add(a: int, b: int, *args: int) -> int:
    """
    Oblicza sumę podanych liczb.

    :param a: Pierwszy składnik.
    :param b: Drugi składnik.
    :param args: Dodatkowe składniki.
    :return: Suma wszystkich podanych liczb.
    """
    return a + b + sum(args)


def sub(a: int, b: int) -> int:
    """
    Oblicza różnicę dwóch liczb.

    :param a: Odjemna.
    :param b: Odjemnik.
    :return: Wynik odejmowania b od a.
    """
    return a - b


def mul(a: int, b: int, *args: int) -> int:
    """
    Oblicza iloczyn podanych liczb.

    :param a: Pierwszy czynnik.
    :param b: Drugi czynnik.
    :param args: Dodatkowe czynniki.
    :return: Wynik mnożenia wszystkich podanych liczb.
    """
    result = a * b
    for arg in args:
        result *= arg
    return result


def div(a: int, b: int) -> None:
    """
    Oblicza iloraz dwóch liczb.

    :param a: Dzielna.
    :param b: Dzielnik.
    :return: Wynik dzielenia a przez b lub None, jeśli nastąpiła próba dzielenia przez zero.
    """
    if b == 0:
        return None
    return a / b


def get_additonal_data(op: str) -> list[int]:
    """
    Pobiera dodatkowe argumenty od użytkownika dla operacji dodawania i mnożenia.

    :param op: Symbol operacji matematycznej.
    :return: Lista dodatkowych liczb całkowitych pobranych od użytkownika.
    """
    args: list[int] = []
    if op in ["+", "*"]:
        while True:
            arg = input("Podaj kolejny arg lub enter by zakonczyc: ")
            if not arg:
                break
            args.append(int(arg))
    return args


def get_data_from_console() -> tuple[str, int, int, list[int]]:
    """
    Pobiera od użytkownika typ operacji oraz argumenty niezbędne do wykonania obliczeń.

    :return: Krotka zawierająca symbol operacji, dwa pierwsze argumenty oraz listę dodatkowych argumentów.
    """
    op = input("Podaj rodzaj operacji (+-/*): ")
    a = int(input("Podaj arg 1: "))
    b = int(input("Podaj arg 1: "))
    args = get_additonal_data(op)
    return op, a, b, args




def register(func, symbol):
    operations[symbol] = func
    return func


def make_additional_info(op: str, args: list[int]) -> str:
    """
    Tworzy tekstową reprezentację dodatkowych argumentów operacji.

    :param op: Symbol operacji.
    :param args: Lista dodatkowych argumentów.
    :return: Sformatowany ciąg znaków z operatorem i argumentami lub pusty ciąg.
    """
    text = ""
    if args:
        text = " " + op + " " + f" {op} ".join(map(str, args))
    return text


def calculate(op: str, a: int, b: int, *args: int) -> int | float | None:
    """
    Wykonuje operację matematyczną na podstawie przekazanego symbolu.

    :param op: Symbol operacji (+, -, *, /).
    :param a: Pierwszy argument.
    :param b: Drugi argument.
    :param args: Dodatkowe argumenty.
    :return: Wynik operacji matematycznej.
    """
    return operations[op](a, b, *args)


def main() -> None:
    """
    Główna funkcja programu obsługująca interakcję z użytkownikiem i wyświetlanie wyników.
    """
    op, a, b, args = get_data_from_console()
    result = calculate(op, a, b, *args)
    print(f"Wynik operacji {a} + {b}{make_additional_info(op, args)} = {result}")


register(add, "+")
register(sub, "-")
register(mul, "*")
register(div, "/")

print(dir())
# print(__name__)
if __name__ == "__main__":
    main()
