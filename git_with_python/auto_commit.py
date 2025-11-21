# pip install GitPython

from git import Repo
from datetime import datetime
from pathlib import Path


def ensure_upstream(repo: Repo):
    branch = repo.active_branch
    origin = repo.remote("origin")

    if branch.tracking_branch() is None:
        print(f"Brak upstreamu dla {branch.name}, ustawiam...")
        origin.push(refspec=f"{branch.name}:{branch.name}")
        repo.git.branch("-u", f"origin/{branch.name}", branch.name)
        print(f"Upstream ustawiony: origin/{branch.name}")


def auto_commit_reports(repo_path: str = ".", reports_dir: str = "reports"):
    repo = Repo(repo_path)
    assert not repo.bare

    ensure_upstream(repo)

    reports_path = Path(repo_path) / reports_dir
    if not reports_path.exists():
        print("Brak katalogu reports/")
        return

    # 🚀 1. Upewnij się, że katalog jest śledzony
    # (dodaje katalog nawet jeśli jest untracked)
    repo.git.add(reports_dir)

    # 🚀 2. Zbierz wszystkie pliki
    to_add = [str(p) for p in reports_path.rglob("*") if p.is_file()]
    if not to_add:
        print("Brak plików w katalogu reports/")
        return

    # 🚀 3. Dodaj indywidualne pliki
    repo.index.add(to_add)

    # Zapis indexu
    repo.index.write()

    # 🚀 4. Sprawdź, czy są zmiany
    if not repo.is_dirty(index=True, working_tree=True):
        print("Brak zmian — nic do commitowania.")
        return

    msg = f"[auto] Update reports {datetime.now():%Y-%m-%d %H:%M}"
    commit = repo.index.commit(msg)
    print("Commit:", commit.hexsha)

    repo.remote("origin").push()
    print("Zmiany wypchnięte.")


if __name__ == "__main__":
    auto_commit_reports()