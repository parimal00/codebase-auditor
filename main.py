import json
import sys
from src.ingestion.codebase_walker import CodebaseWalker
from src.ingestion.ast_parser import PythonASTParser
from src.agents.graph_router import build_audit_graph
from rich.pretty import pprint
from src.reporting.console_reporter import display_audit_report
from src.reporting.exporter import export_report
from src.vector_store.code_indexer import CodebaseVectorStore
from rich import print
def run_ingestion(target_dir: str):
    
    print(f" Scanning directory: {target_dir}")
    walker = CodebaseWalker(target_dir)
    parser = PythonASTParser()

    files = walker.build_file_tree()
    print(f"Found {len(files)} files.")

    parsed_data = []
    for f in files:
        if f["extension"] == "py":
            code = walker.read_file(f["relative_path"])
            ast_meta = parser.parse_code(code, f["relative_path"])
            parsed_data.append(ast_meta)

    vectorStore = CodebaseVectorStore()
    vectorStore.index_parsed_ast(parsed_data, walker)
    
    
    initial_state = {
        "target_dir": target_dir,
        "file_tree": files,
        "parsed_ast": parsed_data,
        "findings": [],
        "current_node": "entry",
        "user_query": "how is architecture agent implemented",
        "route": "",
        "router_reasoning": "",
        "rag_response": {},
        "retrieved_matches": []
    }
    
    
    app = build_audit_graph()
    final_state = app.invoke(initial_state)
    
    pprint(final_state['rag_response'])
    
    return
    
    display_audit_report(final_state)    
    export_report(final_state, output_path="audit_report.json")
    
if __name__ == "__main__":
    path = "."
    run_ingestion(path)
    
