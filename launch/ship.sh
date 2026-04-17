#!/usr/bin/env bash
# Vera launch gate — one step at a time, with checks.
# Does what it can automate; stops and tells you what to paste where.

set -euo pipefail
cd "$(dirname "$0")/.."

bold() { printf "\033[1m%s\033[0m\n" "$*"; }
ok()   { printf "\033[32m✅ %s\033[0m\n" "$*"; }
ask()  { read -r -p "$(printf '\033[33m▶ %s\033[0m ' "$*")" _; }

bold "Vera launch — pre-flight"
command -v python3 >/dev/null || { echo "python3 missing"; exit 1; }
command -v git >/dev/null     || { echo "git missing"; exit 1; }
command -v pipx >/dev/null    || echo "note: pipx not on PATH — smoke test will need it"
ok "Tools present"

bold ""
bold "Step 1/6 — Build dist/"
# --user is rejected inside a venv; only pass it outside one.
pip_user_flag="--user"
if [[ -n "${VIRTUAL_ENV:-}" ]] || python3 -c "import sys; sys.exit(0 if sys.prefix != sys.base_prefix else 1)"; then
    pip_user_flag=""
fi
python3 -m pip install $pip_user_flag --quiet --upgrade build twine >/dev/null
rm -rf dist build ./*.egg-info
python3 -m build
python3 -m twine check dist/*
ok "Build passed twine check"

bold ""
bold "Step 2/6 — PyPI upload"
echo "   Open:  https://pypi.org/manage/account/token/"
echo "   Name:  vera-upload"
echo "   Scope: Entire account (rotate to project-scoped after first upload)"
ask "Token copied? ENTER to upload (user: __token__, password: your pypi-... token)."
python3 -m twine upload dist/*
echo "   Open:  https://pypi.org/project/vera-ai/"
ask "Is the 0.1.0 release live there? ENTER to continue."

bold ""
bold "Step 3/6 — Smoke test (run in a FRESH terminal)"
echo "   pipx install vera-ai"
echo "   vera --help"
ask "Did 'vera --help' print the four commands? ENTER if yes."

bold ""
bold "Step 4/6 — Patch README + LAUNCH.md to reference PyPI"
python3 - <<'PY'
import pathlib, re
changed = False
for f in ['README.md', 'LAUNCH.md']:
    p = pathlib.Path(f)
    if not p.exists():
        continue
    s = p.read_text()
    s2 = s.replace('pipx install git+https://github.com/iamitp/vera',
                   'pipx install vera-ai')
    s2 = re.sub(r'\n_\(PyPI release coming[^)]*\)_\n', '\n', s2)
    if s2 != s:
        p.write_text(s2)
        print(f'  patched {f}')
        changed = True
if not changed:
    print('  (no changes needed — already patched)')
PY
if git diff --quiet; then
    ok "Nothing to commit"
else
    git add README.md LAUNCH.md
    git commit -m "PyPI shipped: vera-ai is live"
    ok "Commit created"
    echo "   Run 'git push' when you're ready for visitors."
fi

bold ""
bold "Step 5/6 — Audit screenshot (do this before social posts)"
echo "   export ANTHROPIC_API_KEY=sk-ant-..."
echo "   vera init && vera chat   # 5-10 turns with sycophancy bait"
echo "   vera audit --share       # screenshot the output"
ask "Got a screenshot of the 'What Vera caught' block? ENTER to continue."

bold ""
bold "Step 6/6 — Post"
echo "   All copy is in launch/POSTS.md. Order:"
echo "   · §4 + §5   Show HN (T/W/Th 8-10am PT — reply for 2h)"
echo "   · §6 + §7   X thread (pin it, attach screenshot)"
echo "   · §8        r/LocalLLaMA  (wait ~4h post-HN so you can link it)"
echo "   · §9        r/ClaudeAI + r/OpenAI"
echo "   · §10       DMs to Simon → Huntley → Swyx"
echo "   · §12       Tracking tabs — check daily for 7 days"
ok ""
bold "🚢 Playbook complete. Ship."
