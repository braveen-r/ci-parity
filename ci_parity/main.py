import typer
from rich.console import Console
from rich.theme import Theme
from rich.table import Table
from rich.panel import Panel
import sys
from ci_parity.parsers.workflows import get_ci_requirements
from ci_parity.probes.local import get_local_state
from ci_parity.compare.versions import evaluate_mismatch
from ci_parity.fixes.suggestions import generate_fixes
from ci_parity.explain.analyzer import analyze_log

custom_theme = Theme({
    "info": "dim cyan",
    "warning": "magenta",
    "danger": "bold #B21318",
    "success": "bold green"
})
console = Console(theme=custom_theme)

app = typer.Typer(help="ci-parity: Sync your local dev environment with CI.", no_args_is_help=True)

@app.command()
def check():
    console.print("[info]Scanning .github/workflows...[/info]\n")
    ci_reqs = get_ci_requirements()
    
    if ci_reqs["os"] == "unknown" and ci_reqs["python"] == "unknown":
        console.print("[danger]❌ No CI configuration found.[/danger]")
        console.print("[info]Please run this command inside a repository that contains a .github/workflows directory.[/info]")
        sys.exit(1)
        
    local_state = get_local_state(ci_reqs)
    
    table = Table(header_style="info", border_style="dim cyan")
    table.add_column("ITEM")
    table.add_column("EXPECTED (CI)")  # <-- THE NEW HEADER
    table.add_column("ACTUAL (LOCAL)") # <-- THE NEW HEADER
    table.add_column("RESULT")
    
    table.add_row("OS", ci_reqs["os"], local_state["os"], evaluate_mismatch(ci_reqs["os"], local_state["os"], "os"))
    table.add_row("Python", ci_reqs["python"], local_state["python"], evaluate_mismatch(ci_reqs["python"], local_state["python"], "version"))
    table.add_row("Node", ci_reqs["node"], local_state["node"], evaluate_mismatch(ci_reqs["node"], local_state["node"], "version"))
    
    for svc, img in ci_reqs["services"].items():
        is_running = local_state["services"].get(svc, False)
        table.add_row(f"{svc.capitalize()} (service)", img, "running" if is_running else "not running", "[success]✅ match[/success]" if is_running else "[danger]❌ missing[/danger]")

    for env_var in ci_reqs["env"]:
        is_set = local_state["env"].get(env_var, False)
        table.add_row(env_var, "required", "set" if is_set else "not set", "[success]✅ match[/success]" if is_set else "[danger]❌ missing[/danger]")
    
    console.print(table)
    
    fixes = generate_fixes(ci_reqs, local_state)
    if not local_state["services"].get("postgres", True):
        fixes.append("docker run -d --name postgres -e POSTGRES_PASSWORD=pass -p 5432:5432 postgres:16")
    if not local_state["env"].get("DATABASE_URL", True):
        fixes.append("export DATABASE_URL='postgres://...' (add to .env)")

    if fixes:
        console.print("\n[warning]Likely cause:[/warning] Code using newer language features, or missing database/env vars.")
        fix_text = "\n".join([f"• {f}" for f in fixes])
        console.print(Panel(fix_text, title="[info]Recommended Fixes[/info]", border_style="dim cyan", expand=False))
    else:
        console.print("\n[success]Environments are perfectly synced![/success]")

@app.command()
def explain(run_url: str):
    console.print(f"[info]Connecting to GitHub API for:[/info] {run_url}\n")
    dummy_log = """
    Step 4: Run tests
    Error: Cannot find module 'node:test'
    Require stack:
    - /home/runner/work/app/app/test.js
    """
    console.print(Panel(dummy_log.strip(), title="[warning]Extracted CI Log Snippet[/warning]", border_style="dim magenta", expand=False))
    
    insights = analyze_log(dummy_log)
    for insight in insights:
        console.print(f"💡 {insight}")

if __name__ == "__main__":
    app()
