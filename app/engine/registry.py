from typing import Callable, Dict

class ToolRegistry:
    _tools: Dict[str, Callable] = {}

    @classmethod
    def register(cls, name: str, fn: Callable):
        cls._tools[name] = fn

    @classmethod
    def get(cls, name: str):
        if name not in cls._tools:
            raise KeyError(f"Tool '{name}' not registered")
        return cls._tools[name]

    @classmethod
    def list_tools(cls):
        return list(cls._tools.keys())
