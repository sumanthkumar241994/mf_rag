# # verison 1

# from functools import wraps
# from typing import Callable, Any

# from langfuse import observe


# def trace_workflow(name: str):
#     """
#     Workflow-level tracing

#     Example:
#     @tracing_workflow("advisor_workflow")
#     async def run(...):
#         ...
#     """

#     def decorator(func: Callable[..., Any]):
#         observed_func = observe(name=name)(func)

#         @wraps(func)
#         async def wrapper(*args, **kwargs):
#             return await observed_func(*args, **kwargs)
        
#         return wrapper
    
#     return decorator


# def trace_step(name: str):
#     """
#     Node/step-level tracing

#     Example:
#     @trace("retrieve context")
#     async def retrieve(...):
#         ...
#     """

#     def decorator(func: Callable[..., Any]):
#         observed_func = observe(name=name)(func)

#         @wraps(func)
#         async def wrapper(*args, **kwargs):
#             return await observed_func(*args, **kwargs)
        
#         return wrapper
#     return decorator

from functools import wraps
from typing import Callable, Any
import inspect

from langfuse import observe


def _trace(name: str):
    def decorator(func: Callable[..., Any]):
        observed_func = observe(name=name)(func)

        # Async Generator (Streaming)
        if inspect.isasyncgenfunction(func):
            @wraps(func)
            async def async_generator_wrapper(*args, **kwargs):
                async for item in observed_func(*args, **kwargs):
                    yield item

        # Async function
        if inspect.iscoroutinefunction(func):
            @wraps(func)
            async def async_wrapper(*args, **kwargs):
                return await observed_func(*args, **kwargs)
            return async_wrapper
        
        # Sync function
        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            return observed_func(*args, **kwargs)
        return sync_wrapper
    
    return decorator




def trace_workflow(name: str):
    """
    Workflow-level tracing

    Example:
    @tracing_workflow("advisor_workflow")
    async def run(...):
        ...
    """

    return _trace(name)


def trace_step(name: str):
    """
    Node/step-level tracing

    Example:
    @trace("retrieve context")
    async def retrieve(...):
        ...
    """

    return _trace(name)