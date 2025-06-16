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
        with open('descarga.csv',mode="r",newline="",encoding="utf-8") as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                page.goto("https://www.gob.pe/admin2/informes-publicaciones?filters%5Brelated_institution%5D=own")
                page.fill('#filters_words',row[0])
                page.press("input#filters_words", "Enter")
                page.wait_for_timeout(2000)
                enlaces = page.query_selector_all("td > div > div.ml-auto.flex > span.inline-block.mr-2 > a")
                for i, x in enumerate(enlaces):
                    if i == 0:
                        href = x.get_attribute("href")
                        if href:
                            nueva = context.new_page()
                            nueva.goto("https://www.gob.pe" + href)
                            nueva.wait_for_load_state()
                            nueva.click("a:has-text('Agregar documento')")
                            nueva.set_input_files("input.file.required.js-documents-fields-file", row[1])
                            nueva.click('input[value="Guardar y publicar"]') 
                            # Esta linea de arriba lo que hace es guardar la publicacion
                            nueva.wait_for_load_state('networkidle')
                            # con esto esperamos que la pagina cargue y suba el archivo  para poder recien cerrarla
                            nueva.close()
                        else:
                            continue
                    continue
    page.pause()