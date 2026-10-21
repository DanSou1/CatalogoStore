# Biblia de la serie "Recién mudados" (Vale y Andrés)

Este archivo guarda todo lo que tiene que repetirse igual en cada capítulo: personajes, escenario, voces, música y cómo se generan las tomas. Antes de producir un capítulo, se lee entero. Después de cada capítulo, se actualiza la sección "Estado de la historia" y la tabla de tomas.

Plan completo de la temporada: documento "Serie: Recién mudados (Vale y Andrés)" en Claude Docs (https://claude.ai/artifact/YBEKWgzJ7B5DCiVoxbwu64).

## Regla de continuidad

Las caras nunca se ven: tomas de espaldas, por encima del hombro, manos, pies, siluetas a contraluz. Así la IA no tiene que repetir un rostro y los personajes se reconocen por el pelo, la ropa y los objetos, que sí se pueden copiar exacto.

**Todo vive en el proyecto de Flow "Serie Recién mudados"** (cuenta PRO de Daniel, flow.google.com/project/5e106669-9adb-4d92-8364-1bb5965bab63):
- **Personajes** (sección Personajes, con su descripción guardada): `Vale` y `Andrés`. Creados el 21 oct 2026 con Nano Banana 2.1.
- **Imagen del apartamento**: "Modern apartment living room at night…" (sección Imágenes). Versión con cajas de trasteo; para la Parte 2 en adelante se genera una variante "boxes stacked in a corner, sofa without plastic" partiendo de esta.

Cómo se hace cada toma (chat de Flow):
1. Sesión nueva del chat (ícono de lápiz arriba a la derecha).
2. Escribir `@`, buscar `apartment` → "Agregar a la instrucción". Repetir con `@` + `Vale` y `@` + `Andr`.
3. Pegar el prompt de la toma y Enter. Flow pregunta "¿Quieres que inicie esta generación por 12 créditos?" → **Aprobar** (no "Aprobar siempre").
4. Si hay fila por demanda, mandar las demás tomas en sesiones nuevas y volver a "Videos".

Copias locales de referencia: carpeta `ref/` de este directorio, cuando se descarguen.

## Personajes (texto fijo para pegar en cada prompt)

**Vale** (29, diseñadora):
`a Latina woman, 29, long dark brown curly hair loose to mid-back, small gold hoop earrings, mustard-yellow oversized knit sweater, light-wash high-waist jeans, white socks, silver ring on her right index finger`

**Andrés** (31, contador):
`a Latino man, 31, short dark hair faded on the sides, light beard, navy blue hoodie, grey joggers, black digital watch on his left wrist`

**Doña Gloria** (mamá de Andrés, aparece desde la Parte 3):
`a Latina woman in her late 50s, short grey-streaked hair in a neat bob, burgundy cardigan, pearl stud earrings, carries a small floral suitcase`

## Escenario

**Apartamento** (todos los capítulos):
`small modern apartment in Bogotá at night, exposed red brick wall, large window with rainy city lights and mountains in the distance, warm wooden floor, grey fabric sofa with a mustard throw blanket, a monstera plant in a terracotta pot, warm amber floor lamp, string of warm fairy lights on the brick wall`

Detalle por capítulo:
- Parte 1: cajas de cartón de trasteo por todas partes, sin texto; el sofá aún con plástico.
- Parte 2 en adelante: cajas ya desocupadas y apiladas en una esquina; cojines en el sofá.

**Paleta**: ámbar cálido, mostaza, ladrillo, azul noche de la ventana. Sin neón (el neón rosa solo en la placa de cierre de la marca).

## Plantilla de prompt para Flow (inglés)

```
Vertical 9:16, cinematic, shallow depth of field, warm amber light, 35mm film look.
[ESCENARIO]
[PERSONAJE(S)], seen from behind / over the shoulder / only hands, faces never visible.
[ACCIÓN de la toma, una sola]
Casual clothes, no nudity, no text, no logos, no subtitles.
```
Una sesión nueva del chat de Flow por toma (en la misma sesión fallan). 12 créditos por toma de 8 s; 15 con dos personas.

## Voces (ElevenLabs, Eleven v4)

| Personaje | Voz | Ajustes |
| --- | --- | --- |
| Narradora | "Daniela - Vendedora" | estabilidad 50 %, similitud 75 %, estilo 20 %, velocidad 1,05 |
| Andrés | "Andrés - XperienceLove" | estabilidad 50 %, velocidad 1,0 |
| Vale | "Vale - XperienceLove" (crear en Diseño de voz si no existe) | estabilidad 50 %, velocidad 1,0 |

Prompt de diseño de voz de Vale: `Young Colombian woman from Bogotá, 29 years old, warm, playful and a little teasing, natural conversational tone, soft smile in the voice, neutral Bogotá accent, clear diction.`

## Sonido de serie

- Apertura: sonido de llaves abriendo una puerta + "Recién mudados · Parte X" como subtítulo grande al centro, en los 2 primeros segundos de todos los capítulos.
- Música: lo-fi R&B cálido, instrumental, el mismo tema en toda la temporada (`musica/tema.mp3` cuando exista). Ducking bajo la voz.
- Cierre: pantera neón + palabra clave del capítulo + "Pregunta por WhatsApp".

## Estado de la historia (se actualiza después de cada capítulo)

- **Parte 1 · Las cajas**: primera noche en el apartamento, comen pizza en el piso, pacto de "viernes de juego, sin celular". Juegan Verdad o se atreve. Suspenso: Vale lee "¿Qué es lo que nunca le has contado a tu pareja?" y Andrés se queda callado. Objetos que deben seguir: la caja de pizza, la vela en un frasco de vidrio, la baraja Verdad o se atreve en el piso.

## Tomas generadas (para reutilizar)

| Capítulo | Archivo | Qué muestra |
| --- | --- | --- |
| 1 | `parte-01/tomas/t1-puerta.mp4` | Mano con llaves abre la puerta; a los 6 s se prende la luz de la sala con cajas |
| 1 | `parte-01/tomas/t2-pizza-piso.mp4` | Vale y Andrés de espaldas en el piso comiendo pizza frente a la ventana; ella recuesta la cabeza (5–7 s). Los 2 primeros segundos traen esquinas redondeadas: no usar |
| 1 | `parte-01/tomas/t3-celulares.mp4` | Celulares en el piso junto a la pizza; las manos los toman (3–5 s); Vale baja el de Andrés y queda boca abajo (6–8 s) |
| 1 | `parte-01/tomas/t5-manos.mp4` | Manos que se entrelazan sobre la pizza con una vela (3–7 s) |
| 1 | `parte-01/tomas/t6-carta.mp4` | Por encima del hombro de Andrés: Vale de lado con pizza y una carta en blanco |

Video final de la Parte 1: `parte-01/recien-mudados-parte-01.mp4` (37 s). Montaje: `parte-01/build_p1.py` (para cada parte nueva se copia y se cambian SHOTS, VOICE y SUBS).

**Voz y música usadas**: narración "Daniela - Vendedora" en bloques cortos sin etiquetas de pausa (cada [short pause] suma ~0,5 s); Vale con sus frases en un solo audio separado por [long pause] y recortado en el montaje. Música de fondo: `musica-tema.mp3` (Playful Heart), al 30 % con ducking. El ambiente de las tomas de Flow va al 35 %.
