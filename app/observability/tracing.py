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

# from functools import wraps
# from typing import Callable, Any
# import inspect

# from langfuse import observe


# def _trace(name: str):
#     def decorator(func: Callable[..., Any]):
#         observed_func = observe(name=name)(func)

#         # Async Generator (Streaming)
#         if inspect.isasyncgenfunction(func):
#             @wraps(func)
#             async def async_generator_wrapper(*args, **kwargs):
#                 async for item in observed_func(*args, **kwargs):
#                     yield item

#         # Async function
#         if inspect.iscoroutinefunction(func):
#             @wraps(func)
#             async def async_wrapper(*args, **kwargs):
#                 return await observed_func(*args, **kwargs)
#             return async_wrapper
        
#         # Sync function
#         @wraps(func)
#         def sync_wrapper(*args, **kwargs):
#             return observed_func(*args, **kwargs)
#         return sync_wrapper
    
#     return decorator




# def trace_workflow(name: str):
#     """
#     Workflow-level tracing

#     Example:
#     @tracing_workflow("advisor_workflow")
#     async def run(...):
#         ...
#     """

#     return _trace(name)


# def trace_step(name: str):
#     """
#     Node/step-level tracing

#     Example:
#     @trace("retrieve context")
#     async def retrieve(...):
#         ...
#     """

#     return _trace(name)


from functools import wraps
from typing import Any, Callable
import inspect

from langfuse import get_client

langfuse = get_client()


def _trace(
    name: str,
    *,
    input_mapper: Callable[..., Any] | None = None,
    output_mapper: Callable[[Any], Any] | None = None,
    metadata_mapper: Callable[[Any], dict[str, Any]] | None = None,
):
    def decorator(func: Callable[..., Any]):

        # -------------------------
        # Async Generator
        # -------------------------
        if inspect.isasyncgenfunction(func):

            @wraps(func)
            async def async_generator_wrapper(*args, **kwargs):
                input_data = (
                    input_mapper(*args, **kwargs)
                    if input_mapper
                    else None
                )

                with langfuse.start_as_current_observation(
                    name=name,
                    input=input_data,
                ) as observation:

                    last_item = None

                    try:
                        async for item in func(*args, **kwargs):
                            last_item = item
                            yield item

                        if output_mapper:
                            observation.update(
                                output=output_mapper(last_item)
                            )

                        if metadata_mapper:
                            observation.update(
                                metadata=metadata_mapper(last_item)
                            )

                    except Exception as e:
                        observation.update(
                            level="ERROR",
                            status_message=str(e),
                        )
                        raise

            return async_generator_wrapper

        # -------------------------
        # Async Function
        # -------------------------
        if inspect.iscoroutinefunction(func):

            @wraps(func)
            async def async_wrapper(*args, **kwargs):

                input_data = (
                    input_mapper(*args, **kwargs)
                    if input_mapper
                    else None
                )

                with langfuse.start_as_current_observation(
                    name=name,
                    input=input_data,
                ) as observation:

                    try:
                        result = await func(*args, **kwargs)

                        if output_mapper:
                            observation.update(
                                output=output_mapper(result)
                            )

                        if metadata_mapper:
                            observation.update(
                                metadata=metadata_mapper(result)
                            )

                        return result

                    except Exception as e:
                        observation.update(
                            level="ERROR",
                            status_message=str(e),
                        )
                        raise

            return async_wrapper

        # -------------------------
        # Sync Function
        # -------------------------
        @wraps(func)
        def sync_wrapper(*args, **kwargs):

            input_data = (
                input_mapper(*args, **kwargs)
                if input_mapper
                else None
            )

            with langfuse.start_as_current_observation(
                name=name,
                input=input_data,
            ) as observation:

                try:
                    result = func(*args, **kwargs)

                    if output_mapper:
                        observation.update(
                            output=output_mapper(result)
                        )

                    if metadata_mapper:
                        observation.update(
                            metadata=metadata_mapper(result)
                        )

                    return result

                except Exception as e:
                    observation.update(
                        level="ERROR",
                        status_message=str(e),
                    )
                    raise

        return sync_wrapper

    return decorator


def trace_workflow(
    name: str,
    *,
    input_mapper: Callable[..., Any] | None = None,
    output_mapper: Callable[[Any], Any] | None = None,
    metadata_mapper: Callable[[Any], dict[str, Any]] | None = None,
    ):
    return _trace(
        name=name,
        input_mapper=input_mapper,
        output_mapper=output_mapper,
        metadata_mapper=metadata_mapper,
    )


def trace_step(
    name: str,
    *,
    input_mapper: Callable[..., Any] | None = None,
    output_mapper: Callable[[Any], Any] | None = None,
    metadata_mapper: Callable[[Any], dict[str, Any]] | None = None,
):
    return _trace(
        name=name,
        input_mapper=input_mapper,
        output_mapper=output_mapper,
        metadata_mapper=metadata_mapper,
    )