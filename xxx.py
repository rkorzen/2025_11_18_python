
class LE:
    def __init__(self, value, next=None):
        self.value = value
        self.next = next

    def __str__(self):
        if self.next is None:
            return str(self.value)
        return f"{self.value} -> {self.next}"

def reverse(l: LE) -> LE:
    """
    Rekurencyjnie odwraca listę jednokierunkową.
    Zwraca nową głowę odwróconej listy.
    """
    # przypadek bazowy — lista pusta lub jednoelementowa
    if l is None or l.next is None:
        return l

    # odwrócenie reszty listy
    new_head = reverse(l.next)

    # odwrócenie wskaźników
    l.next.next = l
    l.next = None

    return new_head


def make_list(values):
    head = None
    for v in reversed(values):
        head = LE(v, head)
    return head


tests = [
    None,
    make_list(["a"]),
    make_list(["x", "y"]),
    make_list([0, 1, 2]),
    make_list([1, 2, 3, 4, 5]),
    make_list(["A", 42, 3.14]),
]

for t in tests:
    print("Przed :", t)
    print("Po    :", reverse(t))
    print("-" * 40)
