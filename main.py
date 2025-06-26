# cli.py
import click
from pathlib import Path
import os
from src.publicacion import crear_publicaciones
from src.resultado import crear_archivos


@click.group()
def cli():
    """Herramienta para subir documentos al portal gob.pe"""

@cli.command()
@click.option('--csv', help='Ruta al archivo CSV donde estan las publicaciones',required=True)
def publicacion_cmd(csv):
    """Crear nuevas publicaciones en el portal"""
    
    filepath = os.path.abspath(csv)
    file = Path(filepath)
    
    if not file.exists():
        raise click.ClickException(f"❌ Error: El archivo '{file}' no existe.")
    
    if not file.is_file():
        raise click.ClickException(f"❌ Error: La ruta '{file}' no apunta a un archivo.")
    
    if file.suffix.lower() != '.csv':
        click.secho(f"⚠️ Advertencia: La extensión del archivo '{file}' no es .csv. Podría no ser un CSV.", fg="yellow")

    click.secho("✅ Archivo CSV validado correctamente.", fg="green")
    
    crear_publicaciones(csv_path=file)
    

@cli.command()
@click.option('--csv', help='Ruta al archivo CSV donde estan las resultados',required=True)
def resultado_cmd(csv):
    """Agregar archivos a publicaciones ya creadas \n
    Tener en cuenta que la primera fila siempre debe de tener este formato xx-xx-xx 
    \n\nEjm: 123-2025-algo
    """
    
    filepath = os.path.abspath(csv)
    file = Path(filepath)
    
    if not file.exists():
        raise click.ClickException(f"❌ Error: El archivo '{file}' no existe.")
    
    if not file.is_file():
        raise click.ClickException(f"❌ Error: La ruta '{file}' no apunta a un archivo.")
    
    if file.suffix.lower() != '.csv':
        click.secho(f"⚠️ Advertencia: La extensión del archivo '{file}' no es .csv. Podría no ser un CSV.", fg="yellow")

    click.secho("✅ Archivo CSV validado correctamente.", fg="green")
    
    crear_archivos(csv_path=file)

if __name__ == '__main__':
    cli()
