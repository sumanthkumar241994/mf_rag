from functools import wraps
from typing import Callable, Any

from langfuse import observe


def trace_workflow(name: str):
    """
    Workflow-level tracing

    Example:
    @tracing_workflow("advisor_workflow")
    async def run(...):
        ...
    """

    def decorator(func: Callable[..., Any]):
        observed_func = observe(name=name)(func)

        @wraps(func)
        async def wrapper(*args, **kwargs):
            return await observed_func(*args, **kwargs)
        
        return wrapper
    
    return decorator


def trace_step(name: str):
    """
    Node/step-level tracing

    Example:
    @trace("retrieve context")
    async def retrieve(...):
        ...
    """

    def decorator(func: Callable[..., Any]):
        observed_func = observe(name=name)(func)

        @wraps(func)
        async def wrapper(*args, **kwargs):
            return await observed_func(*args, **kwargs)
        
        return wrapper
    return decorator