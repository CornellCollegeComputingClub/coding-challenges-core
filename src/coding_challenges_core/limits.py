from dataclasses import dataclass
import ast
from typing import Optional

@dataclass
class Limits:
    ### Preprocessing ###
    max_statements: int = -1
    # allow_threads: bool = False
    # allow_processes: bool = False # via subprocess, multiprocessing, or os.fork
    # allow_filesystem: bool = False # via open, os, pathlib, etc.
    # allow_network: bool = False # via socket, requests, urllib, etc.
    # allow_eval: bool = False # via eval, exec, compile
    allowed_imports: Optional[list[str]] = None
    test_mode: bool = False # let through potentially unsafe code for testing purposes

    # ### Execution ###
    # max_execution_time: int = 60 # seconds
    # max_memory: int = 512 # MB

def _count_statements(tree: ast.AST) -> int:
    # TODO: improve statement counting! it's... vague right now.
    # like what even counts as a statement? probably shouldn't count imports
    return sum(isinstance(node, ast.stmt) for node in ast.walk(tree))

def validate(limits: Limits, src: str) -> None:
    tree = ast.parse(src)
    num_statements = _count_statements(tree)
    if limits.max_statements != -1 and num_statements > limits.max_statements:
        raise ValueError(f"Code contains {num_statements} statements, exceeding the limit of {limits.max_statements}.")

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names: # TODO: handle from ... import ...
                if limits.allowed_imports is not None and alias.name not in limits.allowed_imports:
                    raise ValueError(f"Import of '{alias.name}' is not allowed.")
        if isinstance(node, ast.ImportFrom):
            if limits.allowed_imports is not None and node.module not in limits.allowed_imports:
                raise ValueError(f"Import from '{node.module}' is not allowed.")
        elif isinstance(node, ast.Call):
            # TODO: improve this!
            # for now, i'm skipping this because it's BAD.
            continue
            func_name = getattr(node.func, 'id', None) or getattr(getattr(node.func, 'attr', None), 'id', None)
            if func_name in {'eval', 'exec', 'compile'} and not limits.allow_eval:
                raise ValueError(f"Use of '{func_name}' is not allowed.")
            if func_name in {'open', 'os', 'pathlib'} and not limits.allow_filesystem:
                raise ValueError(f"Use of filesystem operations is not allowed.")
            if func_name in {'socket', 'requests', 'urllib'} and not limits.allow_network:
                raise ValueError(f"Use of network operations is not allowed.")
            if func_name in {'threading', 'multiprocessing', 'subprocess', 'os.fork'}:
                if (func_name in {'threading'} and not limits.allow_threads) or \
                   (func_name in {'multiprocessing', 'subprocess', 'os.fork'} and not limits.allow_processes):
                    raise ValueError(f"Use of '{func_name}' is not allowed.")
