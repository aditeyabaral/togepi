from flask import Flask, render_template

app = Flask(
    __name__,
    static_folder="static",
    template_folder="templates"
)

@app.route("/loginregister", methods=["GET", "POST"])
def loginregisterpage():
    return render_template("templates/login-register.html")


if __name__ == "__main__":
    app.run()