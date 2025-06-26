import os
import csv
from pathlib import Path
from playwright.sync_api import sync_playwright

def check_login(page) -> bool:
    try:
        return page.query_selector("section > h1") is not None
    except:
        return False

def crear_publicaciones(csv_path: str):
    csv_file = Path(csv_path)
    if not csv_file.exists() or not csv_file.is_file():
        print(f"❌ El archivo '{csv_path}' no existe o no es válido.")
        return

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        if not os.path.exists("sesion.json"):
            context = p.chromium.launch_persistent_context(
                user_data_dir="./user-data",
                headless=False
            )
        else:
            context = p.chromium.launch(headless=False).new_context(storage_state="sesion.json")

        page = context.new_page()
        page.goto("https://www.gob.pe/admin2")

        if not check_login(page):
            print("🔒 No logueado. Inicia sesión manualmente, luego ejecuta nuevamente.")
            page.pause()
            context.storage_state(path="sesion.json")
            return
        with open(csv_file, mode="r", newline="", encoding="utf-8") as file, open("resumen.txt", "a", encoding="utf-8") as resumen:
            csv_reader = csv.reader(file)
            for index, row in enumerate(csv_reader, start=1):
                mensaje = f"📄 Procesando fila {index}: {row[0]}."
                print(mensaje)
                resumen.write(mensaje + "\n")

                try:
                    page.goto("https://www.gob.pe/admin2/informes-publicaciones/new")

                    page.fill('#report_title', row[0])
                    page.click('.choices[data-type="select-one"]')
                    page.wait_for_selector('.choices__list--dropdown')
                    page.click('#choices--report_publication_type_id-item-choice-32')
                    page.wait_for_selector("trix-editor")
                    page.eval_on_selector("input[name='report[body]']", "el => el.value = 'CONVOCATORIA PARA LA CONTRATACIÓN DE SERVICIOS'")

                    archivo = Path(row[1])
                    if not archivo.exists():
                        mensaje = f"❌ Error: El archivo a subir '{archivo}' no existe."
                        print(mensaje)
                        resumen.write(mensaje + "\n\n")
                        continue

                    page.set_input_files("input.file.required.js-documents-fields-file", row[1])

                    page.select_option("#report_publication_3i", row[2])
                    page.select_option("#report_publication_2i", row[3])
                    page.select_option("#report_publication_1i", row[4])
                    page.select_option("#report_publication_4i", row[5])
                    page.select_option("#report_publication_5i", row[6])

                    page.click('.choices[data-type="select-multiple"]')
                    page.click('#choices--report_category_ids-item-choice-50')
                    page.click('.choices[data-type="select-multiple"]')
                    page.click('#choices--report_category_ids-item-choice-22')
                    page.press('.choices[data-type="select-multiple"]', "Escape")

                    page.click("#new_report > div > fieldset:nth-child(6) > div.input-control.select.optional.report_documents_collections > div > div > div.choices__inner__custom > input")
                    page.keyboard.type("Convocatorias de Servicio 2025", delay=50)
                    page.wait_for_timeout(500)
                    page.click('#choices--report_documents_collection_ids-item-choice-1')

                    #page.click('input[value="Guardar y publicar"]')
                    page.wait_for_load_state('networkidle')
                    page.wait_for_timeout(1000)

                    check = page.locator(
                        "body > div.yield.py-5.bg-white.flex-1 > div > div.flash.flex.success > div.flex-1",
                        has_text="Se ha modificado la publicación"
                    )
                    if check.is_visible():
                        mensaje = f"✅ {row[0]}: publicación realizada correctamente."
                    else:
                        mensaje = f"❌ {row[0]}: no se pudo verificar la publicación."

                except Exception as e:
                    mensaje = f"⚠️ {row[0]}: ocurrió un error al procesar la fila. No se publicó. Detalle: {str(e)}"

                print(mensaje)
                resumen.write(mensaje + "\n\n")
