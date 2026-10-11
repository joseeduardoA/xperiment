
import flet as ft
import flet_geolocator as ftg


async def main(page: ft.Page):
    page.title = "Rastreador GPS"
    page.padding = 20
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    txt_lat = ft.Text("Latitud: --", size=18)
    txt_lon = ft.Text("Longitud: --", size=18)
    txt_acc = ft.Text("Precisión: --", size=18)

    estado = ft.Text("Estado: Inactivo", color=ft.Colors.GREY)
    btn_gps = ft.Button("Obtener ubicación")

    def mostrar_error(e):
        estado.value = f"Error GPS: {e.data}"
        estado.color = ft.Colors.RED
        page.update()

    def actualizar_posicion(e: ftg.GeolocatorPositionChangeEvent):
        p = e.position
        txt_lat.value = f"Latitud: {p.latitude}"
        txt_lon.value = f"Longitud: {p.longitude}"
        txt_acc.value = f"Precisión: {p.accuracy} metros"
        estado.value = "Ubicación actualizada"
        estado.color = ft.Colors.GREEN
        page.update()

    
    geo = ftg.Geolocator(
        configuration=ftg.GeolocatorConfiguration(
            accuracy=ftg.GeolocatorPositionAccuracy.HIGH,
            distance_filter=0,
        ),
        on_position_change=actualizar_posicion,
        on_error=mostrar_error,
    )
    
    page.services.append(geo)


    async def obtener_ubicacion(e):
        btn_gps.disabled = True
        estado.value = "Comprobando permisos..."
        estado.color = ft.Colors.BLUE
        page.update()

        try:
            permiso = await geo.request_permission()
            permiso_txt = str(permiso).lower()
            
            if not (
                "while_in_use" in permiso_txt
                or "always" in permiso_txt
            ):
                estado.value = f"Permiso de ubicación no concedido: {permiso}"
                estado.color = ft.Colors.RED
                return


            servicio_activo = await geo.is_location_service_enabled()

            if not servicio_activo:
                estado.value = "Activa la ubicación del teléfono e inténtalo de nuevo."
                estado.color = ft.Colors.RED
                return

            estado.value = "Buscando ubicación..."
            page.update()

            p = await geo.get_current_position()

            txt_lat.value = f"Latitud: {p.latitude}"
            txt_lon.value = f"Longitud: {p.longitude}"
            txt_acc.value = f"Precisión: {p.accuracy} metros"
            estado.value = "Ubicación obtenida correctamente"
            estado.color = ft.Colors.GREEN

        except Exception as ex:
            estado.value = f"Error: {type(ex).__name__}: {ex}"
            estado.color = ft.Colors.RED

        finally:
            btn_gps.disabled = False
            page.update()

    btn_gps.on_click = obtener_ubicacion

    page.add(
        ft.Column(
            controls=[
                ft.Text(
                    "Rastreador GPS Flet",
                    size=24,
                    weight=ft.FontWeight.BOLD,
                ),
                estado,
                txt_lat,
                txt_lon,
                txt_acc,
                btn_gps,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15,
        )
    )


if __name__ == "__main__":
    ft.run(main)
