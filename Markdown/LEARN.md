# 🎓 Git Education Guide

Welcome to the **Git Learning Module**! This guide is designed to take you from a beginner to a confident user of version control.

---

## 1. What is Git?
Git is a **distributed version control system**. It tracks changes in your source code during software development.
*   **Version Control**: Saves snapshots of your project history. You can revert to any previous state.
*   **Distributed**: Every developer has a full copy of the codebase history.

---

## 2. Basic Commands (The Daily Drivers)

These are the commands you'll use 90% of the time.

### `git init`
Initializes a new Git repository.
```bash
git init
```

### `git status`
Checks the state of your working directory. Shows which files are staged, modified, or untracked.
```bash
git status
```

### `git add`
Stages changes for the next commit.
```bash
git add .          # Stages all changes
git add file.py    # Stages a specific file
```

### `git commit`
Saves your staged changes to the repository history.
```bash
git commit -m "feat: added login functionality"
```
> **Tip**: Write clear, descriptive commit messages. start with a verb (Added, Fixed, Updated).

### `git push`
Uploads your local commits to a remote repository (like GitHub).
```bash
git push origin main
```

### `git pull`
Downloads changes from the remote repository and merges them into your local branch.
```bash
git pull origin main
```

---

## 3. Branching & Merging (Parallel Development)

Branches allow you to work on new features without breaking the main code.

### Create a Branch
```bash
git checkout -b feature/new-ui
```

### Switch Branch
```bash
git checkout main
```

### Merge a Branch
To merge `feature/new-ui` into `main`:
1.  Switch to main: `git checkout main`
2.  Merge: `git merge feature/new-ui`

---

## 4. Best Practices

1.  **Commit Often**: Small, frequent commits are easier to manage than massive ones.
2.  **Use Branches**: Never work directly on `main` for complex features.
3.  **Pull Before Push**: rapid changes happen. Always pull the latest code before pushing yours to avoid conflicts.
4.  **Ignore Garbage**: Always use a `.gitignore` file to exclude `venv`, `.env`, and `__pycache__`.

---

## 5. Cheat Sheet

| Command | Action |
| :--- | :--- |
| `git clone <url>` | Download a repo |
| `git log` | View commit history |
| `git diff` | Show file differences |
| `git reset` | Unstage files |
| `git stash` | Temporarily save changes |

Happy Coding! 🚀
