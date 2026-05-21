# GitHub Setup

Target repository:

```text
phildavies/GBP-Operations-Agent
```

## Create Remote Repository

Create a new empty GitHub repository named `GBP-Operations-Agent`.

Recommended settings:

- visibility: private until credentials and publishing controls are mature
- initialize with README: no
- add `.gitignore`: no
- add license: choose later

## Connect Local Project

After the remote exists, run:

```powershell
git branch -M main
git add .
git commit -m "Initialize GBP operations agent framework"
git remote add origin https://github.com/phildavies/GBP-Operations-Agent.git
git push -u origin main
```

## Notes

This project is intentionally configured for draft-first operation. Keep live publishing disabled until the approval workflow, logging, and Google API scopes are verified.
