## For Auth im using a JWT

The JWS is MACed using the HMAC SHA-256 algorithm.
The JWT [RFC7519](https://www.rfc-editor.org/info/rfc7519/#section-3) and JWS [RFC7515](https://www.rfc-editor.org/info/rfc7515/#section-3) describe the JWT and JWS as follows:

JWT - JSON Web Token
JWS - JSON Web Signature

JWS represents digitally signed or MACed content using JSON data structures and base64url encoding.
A JWS represents these logical values:
* JOSE Header
* JWS Payload
* JWS Signature

For a JWS, the JOSE Header members are the union of the members of these values:
* JWS Protected Header
* JWS Unprotected Header

The RFC7515 document defines two serializations for JWSs: a compact, URL-safe serialization called the JWS Compact Serialization and a JSON serialization called the JWS JSON Serialization.

I will go with the **JWS Compact Serialization**:
```text
BASE64URL(UTF8(JWS Protected Header)) || '.' ||
BASE64URL(JWS Payload) || '.' ||
BASE64URL(JWS Signature)
```

### Example JWS
The following example JWS Protected Header declares that the encoded object is a JSON Web Token JWT and the JWS Protected Header and the JWS Payload are secured using the **HMAC SHA-256** algorithm:
```text
{
    "typ":"JWT",
    "alg":"HS256"
}
```
Encoding this JWS Protected Header as BASE64URL(UTF8(JWS Protected Header)) gives this value:
```text
    eyJ0eXAiOiJKV1QiLA0KICJhbGciOiJIUzI1NiJ9
```

The JWS Payload used in this example is the octets of the UTF-8 representation of the JSON object below.
```text
{
    "iss":"joe",
    "exp":1300819380,
    "http://example.com/is_root":true
    }
```
Encoding this JWS Payload as BASE64URL(UTF8(JWS Payload)) gives this value (with line breaks for display purposes only):
```text
    eyJpc3MiOiJqb2UiLA0KICJleHAiOjEzMDA4MTkzODAsDQogImh0dHA6Ly9leGFt
    cGxlLmNvbS9pc19yb290Ijp0cnVlfQ
```
Combining these as BASE64URL(UTF8(JWS Protected Header)) || '.' || BASE64URL(JWS Payload) gives this string (with line breaks for display purposes only):
```text
    eyJ0eXAiOiJKV1QiLA0KICJhbGciOiJIUzI1NiJ9
     .
     eyJpc3MiOiJqb2UiLA0KICJleHAiOjEzMDA4MTkzODAsDQogImh0dHA6Ly9leGFt
     cGxlLmNvbS9pc19yb290Ijp0cnVlfQ
```
Running the HMAC SHA-256 algorithm on the JWS Signing Input with a randomly generated key (python **secrets**). Computing the HMAC of the JWS Signing Input ASCII(BASE64URL(UTF8(JWS Protected Header)) || '.' || BASE64URL(JWS Payload)) with the HMAC SHA-256 algorithm using the key specified and base64url-encoding the result yields this BASE64URL(JWS Signature) value:

```text
    dBjftJeZ4CVP-mB92K27uhbUJU1p1r_wW1gFWFOEjXk
```

 Concatenating these encoded parts in this order with period ('.') characters between the parts yields this complete JWT (with line breaks for display purposes only):
 ```text
    eyJ0eXAiOiJKV1QiLA0KICJhbGciOiJIUzI1NiJ9
    .
    eyJpc3MiOiJqb2UiLA0KICJleHAiOjEzMDA4MTkzODAsDQogImh0dHA6Ly9leGFt
    cGxlLmNvbS9pc19yb290Ijp0cnVlfQ
    .
    dBjftJeZ4CVP-mB92K27uhbUJU1p1r_wW1gFWFOEjXk
 ```