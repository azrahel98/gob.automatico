# 🤖 Automatización de Publicaciones en gob.pe

---

Este proyecto es una **herramienta de automatización** desarrollada con **Python y Playwright** que simplifica la gestión de publicaciones en el portal oficial del Estado Peruano, [gob.pe](https://www.gob.pe).

Sus funcionalidades principales incluyen:

- **Registro de Nuevas Publicaciones:** Automatiza el proceso de subir nuevos informes o documentos al portal.
- **Adición de Documentos a Publicaciones Existentes:** Permite adjuntar archivos adicionales a publicaciones ya existentes.

---

## ⚙️ Requisitos y Configuración

Para utilizar esta herramienta, asegúrate de tener **Python 3.8 o superior** y **Playwright** instalados.

### Instalación

Sigue estos pasos para configurar tu entorno:

1.  **Clona este repositorio** (si aún no lo has hecho).
2.  **Crea un entorno virtual**:

    ```bash
    python -m venv .venv
    ```

3.  **Activa el entorno virtual**:

    - **En Linux/macOS:**
      ```bash
      source .venv/bin/activate
      ```
    - **En Windows:**
      ```bash
      .venv\Scripts\activate
      ```

4.  **Instala las dependencias de Python** del proyecto:

    ```bash
    pip install -r requirements.txt
    ```

5.  **Instala los navegadores necesarios para Playwright**:

    ```bash
    playwright install
    ```

---

## 🚀 Uso

El script ofrece dos modos de operación principales: `publicar` para subir nuevos informes y `modificar` para añadir documentos a publicaciones existentes.

### 📤 Publicar Nuevas Publicaciones

Para publicar nuevos informes, necesitas preparar un archivo CSV llamado `publicacion.csv`. Cada fila en este archivo debe representar una publicación y contener **siete campos** separados por comas, siguiendo este orden y formato:

| Nº  | Campo          | Descripción                                     |
| :-- | :------------- | :---------------------------------------------- |
| 0   | `Título`       | Nombre completo del documento a publicar.       |
| 1   | `Ruta Archivo` | **Ruta completa** al archivo PDF en tu sistema. |
| 2   | `Día`          | Día de publicación (ej. `24`).                  |
| 3   | `Mes`          | Mes de publicación (ej. `6`).                   |
| 4   | `Año`          | Año de publicación (ej. `2025`).                |
| 5   | `Hora`         | Hora de publicación (formato 24h, ej. `08`).    |
| 6   | `Minuto`       | Minuto de publicación (ej. `00`).               |

**Ejemplo de una línea en `publicacion.csv`:**

```csv
Documento de Algo N° xx-xx-x,\\xxx.pdf,24,6,2025,08,00
```

### 📤 Aregar nuevos documentos a informes existentes

Para documentos nuevos a informes ya creados, necesitas preparar un archivo CSV llamado `resultado.csv`. Cada fila en este archivo debe representar una publicación y contener **dos campos** separados por comas, siguiendo este orden y formato:

| Nº  | Campo          | Descripción                                           |
| :-- | :------------- | :---------------------------------------------------- |
| 0   | `Text  `       | Campo de busqueda dentro de informes y publicaciones. |
| 1   | `Ruta Archivo` | **Ruta completa** al archivo PDF en tu sistema.       |

**Ejemplo de una línea en `resultado.csv`:**

```csv
xx-2025-xx,\\xxx.pdf
```
