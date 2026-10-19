# Contribuir a SkyFlap

¡Gracias por tu interés en mejorar **SkyFlap**! Esta guía resume cómo proponer cambios.

## 🧭 Antes de empezar

- Revisá los [issues abiertos](../../issues) para no duplicar trabajo.
- Para cambios grandes, abrí primero un issue y conversemos el enfoque.

## 🛠️ Entorno local

```bash
python -m venv .venv
.venv\Scripts\activate   # en Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
python Final6.py
# pruebas
pytest
```

Más detalles en el [README](README.md).

## 🌿 Flujo de trabajo

1. Hacé un fork y creá una rama desde `main`: `feat/nombre-corto`, `fix/nombre-corto` o `docs/nombre-corto`.
2. Usá [Conventional Commits](https://www.conventionalcommits.org/es/v1.0.0/): `feat:`, `fix:`, `docs:`, `refactor:`, `test:`, `chore:`.
3. Verificá que el proyecto compile y que las pruebas pasen antes de abrir el PR.
4. Abrí el Pull Request completando la plantilla y enlazá el issue (`Closes #123`).

## ✅ Checklist del PR

- [ ] El cambio está acotado a un solo objetivo.
- [ ] Actualicé la documentación si hacía falta.
- [ ] No subí secretos (`.env`, claves, tokens).

## 💬 Código de conducta

Al participar aceptás el [Código de Conducta](CODE_OF_CONDUCT.md).
