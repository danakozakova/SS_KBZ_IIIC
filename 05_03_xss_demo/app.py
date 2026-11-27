from flask import Flask, make_response, request

# =====================================================================
#  UČEBNÉ DEMO — ZÁMERNE OBSAHUJE BEZPEČNOSTNÚ CHYBU (XSS).
#  Beží len lokálne na tvojom počítači (127.0.0.1). Pracujeme s
#  FIKTÍVNYM tokenom. NIKDY to nenasadzuj na verejný web a nič
#  neskúšaj na cudzích stránkach.
# =====================================================================

app = Flask(__name__)

# Rovnaký prepínač ako v časti 1 (HttpOnly).
HTTP_ONLY = False

HLAVICKA = """
<!doctype html>
<html lang="sk">
<head><meta charset="utf-8"><title>Mini-nástenka</title></head>
<body>
  <h1>Mini-nástenka</h1>
  <p>Napíš odkaz a server ti ho zobrazí pod formulárom.</p>
  <form action="/" method="get">
    <input name="odkaz" size="50" placeholder="tvoj odkaz">
    <button type="submit">Zobraziť</button>
  </form>
  <hr>
"""

PATICKA = """
</body>
</html>
"""


@app.route("/")
def index():
    odkaz = request.args.get("odkaz", "")

    # ⚠️ CHYBA (XSS): hodnotu od používateľa vkladáme do stránky
    #    BEZ ošetrenia (escapovania). Preto sa z nej môže stať kód.
    telo = "<p>Posledný odkaz: " + odkaz + "</p>"

    response = make_response(HLAVICKA + telo + PATICKA)

    # Prihlasovací (fiktívny) token — to je to, čo chce útok ukradnúť.
    response.set_cookie(
        "demo_token",
        "FIKTIVNY_TOKEN_123",
        max_age=600,
        path="/",
        httponly=HTTP_ONLY,
        samesite="Lax",
    )
    return response


@app.route("/zber")
def zber():
    # "Server útočníka" — beží tiež len lokálne. Sem by v reálnom
    # útoku unikol ukradnutý token. My ho len vypíšeme do terminálu,
    # nič neodchádza z tvojho počítača.
    ukradnute = request.args.get("c", "")
    print("‼️  [utocnik] prislo mi:", ukradnute)
    return "ok"


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
