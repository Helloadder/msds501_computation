# MSDS 501 – Day 2 Exercise: Git + Error Handling

Welcome! This repo is the starting point for the **Day 2 hands-on workflow** in MSDS 501 (Computation for Data Science) at USF.

## What's in here

| File | Assigned to |
|------|-------------|
| `partner_a.py` | Partner A |
| `partner_b.py` | Partner B |

Both scripts have an intentional bug — a `ValueError` that crashes when the code tries to convert a bad string to a number. Your job is to find it, understand it, and fix it with `try/except`.

## The workflow (Tasks 0–5)

**Task 0 – Setup** (start of class)
- Git installed (`git --version` in your terminal)
- GitHub account at github.com
- Decide your pair. **One person** forks this repo: click **Fork** in the top-right corner of this page
- Forker: go to your fork → **Settings → Collaborators** → invite your partner's GitHub username
- Partner: accept the collaborator invite (check your email or github.com/notifications)
- Both of you clone the **same** URL (the forker's fork):

**Task 1 – Clone & Open**
```bash
git clone https://github.com/FORKER_USERNAME/msds501_computation
cd msds501_computation
code .
```

**Task 2 – Read the Code, Find the Error**
- Partner A opens `partner_a.py`, Partner B opens `partner_b.py`
- Run your file: `python partner_a.py` (or `partner_b.py`)
- Read the traceback. What type of error? Which line?
- *Do not fix it yet* — write a comment explaining the cause

**Task 3 – Handle the Error**
- Wrap the risky line in `try / except`
- Catch the *specific* error type — no bare `except:`
- Print a message on failure that includes the index and bad value
- Run again — the script should complete without crashing

**Task 4 – Stage → Commit → Push**
```bash
git status
git add partner_a.py          # or partner_b.py
git commit -m "add try/except for ValueError"
git push origin main
```

**Task 5 – Pull & Review Your Partner's Code**
```bash
git pull origin main
```
Your partner's fixed file now appears in your local repo. Read it, run it, discuss.

## Need help?

- Re-read the error type slides from Day 2
- Google the exact last line of the traceback
- Ask your partner or instructor
