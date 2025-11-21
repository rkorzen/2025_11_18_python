
# 🚀 **1. Co to jest webhook? (najprostsze możliwe wyjaśnienie)**

**Webhook = powiadomienie wysyłane przez GitHub / GitLab / Bitbucket do Twojej aplikacji, gdy coś się wydarzy w repo.**

Tak samo jak:

* SMS przychodzący do telefonu,
* powiadomienie push w aplikacji,
* event w systemie.

💡 **Webhook = “hej, coś się zmieniło w repo, zrób z tym coś!”**

---

# 📌 **2. Po co są webhooki?**

Umożliwiają automatyzację.

Np.:

### ✔️ automatyczne CI (uruchamiasz testy po każdym push)

### ✔️ automatyczny deploy (gdy push na main)

### ✔️ generowanie changelogów

### ✔️ aktualizacja dokumentacji

### ✔️ powiadomienia Slack / Discord / e-mail

### ✔️ synchronizacja z innymi systemami (np. JIRA)

Webhook jest **eventem**, a Ty piszesz **serwer**, który ten event obsłuży.

---

# 📌 **3. Co wysyła GitHub?**

Kiedy ktoś zrobi `git push`, GitHub robi:

```
POST https://twoja-aplikacja.com/webhook
Content-Type: application/json

{
    "ref": "refs/heads/main",
    "repository": { ... },
    "commits": [ ... ]
}
```

czyli wysyła **JSON z informacją o zdarzeniu**.

---

# 📌 **4. Czym jest “ta aplikacja” w Pythonie?**

To po prostu **mały serwer HTTP**, który:

* nasłuchuje na porcie (np. 8000),
* odbiera webhooka,
* robi jakieś działanie.

Możemy go napisać:

* w **FastAPI**
* w **Flask**
* w **Django**
* lub w czystym Pythonie (ale odradzam)

FastAPI jest najwygodniejsze, dlatego użyłem go w przykładach.

---

# 📌 **5. Minimalny przykład – serwer webhooków (FastAPI)**

To jest dosłownie **najmniejsza możliwa aplikacja webhookowa**:

```python
from fastapi import FastAPI, Request

app = FastAPI()

@app.post("/webhook")
async def webhook(request: Request):
    payload = await request.json()
    print("Webhook received:", payload)
    return {"status": "ok"}
```

---

# 📌 **6. Jak ją uruchomić?**

W terminalu:

```
uvicorn webhook_server:app --reload --port 8000
```

Serwer działa na:

```
http://localhost:8000/webhook
```

---

# 📌 **7. Jak GitHub ma wywołać ten endpoint?**

GitHub musi widzieć Twój serwer.
Lokalnie **nie działa**, bo GitHub nie ma dostępu do Twojego laptopa.

Dlatego używa się **ngrok**:

```
ngrok http 8000
```

I dostaniesz publiczny URL, np.:

```
https://92ac-83-3-204-140.ngrok-free.app
```

Wtedy w GitHub → Settings → Webhooks → Add webhook:

* **Payload URL:**
  `https://92ac-83-3-204-140.ngrok-free.app/webhook`
* Content type: `application/json`
* Secret: `co chcesz`
* Events: Push event

Klikasz **Add**.

---

# 📌 **8. Teraz, gdy zrobisz:**

```
git push
```

GitHub robi:

```
POST https://twój-ngrok/webhook
```

A Twój terminal z FastAPI wypisze:

```
Webhook received: {...}
```

---

# 📌 **9. To wszystko!**

Teraz możesz w kodzie zrobić cokolwiek:

* uruchomić testy
* napisać commit
* wysłać powiadomienie
* pobrać dodatkowe pliki z repo
* wykonać deploy

Webhook to tylko **wyzwalacz**, a Ty decydujesz co robi aplikacja.

---

# 🧠 **10. Przykład naprawdę praktyczny: uruchamianie testów po pushu**

```python
import subprocess
from fastapi import FastAPI, Request

app = FastAPI()

@app.post("/ci")
async def ci(request: Request):
    payload = await request.json()

    print("Received push, running tests...")

    result = subprocess.run(["pytest", "-q"], capture_output=True, text=True)

    print("Tests output:")
    print(result.stdout)

    return {"tests_passed": result.returncode == 0}
```

GitHub push → Twój serwer dostaje webhook → uruchamia pytest.

Gratulacje, właśnie napisałeś mini-CI 😎

---

# 📌 **11. Jeszcze prościej: co to daje?**

Webhook = **kiedy cokolwiek dzieje się w repo, Twoja aplikacja dostaje o tym info w czasie rzeczywistym.**
Bez pollingów, cronów, zapytań API.

Z tą jedną rzeczą możesz zautomatyzować naprawdę wszystko.

---

