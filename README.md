# Taller I – Programación · repositorio del curso

Universidad UCOM · 9 de noviembre al 14 de diciembre de 2026.

Este repositorio **no tiene código de partida**. Cada estudiante construye su sistema desde cero,
en su propio repositorio privado (`talleres-ucom/taller-i-<usuario>`). Acá está lo que la cátedra
entrega: el problema, el formato con el que el sistema se comunica con el exterior y una herramienta
para comprobarlo.

| Carpeta | Qué es |
|---|---|
| `reglas/reglas-del-dominio.md` | Las reglas de Arandu: qué tiene que hacer el sistema |
| `esquema/caso-v1.schema.json` | El contrato v1: el formato de un caso de aceptación (entrada y resultado esperado) |
| `casos-publicos/` | 13 casos de ejemplo en ese formato |
| `herramientas/verificar/` | `arandu-verificar`: corre casos contra el sistema de cada estudiante |

## El contrato v1 (Tarea 1)

El sistema de cada estudiante se ejecuta así:

```
uv run arandu evaluar <caso.json>
```

- **Recibe** la ruta de un archivo de caso. Usa solo la parte `entrada`; `esperado` es para quien
  verifica.
- **Imprime** en la última línea de la salida un JSON con el resultado:

  ```json
  {"resultado": "aceptada"}
  {"resultado": "rechazada", "motivo": "R5"}
  ```

Cómo está hecho por dentro (módulos, clases, pruebas) lo decide cada estudiante.

## Usar el verificador

No hace falta instalarlo: `uvx` lo descarga y lo corre.

```
# los 13 casos públicos contra el propio sistema
uvx --from "git+https://github.com/talleres-ucom/taller-I-2026#subdirectory=herramientas/verificar" arandu-verificar --publicos

# los casos propios (carpeta casos/)
uvx --from "git+https://github.com/talleres-ucom/taller-I-2026#subdirectory=herramientas/verificar" arandu-verificar casos

# solo revisar que los casos propios cumplan el formato
uvx --from "git+https://github.com/talleres-ucom/taller-I-2026#subdirectory=herramientas/verificar" arandu-verificar --solo-esquema casos
```

El verificador no contiene ninguna implementación de las reglas: solo ejecuta el comando del
estudiante y compara la respuesta con el resultado esperado de cada caso.
