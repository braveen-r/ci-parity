def evaluate_mismatch(ci_val, local_val, item_type):
    if ci_val == "unknown" or local_val == "not installed":
        return "[danger]❌ missing[/danger]"
    
    if item_type == "os":
        if ci_val.split("-")[0].lower() not in local_val.lower():
            return "[warning]⚠ different[/warning]"
        return "[success]✅ match[/success]"
        
    # Semantic versioning comparison (e.g., 22.4 vs 26.12.1)
    ci_parts = ci_val.split(".")
    local_parts = local_val.split(".")
    
    if ci_parts[0] != local_parts[0]:
        return "[danger]❌ major differs[/danger]"
    elif len(ci_parts) > 1 and len(local_parts) > 1 and ci_parts[1] != local_parts[1]:
        return "[warning]⚠ minor differs[/warning]"
        
    return "[success]✅ match[/success]"
