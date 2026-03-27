import os
import re
import sys
from collections import defaultdict

def build_graph(workflow_dir):
    start_nodes = []
    edges = defaultdict(list)
    nodes = set()
    
    for filename in os.listdir(workflow_dir):
        if not filename.endswith(".md"): 
            continue
            
        node_name = filename.replace(".md", "")
        nodes.add(node_name)
        
        filepath = os.path.join(workflow_dir, filename)
        with open(filepath, 'r') as f:
            content = f.read()
            
        # Regex to find links to other workflows: [name](...workflows/name.md) or just [name] if typically used
        # Conservative approach: look for `[name](...name.md)` or `call workflow` patterns
        # For this audit, we'll scan for standard markdown links to other md files
        
        # Match [Link Text](dest) where dest ends in .md
        links = re.findall(r'\[.*?\]\((.*?\.md)\)', content)
        for link in links:
            target = os.path.basename(link).replace(".md", "")
            if target != node_name: # Ignore self-links
                edges[node_name].append(target)
                
    return nodes, edges

def get_depth(node, edges, visited, current_depth):
    if current_depth > 10: # Circuit breaker
        return 999
        
    if not edges[node]:
        return 1
        
    max_child_depth = 0
    for child in edges[node]:
        if child in visited: # Cycle
            print(f"CYCLE DETECTED: {node} -> {child}")
            return 999
        
        visited.add(child)
        d = get_depth(child, edges, visited, current_depth + 1)
        visited.remove(child)
        max_child_depth = max(max_child_depth, d)
        
    return 1 + max_child_depth

def main():
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    workflow_path = os.path.join(root_dir, "workflows")
    
    if not os.path.exists(workflow_path):
         print(f"Workflow directory not found: {workflow_path}")
         return

    print(f"Building call graph for {workflow_path}...")
    nodes, edges = build_graph(workflow_path)
    
    failed = False
    for node in nodes:
        depth = get_depth(node, edges, set(), 0)
        status = "PASS" if depth <= 3 else "FAIL"
        print(f"[{status}] {node}: Depth {depth}")
        if depth > 3:
            failed = True
            
    if failed:
        sys.exit(1)
    else:
        print("All workflows passed depth check.")

if __name__ == "__main__":
    main()
