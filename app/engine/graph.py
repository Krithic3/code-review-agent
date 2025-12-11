from typing import Callable, Dict, Optional, Any
from pydantic import BaseModel

class Node(BaseModel):
    name: str
    func_name: str
    params: Dict[str, Any] = {}

class Graph(BaseModel):
    nodes: Dict[str, Node]
    edges: Dict[str, Optional[str]]
    start: str
    loops: Optional[Dict[str, Dict]] = None
