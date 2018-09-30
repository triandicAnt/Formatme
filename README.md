## Formatme : Pre-Commit Hooks

### 1. `pre_commit_regex_me`
* Apply regex formatting to all the files added and modified by the git.
* Find all `untracked + modified` files by `git`.
* Filter `non-apex` files.
* Apply regex formatting to all filtered `apex` files.

#### Command: `pre-commit run --all-files`

```unix
(python3) ➜  Formatme git:(Pre-Commit-Hooks-apex) ✗ pre-commit run --all-files
Regex Expressions........................................................Failed
hookid: pre_commit_regex_me

Files were modified by this hook. Additional output:

"MarsController.cls" : is modified by Regex Expression.

(python3) ➜  Formatme git:(Pre-Commit-Hooks-apex) ✗ pre-commit run --all-files
Regex Expressions........................................................Passed
```
