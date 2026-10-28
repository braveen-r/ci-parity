import yaml
from pathlib import Path

def get_ci_requirements(directory=".github/workflows"):
    requirements = {"os": "unknown", "python": "unknown", "node": "unknown", "services": {}, "env": []}
    
    path = Path(directory)
    if not path.exists():
        return requirements

    for yml_file in path.glob("*.yml"):
        with open(yml_file, "r") as f:
            try:
                data = yaml.safe_load(f)
                jobs = data.get("jobs", {})
                for job_name, job_data in jobs.items():
                    if "runs-on" in job_data:
                        requirements["os"] = job_data["runs-on"]
                        
                    # Extract Environment Variables
                    if "env" in job_data:
                        requirements["env"].extend(job_data["env"].keys())
                        
                    # Extract Services (like Postgres/Redis)
                    if "services" in job_data:
                        for svc_name, svc_details in job_data["services"].items():
                            requirements["services"][svc_name] = svc_details.get("image", "unknown")
                    
                    for step in job_data.get("steps", []):
                        with_block = step.get("with", {})
                        if "python-version" in with_block:
                            requirements["python"] = str(with_block["python-version"])
                        if "node-version" in with_block:
                            requirements["node"] = str(with_block["node-version"])
            except Exception:
                continue
                
    return requirements
