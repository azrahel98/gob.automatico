from playwright.sync_api import sync_playwright
import os
import csv

def check_login(page) -> bool:
    try:
        return page.query_selector("section > h1") is not None
    except:
        return False

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
        with open('resultado.csv',mode="r",newline="",encoding="utf-8") as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                page.goto("https://www.gob.pe/admin2/informes-publicaciones?filters%5Brelated_institution%5D=own")
                page.fill('#filters_words',row[0])
                page.select_option("#filters_sort",value="title_asc")
                page.press("input#filters_words", "Enter")
                page.wait_for_load_state('networkidle')
                enlaces = page.query_selector_all("td > div > div.ml-auto.flex > span.inline-block.mr-2 > a")
                if len(enlaces) == 0:
                    with open("resumen.txt", "a", encoding="utf-8") as archivo:
                        archivo.write(f"⚠️ El Memorando {row[0]} - no se ENCONTRO \n")
                for i, x in enumerate(enlaces):
                    href = x.get_attribute("href")
                    nmr = href.split("/edit?")
                    nmr[0] = nmr[0].replace("-pdf","")
                    nombre = nmr[0].split("n-")
                    textoexacto = nombre[1].split("-")
                    textoexacto = "-".join(textoexacto[0:3]).strip().upper()
                    if textoexacto == row[0].strip().upper():
                        nueva = context.new_page()
                        nueva.goto("https://www.gob.pe" + href)
                        nueva.wait_for_load_state()
                        nueva.click("a:has-text('Agregar documento')")
                        nueva.set_input_files("input.file.required.js-documents-fields-file", row[1])
                        nueva.click('input[value="Guardar y publicar"]')
                        nueva.wait_for_load_state('networkidle')
                        page.wait_for_timeout(1000)
                        check = nueva.locator("div.flash.flex.success >> text=Se ha modificado la publicación")
                        try:
                            check = nueva.locator("div.flash.flex.success >> text=Se ha modificado la publicación")
                            mensaje = f"El Memorando {row[0]} - se MODIFICÓ correctamente ✅\n" if check.is_visible() \
                                    else f"❌ El Memorando {row[0]} - NO se modificó.\n"
                        except Exception as e:
                                ensaje = f"❌ El Memorando {row[0]} - ERROR al verificar modificación: {e}\n"
                        finally:
                            with open("resumen.txt", "a", encoding="utf-8") as archivo:
                                archivo.write(mensaje)
                        nueva.close()
             