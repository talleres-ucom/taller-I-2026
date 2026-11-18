# Arandu · reglas del dominio v1

Taller I – Programación · Universidad UCOM · 2026. Adaptado del documento del caso Arandu (v3,
23-09-2026).

## El escenario

Un estudiante pide inscribirse en una comisión de una materia durante un período académico. El
sistema **acepta** la solicitud o la **rechaza con un motivo**, según las reglas de abajo. En la v1
no hay pagos, equivalencias, lista de espera ni autenticación.

**Entidades:**

| Entidad | Qué tiene |
|---|---|
| Estudiante | Un identificador y su historial de notas finales de períodos anteriores |
| Materia | Un código y sus correlativas |
| Comisión | Un identificador, la materia, el cupo y las franjas horarias |
| Período | Apertura, cierre y plazo de baja |
| Inscripción | El estudiante, la comisión y el estado (`activa` o `baja`) |

**El sistema nunca lee el reloj: recibe el instante de la solicitud.** Esa decisión es la que hace
deterministas las pruebas. Los instantes llevan zona horaria. Dos instantes iguales escritos con
zonas distintas (por ejemplo, `08:00-03:00` y `11:00Z`) son el mismo instante.

## Las reglas

**R1 · Ventana.** Se acepta solo si el instante cae entre la apertura y el cierre del período,
**ambos extremos incluidos**. Fuera de la ventana se rechaza siempre.

**R2 · Correlatividad.** Todas las correlativas de la materia tienen que estar aprobadas, es decir,
tener una nota final mayor o igual que la nota mínima del plan (`plan.nota_minima`; si no se indica,
es 2). Una materia cursada y reprobada no habilita. Si el historial tiene varias notas de la misma
materia, vale la mejor. Una materia sin correlativas no tiene esta restricción.

**R3 · Cupo.** El cupo es un entero mayor o igual que 0. Cada inscripción **activa** de cualquier
estudiante en esa comisión ocupa un lugar. Una baja no ocupa lugar. Con cupo 0 se rechaza siempre.

**R4 · Máximo.** Un estudiante no puede tener más de 6 inscripciones activas en el período. Las
bajas no cuentan.

**R5 · Choque de horarios.** La comisión pedida no puede chocar con ninguna inscripción activa del
estudiante. Dos franjas chocan si son del mismo día y sus intervalos se solapan:
`inicio_A < fin_B` y `inicio_B < fin_A`. Que una termine a las 21:00 y la otra empiece a las 21:00
**no es choque**. Una comisión puede tener varias franjas: alcanza con que una choque.

**R6 · Baja.** Se ve en la Tarea 2: no forma parte de la v1 del contrato.

**R7 · Unicidad.** Un estudiante no puede tener dos inscripciones **activas** a la misma materia en
el mismo período, aunque sean de comisiones distintas.

**R8 · Orden de evaluación.** Las reglas se evalúan en este orden: `R1 → R2 → R7 → R4 → R5 → R3`.
Se rechaza con **el primer motivo que aplique**. El orden es parte del contrato: una
implementación que rechaza por cupo cuando además había choque de horarios está mal, aunque
rechace.

## Casos limítrofes, resueltos de antemano

| Situación | Resultado |
|---|---|
| Solicitud exactamente en la apertura o en el cierre | Se acepta |
| Clases contiguas (una termina 21:00, otra empieza 21:00) | No es choque |
| Cupo lleno, pero con una baja previa | Hay lugar |
| Correlativa cursada y reprobada | Se rechaza (R2) |
| Materia sin correlativas | R2 no aplica |
| Reinscripción en la misma materia después de una baja | Se permite: R7 solo mira las activas |

## Fuera de alcance en la v1

Lista de espera, aranceles, equivalencias, autenticación y roles, notificaciones, historial de
auditoría y concurrencia.
