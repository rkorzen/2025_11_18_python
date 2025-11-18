
# **Treść zadania (Python)**

Napisz w Pythonie funkcję **rekurencyjną**, która odwraca kolejność elementów w **jednokierunkowej liście wiązanej (singly linked list)**.
Funkcja powinna przyjmować obiekt reprezentujący początek listy i zwracać nową głowę odwróconej listy.

Do reprezentacji elementu listy użyj następującej klasy:

```python
class LE:
    def __init__(self, value, next=None):
        self.value = value
        self.next = next

    def __str__(self):
        if self.next is None:
            return str(self.value)
        return f"{self.value} -> {self.next}"
```

Napisz funkcję:

```python
def reverse(l: LE) -> LE:
    """
    Rekurencyjnie odwraca listę jednokierunkową.
    Zwraca nową głowę odwróconej listy.
    """
```

---

# **Twoje zadanie — część 2**

Wypisz **wszystkie przypadki testowe w formie list**, np.:

```
a -> b -> c
```

jakie uważasz, że są **konieczne do pełnego przetestowania funkcji rekurencyjnego odwracania jednokierunkowej listy**.

---

# **Wymagane minimalne przypadki testowe (podpowiedź)**

Poprawne testy powinny obejmować co najmniej:

1. **Lista pusta**

   ```
   None
   ```

2. **Lista jednoelementowa**

   ```
   a
   ```

3. **Lista dwuelementowa**

   ```
   x -> y
   ```

4. **Klasyczna lista trójelementowa**

   ```
   0 -> 1 -> 2
   ```

5. **Lista dłuższa, np. pięcioelementowa**

   ```
   1 -> 2 -> 3 -> 4 -> 5
   ```

6. **Lista z elementami różnych typów**

   ```
   "A" -> 42 -> 3.14
   ```

Każdy przypadek należy przetestować tak, aby program wypisał:

* listę przed odwróceniem,
* listę po odwróceniu.

