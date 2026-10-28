def generate_fixes(ci_reqs, local_state):
    fixes = []
    
    # Python fix using uv
    if ci_reqs["python"] != "unknown" and not local_state["python"].startswith(ci_reqs["python"]):
        fixes.append(f"uv python install {ci_reqs['python']} && uv venv --python {ci_reqs['python']}")
        
    # Node fix using nvm
    if ci_reqs["node"] != "unknown" and not local_state["node"].startswith(ci_reqs["node"]):
        fixes.append(f"nvm install {ci_reqs['node']} && nvm use {ci_reqs['node']}")
        
    return fixes
