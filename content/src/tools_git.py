"""Тема «Git».

Задания — по модулям в _git_m1.py … _git_m3.py, теория — в theory_tools_git.py
(она собирает _git_t1.py … _git_t3.py)."""
from ._lib import topic
from ._git_m1 import m1
from ._git_m2 import m2
from ._git_m3 import m3

TOPIC = topic("tools-git", "Git", "🌿", "#f05033",
              "init и clone, status, add и commit, log и diff, .gitignore, ветки, merge и конфликты, push/pull/fetch, pull request, restore/reset/revert, stash, rebase, cherry-pick, теги, blame, bisect",
              m1, m2, m3, group="Инструменты")
