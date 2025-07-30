# FastAPI-Compatible Typed API Response Builder

This library provides a type-safe, extensible, and strictly validated system for generating standardized API responses in Python. It’s designed for projects that use Pydantic, Django Ninja, FastAPI, or similar frameworks — and want to return rich, well-structured responses with full IDE support, including compatibility with Pylance strict mode.


## 🔧 Features

- ✅ Typed response builders for both success and error responses
- ✅ Fully generic, Pylance-compliant with strict mode enabled
- ✅ Single unified function: `build_api_response(...)`
- ✅ Extensible metadata support via `ResponseMeta`
- ✅ Automatically distinguishes between `data` and `error`
- ✅ Raises clean custom exceptions on misconfiguration


## 🚀 Getting Started

### Define your Pydantic response schema:

```python
from pydantic import BaseModel
from typing import Any

class PredictionResponse(BaseModel):
    entities: list[dict[str, Any]]
```


### Return a structured API response using the builder:

```python
@router.post("/foo", response_model=PredictionResponse)
def foo():
    result = PredictionResponse(entities=[{"label": "RESOURCE", "value": "food"}])
    return build_api_response(data=result, status=200)
```

✅ build_api_response() accepts any Pydantic model or well-typed object and wraps it into a fully structured, metadata-rich response — with full type hint propagation and IDE support via generics.


### Handling errors just as cleanly

You can also return exceptions using the same unified response format:

```python
try:
    ...
except Exception as e:
    return build_api_response(error=e, status=418)
```

✅ build_api_response() wraps the exception in a type-safe, structured error payload — so your failure responses stay as consistent and predictable as your success ones.


## 🧱 API Structure

### Unified Interface

```python
def build_api_response(
    *,
    data: T | None = None,
    error: Exception | None = None,
    status: int,
    meta: ResponseMeta | None = None,
) -> ApiSuccessResponse[T] | ApiErrorResponse
```

- Provide **either** `data` *or* `error`, not both
- `meta` lets you attach timing, versioning, request ID, etc.
- If neither `data` nor `error` is passed, raises `ApiResponseBuilderError`


### Success Response Format

```json
{
  "status": 200,
  "meta": {
    "duration": null,
    "extra": null,
    "method": null,
    "path": null,
    "request_id": null,
    "timestamp": "2025-07-30T04:33:44.833Z",
    "version": null
  },
  "payload": {
    "success": true,
    "data": { ... },
    "error": null
  }
}
```


### Error Response Format

```json
{
  "status": 418,
  "meta": {
    "duration": null,
    "extra": null,
    "method": null,
    "path": null,
    "request_id": null,
    "timestamp": "2025-07-30T00:13:55.531Z",
    "version": null
  },
  "payload": {
    "success": false,
    "data": null,
    "error": {
      "type": "ZeroDivisionError",
      "msg": "division by zero"
    }
  }
}
```


## 🧠 Customizing Metadata

Use `ResponseMeta` to attach custom fields:

```python
meta = ResponseMeta(
    request_id="abc123",
    version="v1.2.0",
    extra={"model": "en_streetninja", "debug": True}
)

return build_api_response(data=result, status=200, meta=meta)
```


## 🛡️ Exceptions

This toolkit raises:

- `ApiResponseBuilderError` – if payload generation fails
- `ApiPayloadBuilderError` – if payload data is inconsistent or incomplete


## 📦 Components

- `ApiResponseBuilder` – abstract base class for builders
- `ApiSuccessResponseBuilder` – builds `ApiSuccessResponse[T]`
- `ApiErrorResponseBuilder` – builds `ApiErrorResponse`
- `ResponseMeta` – optional metadata block
- `Payload` / `SuccessPayload[T]` / `ErrorPayload` – structured payload schemas


## 🧪 Type Safety

This library is:
- Designed for Pylance strict mode
- Fully generic
- Uses overloads to preserve type inference

No need to type hint manually:

```python
response = build_api_response(data=MySchema(...), status=200)
# response.payload.data is inferred as MySchema ✅
```
