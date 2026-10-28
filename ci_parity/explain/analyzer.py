def analyze_log(log_text):
    """Scans a CI log for common environment-related failure signatures."""
    insights = []
    
    if "Cannot find module" in log_text or "MODULE_NOT_FOUND" in log_text:
        insights.append("[danger]Node.js Mismatch:[/danger] CI failed to resolve a module. This often happens if the CI Node version is older than your local version and lacks support for newer built-in packages.")
        
    if "psql: error: connection to server" in log_text or "Connection refused" in log_text:
        insights.append("[danger]Database Missing:[/danger] The CI pipeline attempted to connect to a database service, but it was either not defined in the workflow's `services:` block or failed to start.")
        
    if "KeyError:" in log_text or "undefined" in log_text.lower():
        insights.append("[danger]Missing Env Var:[/danger] The application crashed trying to read an environment variable that wasn't exposed to the CI runner.")
        
    if not insights:
        insights.append("[info]No obvious environment-related crashes found in the log snippet.[/info]")
        
    return insights
