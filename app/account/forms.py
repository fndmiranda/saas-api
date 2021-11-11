from starlette_wtf import StarletteForm
from wtforms import PasswordField, validators


class PasswordResetForm(StarletteForm):
    password = PasswordField(
        "Nova senha",
        [
            validators.DataRequired(),
            validators.Length(min=6, max=32),
        ],
        render_kw={"class": "form-control"},
    )
    confirm = PasswordField(
        "Confirme a nova senha",
        [
            validators.DataRequired(),
            validators.Length(min=6, max=32),
            validators.EqualTo(
                "password", message="As senhas devem ser iguais"
            ),
        ],
        render_kw={"class": "form-control"},
    )
