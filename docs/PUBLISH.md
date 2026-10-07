# Publish the Repository

Created public repository: [devika1806/one-qubit-gate-explorer](https://github.com/devika1806/one-qubit-gate-explorer).

The commands below document the initial publication procedure. Do not rerun `gh repo create` for this existing repository; clone it to continue working.

The local project can be used immediately. Publishing requires authenticated GitHub access as `devika1806`. A username alone cannot authorize repository creation.

If the GitHub CLI is installed, open PowerShell in this project and run:

```powershell
gh auth login --hostname github.com --web
gh api user --jq .login
```

Verify that the printed account is `devika1806`, then:

```powershell
gh repo create devika1806/one-qubit-gate-explorer --public --source . --remote origin --push --description "A beginner quantum gate explorer: predict, measure, reveal hidden phase, and verify against Qiskit and QuTiP."
```

The create command is for a new, nonexistent remote repository. If that name already exists, inspect it first; do not overwrite it or force-push. `gh repo view devika1806/one-qubit-gate-explorer --web` opens an existing repository.

The virtual environment and credentials are ignored by Git. The committed `results/` directory contains simulated experiment data. The local ZIP contains tracked project files, not the virtual environment.

The workflow in `.github/workflows/checks.yml` is intended to rerun validation after publication. A local pass does not imply a GitHub Actions run has occurred.
