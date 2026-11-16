# Parte 4 · La portería (versión sitcom)

Pedido de Daniel (tablero, 15 nov 2026): que se sienta como una serie de TV tipo *The Big Bang Theory*, con chistes y personajes mirando a cámara, natural y no robotizado. Se toma el **formato** de sitcom (escenas cortas, remate cada 4-5 s, risas de público, momento a cámara), nunca personajes, frases, música ni nada de esa serie.

- **Pilar**: humor de pareja (con historia).
- **Producto ancla**: el envío discreto (caja sin marca, sin nombre del producto) + contra entrega en Bogotá. Orgánico.
- **Llamado**: Comenta DISCRETO.
- **Suspenso**: "Me quedo una semanita, mijo" → Parte 5 (Una semana con la suegra).
- **Duración**: ~42 s (una sitcom necesita los remates; si la retención cae antes de 15 s, se corta la versión de 30 s quitando el beat 4).

## Tres maneras de grabarla (Daniel elige una en el tablero)

| | Opción | Cómo se ve | Caras | Riesgo / costo |
|---|---|---|---|---|
| A | **Confesionario** (recomendada) | Escenas de sala en plano abierto, cortadas con cada personaje sentado en el sofá hablándole a la cámara (como los documentales de oficina) | Sí | Lo más "serie de TV" y lo que pediste. Las caras tienen que ser iguales en todas las tomas: se crean primero los 3 personajes con foto de referencia en Flow. Los diálogos los genera Flow con la boca sincronizada (ElevenLabs no sirve con la cara visible). ~9 tomas × 15 = **~135 créditos** (pasa el tope de 100: necesito tu OK) |
| B | **Multicámara de sala** | Plano frontal de la sala como un set de TV, sin hablarle a cámara; risas de público | Sí | Mismo costo y mismo trabajo de caras que A, pero menos "mirada a cámara" |
| C | **Sitcom sin caras** | Mismo guion y mismas risas, pero de espaldas, manos y siluetas como las partes 1-3; los "confesionarios" son un plano fijo del cojín/sofá con la voz | No | Fiel a la biblia, voces de ElevenLabs. ~6 tomas × 15 = **~90 créditos** |

**Riesgo de las caras (opciones A y B)**: Flow genera cada toma por separado, y aunque use la misma foto de referencia la cara puede cambiar un poco entre tomas (nariz, cejas, edad, peinado), sobre todo de perfil, con gestos fuertes o cuando hay dos o tres personas en el cuadro. En una serie eso se nota enseguida y rompe la ilusión. Cómo lo bajamos: personajes guardados en Flow con su foto de referencia, una sola persona por confesionario, planos medios frontales, y repetir la toma que salga distinta (cada repetición cuesta 12-15 créditos más). Aun así puede pasar que alguna toma no quede igual. Si eso preocupa, la C conserva el humor en los diálogos y no tiene ese riesgo.

**Importante**: la serie hasta hoy es sin caras (regla de la biblia). Para A o B escribe en el comentario de la tarea **"Apruebo caras en la serie"** y la letra. Los personajes con cara se declaran como IA en el caption, como siempre.

## Guion (opción A)

| # | Tiempo | Plano | Diálogo | Sonido |
|---|---|---|---|---|
| 0 | 0–2 s | Placa `titulo_p4` (o t1-puerta de la Parte 1) | — | llaves + tema de la serie |
| 1 | 2–7 s | Sala, plano abierto: Andrés con el citófono en la mano, congelado. Vale en el sofá | Vale: "¿Quién era?" · Andrés: "El paquete." · Vale: "¡Ay, qué bien!" · Andrés: "…y mi mamá." | risas |
| 2 | 7–11 s | **Confesionario Vale** (sofá, cojín mostaza, mira a cámara) | "El paquete lo estábamos esperando hace una semana… a mi suegra, nadie." | risas |
| 3 | 11–16 s | Puerta: entra doña Gloria con la maleta floral y una caja de cartón; la sacude junto a la oreja | Gloria: "Mijo, el portero me dio esto. ¿Qué es? Suena raro." | risas |
| 4 | 16–20 s | **Confesionario Andrés** (se pasa la mano por la nuca) | "Yo soy contador. Con los números no sudo. Con mi mamá y una caja… sí." | risas |
| 5 | 20–26 s | Sala: Gloria gira la caja buscando qué dice. Vale se para de un salto | Gloria: "No dice nada: ni marca, ni qué es…" · Vale: "¡Son cositas de cocina!" · Gloria: "¿Cocina? ¿Ustedes cocinan?" | risas grandes |
| 6 | 26–31 s | **Confesionario Gloria** (la caja en las piernas, tranquila) | "Treinta y cinco años de casada. Yo sé muy bien qué son 'cositas de cocina'." (guiña) | risas + "uuuh" |
| 7 | 31–36 s | Placa `ancla_discreto_p4` | Voz de Vale: "Lo bueno: la caja llega sin marca y sin nombre del producto. Lo malo: llegó con mi suegra." | risas |
| 8 | 36–40 s | Sala: Gloria deja la maleta en el sofá y se sienta. Andrés y Vale se miran y miran a cámara | Gloria: "Bueno… me quedo una semanita, mijo." | silencio de 1 s + risas |
| 9 | 40–43 s | Placa `end_discreto` | — | tema de la serie |

**Por qué funciona**: remate cada 4-5 s (ritmo de sitcom), el producto nunca aparece (es la caja, que es el beneficio real), y el suspenso abre la Parte 5. Nada explícito: el chiste es lo que *no* se dice.

## Personajes con cara (solo opciones A y B) — crear primero en Flow (sección Personajes)

Mismo vestuario de la biblia; se agrega la cara. Una imagen de referencia por personaje, frontal, luz cálida:

- **Vale**: `Portrait photo, a Latina woman, 29, warm friendly face, light brown skin, big expressive dark eyes, natural makeup, long dark brown curly hair loose to mid-back, small gold hoop earrings, mustard-yellow oversized knit sweater, silver ring on her right index finger, cozy Bogotá apartment background, warm amber light, photorealistic, natural skin texture, no text, no logos.`
- **Andrés**: `Portrait photo, a Latino man, 31, kind slightly nervous expression, short dark hair faded on the sides, light beard, navy blue hoodie, black digital watch on his left wrist, cozy Bogotá apartment background, warm amber light, photorealistic, natural skin texture, no text, no logos.`
- **Doña Gloria**: `Portrait photo, a Latina woman in her late 50s, mischievous warm smile, short grey-streaked hair in a neat bob, burgundy cardigan, pearl stud earrings, cozy Bogotá apartment background, warm amber light, photorealistic, no text, no logos.`

## Prompts de Flow (opción A) — una sesión nueva por toma, ingredientes: apartment 2 + personajes

Plantilla fija al inicio de cada prompt:
`Vertical 9:16, TV sitcom look, natural performance, realistic acting, subtle facial expressions, warm amber light, small modern apartment in Bogotá at night with exposed brick wall, rainy window with city lights, grey sofa with mustard throw, monstera plant, boxes stacked in a corner. Casual clothes, no nudity, no text, no logos, no subtitles. Dialogue in Colombian Spanish (Bogotá accent).`

1. **S1 citófono**: `Wide static shot of the living room. Andrés stands by the door holding a white intercom handset, frozen. Vale on the sofa asks "¿Quién era?". He answers "El paquete." She smiles: "¡Ay, qué bien!". He adds slowly: "…y mi mamá." Vale's smile freezes.`
2. **C1 confesionario Vale**: `Medium close-up, Vale sits alone on the sofa hugging a mustard cushion and talks directly to the camera, dry humor, documentary style: "El paquete lo estábamos esperando hace una semana… a mi suegra, nadie." Small eye roll.`
3. **S2 llega Gloria**: `Medium shot at the apartment door. Doña Gloria walks in pulling a small floral suitcase, holding a plain brown cardboard box with no labels. She shakes the box next to her ear, curious: "Mijo, el portero me dio esto. ¿Qué es? Suena raro."`
4. **C2 confesionario Andrés**: `Medium close-up, Andrés sits alone on the sofa, talks to the camera, nervous, rubs the back of his neck: "Yo soy contador. Con los números no sudo. Con mi mamá y una caja… sí."`
5. **S3 cositas de cocina**: `Wide shot of the living room. Doña Gloria turns the plain brown box around looking for a label: "No dice nada: ni marca, ni qué es…". Vale jumps up from the sofa: "¡Son cositas de cocina!". Gloria raises an eyebrow: "¿Cocina? ¿Ustedes cocinan?"`
6. **C3 confesionario Gloria**: `Medium close-up, Doña Gloria sits on the sofa with the plain box on her lap, calm and amused, talks to the camera: "Treinta y cinco años de casada. Yo sé muy bien qué son cositas de cocina." She winks at the camera.`
7. **S4 la maleta**: `Wide shot. Doña Gloria places her floral suitcase on the sofa and sits down comfortably: "Bueno… me quedo una semanita, mijo." Andrés and Vale, standing, slowly look at each other, then both look straight into the camera, deadpan.`

Revisar en cada toma: que las caras sean las mismas de la referencia, que el español suene colombiano, esquinas redondeadas y bordes negros (zoom ≥1,08). Si una frase sale mal, se puede doblar solo ese pedazo con ElevenLabs cuando la boca no se vea.

## Opción C (sin caras): cambios a los prompts

Mismos 7 beats, con `seen from behind / over the shoulder / only hands, faces never visible` en lugar de los primeros planos. Los confesionarios: plano fijo del sofá vacío con el cojín mostaza (se reusa en los tres) y la voz de cada personaje con ElevenLabs ("Vale - XperienceLove", "Andrés - XperienceLove" y una voz nueva para Gloria: `Colombian woman from Bogotá, late 50s, warm, witty, maternal, slightly theatrical, clear diction`).

## Risas de público (sin derechos)

ElevenLabs → Efectos de sonido (gratis dentro de los créditos), 4 clips:
- `small TV studio audience laughing warmly, 3 seconds`
- `TV studio audience big laugh with a few claps, 4 seconds`
- `studio audience "ooooh" teasing reaction followed by laughter, 3 seconds`
- `short awkward silence then studio audience laughter, 4 seconds`

Se mezclan al 60 % justo después de cada remate; la música de la serie va solo en la apertura y el cierre.

## Caption

```
Recién mudados · Parte 4: La portería 📦
Cuando el pedido llega… con tu suegra incluida 😅
Lo bueno: la caja llega sin marca y sin nombre del producto. Nadie sabe qué hay adentro.
Comenta DISCRETO y te contamos cómo llega tu pedido.
Parte 4 de 8 · la anterior está en el perfil.

Historia y personajes inventados, situaciones muy reales. Escenas y voces creadas con IA.
#humordepareja #parejas #convivencia #suegra #bogota
```

## Métrica a las 48 h

Tasa de 3 s (meta ≥40 %) y retención al segundo 20. Si la versión con caras retiene más que las partes 1-3, la temporada sigue así.
