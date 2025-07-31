# ------------------------------------------------------------------------
# This file is used for static type verification using `mypy` or Pylance.
# It is NOT a runtime test and should NOT be run with pytest or Python.
#
# Instead, run it like this:
#     mypy tests/typecheck/mypy_typecheck.py
#
# This file uses `reveal_type()` to confirm that type inference and
# generic propagation work correctly across typed_api_response logic.
#
# You can also open this file in VSCode (with Pylance enabled) and
# simply hover over each variable to see the inferred type inline.
# It's a fast way to validate type behavior without running anything.
#
# This helps verify that:
#   - Generic[T] payloads retain their expected types
#   - Error and success responses expose the correct shape
#   - IDEs and static checkers see exactly what end users will see
#
# NOTE: `reveal_type()` is not a real function — it's a static analysis
# directive that prints to the console during `mypy` runs.
# ------------------------------------------------------------------------


from typed_api_response.response import build_api_response
from tests.testdata_cart import cart_dataclass, cart_pydantic

# Success Response:
response_pydantic = build_api_response(data=cart_pydantic, status=200)
response_dataclass = build_api_response(data=cart_dataclass, status=200)

reveal_type(response_pydantic)                          # expect ApiSuccessResponse[CartPydantic]
reveal_type(response_pydantic.payload)                  # expect SuccessPayload[CartPydantic]

reveal_type(response_dataclass.payload.data)            # expect: CartDataclass
reveal_type(response_dataclass.payload.data.items)      # expect: list[CartItemDataclass]

reveal_type(response_pydantic.payload.data)             # expect: CartPydantic
reveal_type(response_pydantic.payload.data.items)       # expect: list[CartItemPydantic]

reveal_type(response_pydantic.payload.success)          # expect: Literal[True]
reveal_type(response_pydantic.payload.error)            # expect: None

reveal_type(response_pydantic.meta)                     # expect: ResponseMeta


# Error Responses:
try:
    _ = 1 / 0
except Exception as e:
    response_error = build_api_response(error=e, status=500)
    
    reveal_type(response_error)                         # expect: ApiErrorResponse
    reveal_type(response_error.payload)                 # expect: ErrorPayload
    
    reveal_type(response_error.payload.data)            # expect: None
    reveal_type(response_error.payload.success)         # expect: Literal[False]
    
    reveal_type(response_error.payload.error)           # expect: ErrorPayloadData
    reveal_type(response_error.payload.error.type)      # expect: str
    reveal_type(response_error.payload.error.msg)       # expect:  str
    
    reveal_type(response_error.meta)                    # expect: ResponseMeta