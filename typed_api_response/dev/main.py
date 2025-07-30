from ..response import build_api_response
from dataclasses import dataclass


@dataclass
class FakeData:
    msg: str
    num: int
    is_dope: bool


if __name__ == "__main__":
# if 1:  
    data = FakeData(
        msg="asdfasdfasdf",
        num=123,
        is_dope=False,
    )
    api_response = build_api_response(data=data, status=200)
    api_response.payload.data
    
    print(api_response)