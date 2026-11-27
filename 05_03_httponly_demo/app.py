from flask import Flask, make_response, request

app = Flask(__name__)

# Experimentálny prepínač. Najprv cookie JavaScriptu sprístupníme (False).
# V pokuse B ho zmeníš na True.
HTTP_ONLY = True

PAGE = """
<!doctype html>
<html lang="sk">
<head>
  <meta charset="utf-8">
  <title>Pokus s HttpOnly</title>
</head>
<body>
  <h1>Kto môže prečítať cookie?</h1>

  <p>
    Cookie obsahuje iba fiktívny token.
    Toto nie je skutočné prihlásenie.
  </p>

  <button id="read">Prečítať cookies JavaScriptom</button>
  <pre id="result"></pre>

  <p>
    <a href="/kontrola">Overiť, či cookie dostane server</a>
  </p>

  <script>
    document.querySelector("#read").addEventListener("click", () => {

          const cookies = ....;

      document.querySelector("#result").textContent = ...
        ;
    });
  </script>
</body>
</html>
"""


@app.route("/")
def index():
    response = make_response(PAGE)

    response.set_cookie(
        "demo_token",
        "FIKTIVNY_TOKEN_123",
        max_age=600,
        path="/",
        httponly=HTTP_ONLY,
        samesite="Lax",
    )

    return response


@app.route("/kontrola")
def kontrola():
    token = request.cookies.get("demo_token")

    if token == "FIKTIVNY_TOKEN_123":
        message = "Server dostal očakávanú fiktívnu cookie."
    else:
        message = "Server nedostal očakávanú fiktívnu cookie."

    return (
        f"<h1>{message}</h1>"
        '<p><a href="/">Späť na pokus</a></p>'
    )


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
