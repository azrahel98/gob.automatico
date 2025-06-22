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
        with open('publicacion.csv',mode="r",newline="",encoding="utf-8") as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                page.goto("https://www.gob.pe/admin2/informes-publicaciones/new")
                page.fill('#report_title',row[0])
                page.click('.choices[data-type="select-one"]')
                page.wait_for_selector('.choices__list--dropdown')
                page.click('#choices--report_publication_type_id-item-choice-32')
                page.wait_for_selector("trix-editor")
                page.eval_on_selector("input[name='report[body]']", "el => el.value = 'CONVOCATORIA PARA LA CONTRATACIÓN DE SERVICIOS'")
                page.set_input_files("input.file.required.js-documents-fields-file", row[1])
                page.select_option("#report_publication_3i",row[2]) # dia
                page.select_option("#report_publication_2i",row[3]) #mes
                page.select_option("#report_publication_1i",row[4]) # año
                page.select_option("#report_publication_4i",row[5]) # hora
                page.select_option("#report_publication_5i",row[6]) # minuto
                
                page.click('.choices[data-type="select-multiple"]')
                page.click('#choices--report_category_ids-item-choice-50')
                page.click('.choices[data-type="select-multiple"]')
                page.click('#choices--report_category_ids-item-choice-22')
                page.press('.choices[data-type="select-multiple"]', "Escape")
    
                page.click("#new_report > div > fieldset:nth-child(6) > div.input-control.select.optional.report_documents_collections > div > div > div.choices__inner__custom > input")

                page.keyboard.type("Convocatorias de Servicio 2025", delay=100)
                page.wait_for_timeout(500)
                page.click('#choices--report_documents_collection_ids-item-choice-1')
                page.click('input[value="Guardar y publicar"]')
                page.wait_for_timeout(1500)
                check = page.locator("body > div.yield.py-5.bg-white.flex-1 > div > div.flash.flex.success > div.flex-1",has_text="Se ha modificado la publicación")
                if check:
                    with open("resumen.txt", "a") as archivo:
                        archivo.write(f"El Memorando {row[0]} - se PUBLICO correctamente ✅ \n")
                else:
                    with open("resumen.txt", "a") as archivo:
                        archivo.write(f"❌ El Memorando {row[0]} - no se PUBLICO !!!! \n")
                        
                page.wait_for_load_state('networkidle')

    page.pause()