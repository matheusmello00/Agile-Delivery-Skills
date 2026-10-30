<div align="center">

[English](README.md) · [Português](README.pt.md) · **🌐 Español**

<img src="assets/banner.svg" alt="Agile Delivery Skills — Matheus Mello" width="100%">

*Cinco skills de agile delivery que convierten los datos de tu tablero en un briefing listo para usar: preparación del backlog, bloqueos, planificación, retros y reviews.*

<a href="https://www.linkedin.com/in/matheusmello00/"><img src="https://img.shields.io/badge/LinkedIn-Conectar-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn"></a>
<a href="mailto:m.mello00@outlook.com"><img src="https://img.shields.io/badge/Email-Escr%C3%ADbeme-6D1A36?style=for-the-badge&logo=microsoftoutlook&logoColor=white" alt="Email"></a>
<a href="https://wa.me/351920102358"><img src="https://img.shields.io/badge/WhatsApp-Chatear-25D366?style=for-the-badge&logo=whatsapp&logoColor=white" alt="WhatsApp"></a>

<img src="https://img.shields.io/github/stars/matheusmello00/Agile-Delivery-Skills?label=Estrellas&style=flat-square&color=6B7B3A" alt="Estrellas">

</div>

---

## 🧭 Empieza por el trabajo que tienes delante

| Trae esto | Usa esta skill | Pide esto |
|---|---|---|
| El tope de tu backlog | `backlog-ready-check` | Verifica si los 20 primeros ítems están listos para el próximo sprint según nuestra Definition of Ready. |
| Un tablero con ítems bloqueados | `blocker-aging` | Muestra qué está bloqueado, durante cuántos días hábiles y qué escalar. |
| El próximo sprint y la capacidad del equipo | `planning-preparation` | Cruza capacidad con velocity, propone el alcance candidato y redacta un borrador de sprint goal. |
| Una retrospectiva próxima | `retro-preparation` | Prepara una retro basada en hechos: métricas, dos o tres temas candidatos y un formato adecuado. |
| Un sprint terminado | `review-demo-preparation` | Arma el briefing de review/demo agrupado por valor, con narrativa y presentadores. |

El asistente lee lo que le proporcionas, hace hasta cuatro preguntas si falta contexto y trabaja hacia el entregable. Indícale tablero o proyecto, sprint, equipo, objetivo y restricciones cuando puedas. Las skills son de solo lectura por defecto: informan, nunca modifican tu tracker.

## 🔌 Funciona con

Jira (Atlassian), Azure DevOps y ClickUp, mediante el conector de tracker (MCP) que tu asistente ya tiene. Cada skill incluye un `references/trackers.md` con el mapeo de consultas y campos. Responde en el idioma en que escribas. Los scripts incluidos usan Python 3.9+ con solo la biblioteca estándar.

> **Azure DevOps y ClickUp:** para funcionar bien fuera de Jira, añade los campos propios de la herramienta a la búsqueda (tipos y estados de los ítems, campo de estimación, marcador de bloqueo, sprint/iteración, criterios de aceptación) o indica sus nombres a la skill. Sin ellos la búsqueda puede perder ítems.

## 📦 Instalación

### Plugin de Claude Code

Ejecuta estos comandos dentro de Claude Code:

```text
/plugin marketplace add matheusmello00/Agile-Delivery-Skills
/plugin install agile-delivery@agile-delivery
```

Luego invoca una skill por el nombre del plugin:

```text
/agile-delivery:blocker-aging
Muéstrame qué está bloqueado en el tablero Checkout y qué debería escalarse.
```

El plugin contiene las 5 skills en `skills/`. No necesita API key ni servicio externo para leer sus instrucciones; tu asistente aporta el modelo y el conector de tracker.

### Codex o Cursor

Clona el repositorio y copia una skill a tu directorio personal de skills:

```bash
git clone https://github.com/matheusmello00/Agile-Delivery-Skills.git
mkdir -p ~/.agents/skills
cp -R Agile-Delivery-Skills/skills/blocker-aging ~/.agents/skills/
```

Para instalar las 5, reemplaza el último comando por:

```bash
cp -R Agile-Delivery-Skills/skills/* ~/.agents/skills/
```

Revisa si ya existen carpetas con el mismo nombre antes de copiar; copiar puede sobrescribir archivos. Para uso en equipo, copia en `.agents/skills/` dentro de tu proyecto. En Codex, invoca `$blocker-aging`; en Cursor, usa `/blocker-aging` o describe la tarea para que el asistente elija la skill.

### Claude Code sin el plugin

Tras clonar, usa `~/.claude/skills/` para skills personales o `.claude/skills/` para skills de proyecto:

```bash
mkdir -p ~/.claude/skills
cp -R Agile-Delivery-Skills/skills/blocker-aging ~/.claude/skills/
```

Invoca `/blocker-aging`. Elige el plugin o el método de copia, no ambos, para evitar instalaciones duplicadas.

### Otros asistentes, incluido ChatGPT

Abre el `SKILL.md` correspondiente y entrégaselo junto con tu trabajo. Incluye los archivos de `references/` de esa skill (y `scripts/` si puedes ejecutar Python) para tener todo el material de apoyo. El descubrimiento automático depende del asistente; clonar este repositorio no instala las skills en todos los productos.

## 👤 Autor

Creado por [Matheus Mello](https://github.com/matheusmello00) 
