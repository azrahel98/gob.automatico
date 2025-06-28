from playwright.sync_api import sync_playwright
import os
import csv
from pathlib import Path
from datetime import datetime

def check_login(page) -> bool:
    try:
        return page.query_selector("section > h1") is not None
    except:
        return False

def crear_archivos(csv_path: str):
    csv_file = Path(csv_path)
    if not csv_file.exists() or not csv_file.is_file():
        print(f"❌ El archivo '{csv_path}' no existe o no es válido.")
        return
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = p.chromium.launch_persistent_context(
            user_data_dir="./user-data",
            headless=False
        ) if not os.path.exists("sesion.json") else p.chromium.launch(headless=False).new_context(storage_state="sesion.json")

        page = context.new_page()
        page.goto("https://www.gob.pe/admin2")

        if not check_login(page):
            print("🔒 No logueado. Inicia sesión manualmente, luego ejecuta nuevamente.")
            page.pause()
            context.storage_state(path="sesion.json")
        else:
            with open(csv_file, mode="r", newline="", encoding="utf-8") as file, open("resumen.txt", "a", encoding="utf-8") as resumen:
                csv_reader = csv.reader(file)
                for index, row in enumerate(csv_reader, start=1):
                    hora = datetime.now().strftime("[%H:%M:%S] ")
                    mensaje = f"📄 Procesando fila {index}: {row[0]}."
                    print(mensaje)
                    resumen.write(mensaje + hora +"  "+"\n")
                    page.goto("https://www.gob.pe/admin2/informes-publicaciones?filters%5Brelated_institution%5D=own")
                    page.fill('#filters_words', row[0])
                    page.select_option("#filters_sort", value="title_asc")
                    page.press("input#filters_words", "Enter")
                    page.wait_for_load_state('networkidle')
                    enlaces = page.query_selector_all("td > div > div.ml-auto.flex > span.inline-block.mr-2 > a")

                    if len(enlaces) == 0:
                        mensaje = f"⚠️ El Memorando {row[0]} - NO se ENCONTRÓ\n\n"
                        print(mensaje)
                        resumen.write(mensaje)
                        continue

                    encontrado = False
                    for i, x in enumerate(enlaces):
                        href = x.get_attribute("href")
                        nmr = href.split("/edit?")
                        nmr[0] = nmr[0].replace("-pdf", "")
                        nombre = nmr[0].split("n-")
                        textoexacto = nombre[1].split("-")
                        textoexacto = "-".join(textoexacto[0:3]).strip().upper()
                        if textoexacto == row[0].strip().upper():
                            encontrado = True
                            nueva = context.new_page()
                            nueva.goto("https://www.gob.pe" + href)
                            nueva.wait_for_load_state()
                            nueva.click("a:has-text('Agregar documento')")

                            archivo = Path(row[1])
                            if not archivo.exists():
                                mensaje = f"🚫 Error: El archivo a subir '{archivo}' no existe.\n\n"
                                print(mensaje)
                                resumen.write(mensaje)
                                nueva.close()
                                break

                            nueva.set_input_files("input.file.required.js-documents-fields-file", row[1])
                            
                            with nueva.expect_navigation():
                                nueva.click('input[value="Guardar y publicar"]')
                            nueva.wait_for_load_state('networkidle')
                            try:
                                check = nueva.locator("div.flash.flex.success >> text=Se ha modificado la publicación")
                                if check.is_visible():
                                    mensaje = f"✅ El Memorando {row[0]} - se MODIFICÓ correctamente.\n"
                                else:
                                    mensaje = f"❌ El Memorando {row[0]} - NO se pudo verificar la modificación.\n"
                            except Exception as e:
                                mensaje = f"❌ El Memorando {row[0]} - ERROR al verificar modificación: {e}\n"
                            
                            print(mensaje)
                            resumen.write(mensaje.strip()+"\n\n")
                            nueva.close()
                        

                    if not encontrado:
                        mensaje = f"🚫 El Memorando {row[0]} - NO se encontró coincidencia exacta revisar que tenga solo 3 ('-')  xx-xx-xx.\n\n"
                        print(mensaje)
                        resumen.write(mensaje)
