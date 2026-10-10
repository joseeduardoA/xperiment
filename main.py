import flet as ft
from plyer import gps
import threading

def main(page: ft.Page):
    page.title = "GPS con Flet y Plyer"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 20

    # Elementos de la interfaz gráfica
    txt_lat = ft.Text("Latitud: --", size=18)
    txt_lon = ft.Text("Longitud: --", size=18)
    txt_acc = ft.Text("Precisión: --", size=18)
    status_text = ft.Text("Estado: Inactivo", italic=True, color=ft.Colors.GREY)

    def actualizar_ui(lat, lon, acc):
        txt_lat.value = f"Latitud: {lat}"
        txt_lon.value = f"Longitud: {lon}"
        txt_acc.value = f"Precisión: {acc} metros"
        page.update()

    def on_location(**kwargs):
        lat = kwargs.get('lat', 'N/A')
        lon = kwargs.get('lon', 'N/A')
        acc = kwargs.get('accuracy', 'N/A')
        actualizar_ui(lat, lon, acc)

    def on_status(stype, status):
        status_text.value = f"Estado GPS: {status}"
        page.update()

    def iniciar_gps(e):
        try:
            status_text.value = "Buscando señal GPS..."
            page.update()
            
            # Configurar e iniciar Plyer GPS
            gps.configure(on_location=on_location, on_status=on_status)
            gps.start(minTime=1000, minDistance=1)
        except NotImplementedError:
            status_text.value = "Error: GPS no soportado en este dispositivo."
            page.update()

    btn_iniciar = ft.TextButton("Activar GPS en Vivo", on_click=iniciar_gps)

    page.add(
        ft.Column(
            [
                ft.Text("Rastreador GPS Flet", size=22, weight=ft.FontWeight.BOLD),
                status_text,
                txt_lat,
                txt_lon,
                txt_acc,
                btn_iniciar
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15
        )
    )
if __name__ == "__main__":
    ft.run(main)
