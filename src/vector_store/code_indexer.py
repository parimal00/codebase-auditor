from typing import List, Union
import chromadb
from chromadb.utils import embedding_functions

from src.schemas.ast_dto import ParsedFileDTO


class CodebaseVectorStore:
    def __init__(self, db_path: str = "./.chroma_db", collection_name: str = "codebase_ast"):
        self.client = chromadb.PersistentClient(path=db_path)

        self.embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="all-MiniLM-L6-v2"
        )

        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            embedding_function=self.embedding_fn
        )

    def index_parsed_ast(self, parsed_ast_data: List[Union[ParsedFileDTO, dict]], walker) -> int:
        """Indexes AST items (classes, functions) into ChromaDB using structural boundaries."""
        documents = []
        metadatas = []
        ids = []

        chunk_counter = 0

        for file_meta in parsed_ast_data:
            rel_path = file_meta.file_path if hasattr(file_meta, "file_path") else file_meta.get("file_path")
            if not rel_path:
                continue

            error = file_meta.error if hasattr(file_meta, "error") else file_meta.get("error")
            if error:
                continue

            self.collection.delete(where={"file_path": rel_path})

            full_code = walker.read_file(rel_path)
            lines = full_code.splitlines()

            functions = file_meta.functions if hasattr(file_meta, "functions") else file_meta.get("functions", [])
            for func in functions:
                func_name = func.name if hasattr(func, "name") else func.get("name")
                lineno = func.lineno if hasattr(func, "lineno") else func.get("lineno", 1)
                docstring = (func.docstring if hasattr(func, "docstring") else func.get("docstring")) or ""
                start_line = lineno - 1
                end_line = start_line + 30
                snippet = "\n".join(lines[start_line:end_line])

                doc_text = f"File: {rel_path}\nFunction: {func_name}\nDocstring: {docstring}\nCode:\n{snippet}"

                documents.append(doc_text)
                metadatas.append({
                    "file_path": rel_path,
                    "symbol_name": func_name,
                    "type": "function"
                })
                ids.append(f"{rel_path}::{func_name}::{chunk_counter}")
                chunk_counter += 1

            classes = file_meta.classes if hasattr(file_meta, "classes") else file_meta.get("classes", [])
            for cls in classes:
                cls_name = cls.name if hasattr(cls, "name") else cls.get("name")
                lineno = cls.lineno if hasattr(cls, "lineno") else cls.get("lineno", 1)
                docstring = (cls.docstring if hasattr(cls, "docstring") else cls.get("docstring")) or ""
                start_line = lineno - 1
                end_line = start_line + 50
                snippet = "\n".join(lines[start_line:end_line])

                doc_text = f"File: {rel_path}\nClass: {cls_name}\nDocstring: {docstring}\nCode:\n{snippet}"

                documents.append(doc_text)
                metadatas.append({
                    "file_path": rel_path,
                    "symbol_name": cls_name,
                    "type": "class"
                })
                ids.append(f"{rel_path}::{cls_name}::{chunk_counter}")
                chunk_counter += 1

        if documents:
            self.collection.upsert(
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )

        return len(documents)

    def search_codebase(self, query: str, top_k: int = 3) -> list:
        """Performs semantic vector search against stored codebase chunks."""
        results = self.collection.query(
            query_texts=[query],
            n_results=top_k
        )

        matches = []
        if results and results.get("documents"):
            for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
                matches.append({
                    "text": doc,
                    "metadata": meta
                })
        return matches
