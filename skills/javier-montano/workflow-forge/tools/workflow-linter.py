import os
import re
import sys

WORKFLOW_DIR = "../workflows"
MAX_STEPS = 10

def lint_workflow(filepath):
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Extract "The Recipe" or "The Protocol" section
    # Heuristic: Find section starting with "## The Recipe" or similar, count numbered lists until next ## section
    
    lines = content.split('\n')
    in_recipe = False
    step_count = 0
    
    recipe_headers = ["## The Recipe", "## Protocol", "## Execution", "## Steps"]
    
    for line in lines:
        if any(line.strip().startswith(h) for h in recipe_headers):
            in_recipe = True
            continue
        
        if in_recipe:
            if line.strip().startswith("## ") and not any(line.strip().startswith(h) for h in recipe_headers):
                in_recipe = False
                break
            
            # Count numbered list items (e.g., "1. ", "10. ")
            if re.match(r'^\d+\.\s', line.strip()):
                step_count += 1
                
    return step_count

def main():
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    workflow_path = os.path.join(root_dir, "workflows")
    
    failed = False
    print(f"Linting workflows in {workflow_path}...")
    
    if not os.path.exists(workflow_path):
         print(f"Workflow directory not found: {workflow_path}")
         return

    for filename in os.listdir(workflow_path):
        if filename.endswith(".md"):
            filepath = os.path.join(workflow_path, filename)
            count = lint_workflow(filepath)
            status = "PASS" if count <= MAX_STEPS else "FAIL"
            print(f"[{status}] {filename}: {count} steps")
            
            if count > MAX_STEPS:
                failed = True
                
    if failed:
        sys.exit(1)
    else:
        print("All workflows passed step count check.")

if __name__ == "__main__":
    main()
