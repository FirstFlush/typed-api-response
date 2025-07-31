# This file is meant for mypy static analysis only.
# Do not run with pytest.

from typed_api_response.response import build_api_response
from tests.testdata_cart import cart_item_pydantic, cart_item_dataclass

response_pydantic = build_api_response(data=cart_item_pydantic, status=200)
response_dataclass = build_api_response(data=cart_item_dataclass, status=200)

reveal_type(response_pydantic.payload.data)     # expect data: CartItemPydantic
reveal_type(response_dataclass.payload.data)    # expect data: CartItemDataclass
