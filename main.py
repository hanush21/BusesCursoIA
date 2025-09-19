import flet as ft
from typing import List, Optional
from services import persistence as P
from services.bus import create_bus, update_bus, delete_bus, find_by_id as find_bus
from services.cliente import create_cliente, update_cliente, delete_cliente, find_by_id as find_cliente
from services.billetes_service import crear_billete, cancelar_billete, devolucio
from models.bus import Bus
from models.cliente import Cliente
from models.billetes import Billete
import os

def ensure_data_dir():
    os.makedirs(os.path.dirname(P.BUSES_FILE), exist_ok=True)
    for path, header in [
        (P.BUSES_FILE, "bus_id,placa,capacidad\n"),
        (P.CLIENTES_FILE, "cliente_id,nombre,apellido\n"),
        (P.BILLETES_FILE, "billete_id,bus_id,cliente_id,asiento,fecha\n"),
    ]:
        if not os.path.exists(path) or os.path.getsize(path) == 0:
            with open(path, "w", encoding="utf-8") as f:
                f.write(header)

def load_all():
    buses = P.cargar_buses()
    clientes = P.cargar_clientes()
    billetes = P.cargar_billetes(buses, clientes)
    return buses, clientes, billetes

def app(page: ft.Page):
    page.title = "Sistema de Buses – Flet"
    page.window_min_width = 980
    page.window_min_height = 700
    ensure_data_dir()

    buses: List[Bus]; clientes: List[Cliente]; billetes: List[Billete]
    buses, clientes, billetes = load_all()

    def save_all():
        P.guardar_buses(buses)
        P.guardar_clientes(clientes)
        P.guardar_billetes(billetes)

    def toast(msg: str):
        page.snack_bar = ft.SnackBar(ft.Text(msg))
        page.snack_bar.open = True
        page.update()

    # BUSES
    bus_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Placa")),
            ft.DataColumn(ft.Text("Capacidad")),
            ft.DataColumn(ft.Text("Ocupados")),
            ft.DataColumn(ft.Text("Libres")),
        ],
        rows=[],
    )
    placa_tf = ft.TextField(label="Placa", width=200)
    cap_tf = ft.TextField(label="Capacidad", width=150)
    bus_sel_id = ft.Text()

    def refresh_buses():
        bus_table.rows.clear()
        for b in buses:
            bus_table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(b.bus_id))),
                        ft.DataCell(ft.Text(b.placa)),
                        ft.DataCell(ft.Text(str(b.capacidad))),
                        ft.DataCell(ft.Text(str(len(b.billetes)))),
                        ft.DataCell(ft.Text(str(len(b.asientos_disponibles())))),
                    ],
                    on_select_changed=lambda e, b=b: select_bus(b),
                )
            )
        refresh_estado()
        page.update()

    def select_bus(b: Bus):
        bus_sel_id.value = str(b.bus_id)
        placa_tf.value = b.placa
        cap_tf.value = str(b.capacidad)
        page.update()

    def bus_add(e):
        try:
            if not placa_tf.value or not cap_tf.value:
                toast("Completa placa y capacidad")
                return
            bus = create_bus(buses, placa_tf.value.strip(), int(cap_tf.value))
            save_all()
            placa_tf.value = ""
            cap_tf.value = ""
            refresh_buses()
            toast(f"Bus creado: {bus.placa}")
        except Exception as ex:
            toast(str(ex))

    def bus_update(e):
        if not bus_sel_id.value:
            toast("Selecciona un bus en la tabla")
            return
        try:
            bid = int(bus_sel_id.value)
            new_placa = placa_tf.value.strip() if placa_tf.value else None
            new_cap = int(cap_tf.value) if cap_tf.value else None
            ok = update_bus(buses, bid, new_placa, new_cap)
            if ok:
                save_all()
                refresh_buses()
                toast("Bus actualizado")
            else:
                toast("Bus no encontrado")
        except Exception as ex:
            toast(str(ex))

    def bus_delete(e):
        if not bus_sel_id.value:
            toast("Selecciona un bus en la tabla")
            return
        try:
            bid = int(bus_sel_id.value)
            ok = delete_bus(buses, bid)
            if ok:
                save_all()
                bus_sel_id.value = ""
                placa_tf.value = ""
                cap_tf.value = ""
                refresh_buses()
                toast("Bus eliminado")
            else:
                toast("Bus no encontrado")
        except Exception as ex:
            toast(str(ex))

    buses_view = ft.Column([
        ft.Text("Buses", size=20, weight=ft.FontWeight.BOLD),
        bus_table,
        ft.Row([placa_tf, cap_tf, ft.ElevatedButton("Crear", on_click=bus_add),
                ft.ElevatedButton("Actualizar", on_click=bus_update),
                ft.OutlinedButton("Eliminar", on_click=bus_delete)]),
    ], expand=True)

    # CLIENTES
    cli_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Nombre")),
            ft.DataColumn(ft.Text("Apellido")),
        ],
        rows=[],
    )
    cli_sel_id = ft.Text()
    cli_nombre = ft.TextField(label="Nombre", width=200)
    cli_apellido = ft.TextField(label="Apellido", width=200)

    def refresh_clientes():
        cli_table.rows.clear()
        for c in clientes:
            cli_table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(c.cliente_id))),
                        ft.DataCell(ft.Text(c.nombre)),
                        ft.DataCell(ft.Text(c.apellido or "")),
                    ],
                    on_select_changed=lambda e, c=c: select_cliente(c),
                )
            )
        refresh_dropdowns()
        page.update()

    def select_cliente(c: Cliente):
        cli_sel_id.value = str(c.cliente_id)
        cli_nombre.value = c.nombre
        cli_apellido.value = c.apellido or ""
        page.update()

    def cli_add(e):
        if not cli_nombre.value:
            toast("Nombre requerido")
            return
        c = create_cliente(clientes, cli_nombre.value.strip(), cli_apellido.value.strip() or None)
        save_all()
        cli_nombre.value = ""
        cli_apellido.value = ""
        refresh_clientes()
        toast(f"Cliente creado: {c.nombre}")

    def cli_update(e):
        if not cli_sel_id.value:
            toast("Selecciona un cliente")
            return
        ok = update_cliente(clientes, int(cli_sel_id.value), cli_nombre.value.strip() or None, cli_apellido.value.strip() or None)
        if ok:
            save_all()
            refresh_clientes()
            toast("Cliente actualizado")
        else:
            toast("Cliente no encontrado")

    def cli_delete(e):
        if not cli_sel_id.value:
            toast("Selecciona un cliente")
            return
        try:
            ok = delete_cliente(clientes, int(cli_sel_id.value), billetes)
            if ok:
                save_all()
                cli_sel_id.value = ""
                cli_nombre.value = ""
                cli_apellido.value = ""
                refresh_clientes()
                toast("Cliente eliminado")
            else:
                toast("Cliente no encontrado")
        except Exception as ex:
            toast(str(ex))

    clientes_view = ft.Column([
        ft.Text("Clientes", size=20, weight=ft.FontWeight.BOLD),
        cli_table,
        ft.Row([cli_nombre, cli_apellido, ft.ElevatedButton("Crear", on_click=cli_add),
                ft.ElevatedButton("Actualizar", on_click=cli_update),
                ft.OutlinedButton("Eliminar", on_click=cli_delete)]),
    ], expand=True)

    # BILLETES
    dd_bus = ft.Dropdown(label="Bus", width=240)
    dd_cliente = ft.Dropdown(label="Cliente", width=240)
    dd_asiento = ft.Dropdown(label="Asiento (opcional)", width=200, hint_text="Vacío => auto")

    bil_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Bus")),
            ft.DataColumn(ft.Text("Cliente")),
            ft.DataColumn(ft.Text("Asiento")),
            ft.DataColumn(ft.Text("Fecha")),
        ],
        rows=[],
    )
    cancel_id = ft.TextField(label="Cancelar por ID", width=200)
    devolver_cant = ft.TextField(label="Devolver últimos N", width=200)

    def refresh_dropdowns():
        dd_bus.options = [ft.dropdown.Option(f"{b.bus_id}:{b.placa}") for b in buses]
        dd_cliente.options = [ft.dropdown.Option(f"{c.cliente_id}:{c.nombre}") for c in clientes]
        dd_bus.value = dd_bus.options[0].key if dd_bus.options else None
        dd_cliente.value = dd_cliente.options[0].key if dd_cliente.options else None
        refresh_asientos()
        page.update()

    def get_selected_bus() -> Optional[Bus]:
        if not dd_bus.value:
            return None
        bid = int(str(dd_bus.value).split(":")[0])
        return find_bus(buses, bid)

    def get_selected_cliente() -> Optional[Cliente]:
        if not dd_cliente.value:
            return None
        cid = int(str(dd_cliente.value).split(":")[0])
        return find_cliente(clientes, cid)

    def refresh_asientos():
        bus = get_selected_bus()
        opts = []
        if bus:
            for a in bus.asientos_disponibles():
                opts.append(ft.dropdown.Option(str(a)))
        dd_asiento.options = opts
        page.update()

    def refresh_billetes_table():
        bil_table.rows.clear()
        for b in sorted(billetes, key=lambda x: (x.bus.bus_id, x.asiento)):
            bil_table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(b.billete_id))),
                        ft.DataCell(ft.Text(f"{b.bus.bus_id}:{b.bus.placa}")),
                        ft.DataCell(ft.Text(f"{b.cliente.cliente_id}:{b.cliente.nombre}")),
                        ft.DataCell(ft.Text(str(b.asiento))),
                        ft.DataCell(ft.Text(b.fecha)),
                    ]
                )
            )
        refresh_estado()
        page.update()

    def vender(e):
        bus = get_selected_bus()
        cliente = get_selected_cliente()
        if not bus or not cliente:
            toast("Selecciona bus y cliente"); return
        asiento = int(dd_asiento.value) if dd_asiento.value else None
        ok, msg, _ = crear_billete(bus, cliente, billetes, asiento=asiento)
        toast(msg)
        if ok:
            save_all()
            refresh_asientos()
            refresh_buses()
            refresh_billetes_table()

    def cancelar_por_id(e):
        if not cancel_id.value:
            toast("Introduce ID de billete"); return
        try:
            bid = int(cancel_id.value)
            ok, msg = cancelar_billete(billetes, bid)
            toast(msg)
            if ok:
                save_all()
                refresh_asientos()
                refresh_buses()
                refresh_billetes_table()
                cancel_id.value = ""
                page.update()
        except Exception as ex:
            toast(str(ex))

    def devolver_lifo(e):
        if not devolver_cant.value:
            toast("Introduce cantidad"); return
        try:
            n = int(devolver_cant.value)
            ok, msg = devolucio(n, billetes, buses)
            toast(msg)
            if ok:
                save_all()
                refresh_asientos()
                refresh_buses()
                refresh_billetes_table()
                devolver_cant.value = ""
                page.update()
        except Exception as ex:
            toast(str(ex))

    billetes_view = ft.Column([
        ft.Text("Billetes", size=20, weight=ft.FontWeight.BOLD),
        ft.Row([dd_bus, dd_cliente, dd_asiento, ft.ElevatedButton("Vender", on_click=vender)]),
        bil_table,
        ft.Row([cancel_id, ft.ElevatedButton("Cancelar por ID", on_click=cancelar_por_id),
                devolver_cant, ft.OutlinedButton("Devolver últimos", on_click=devolver_lifo)]),
    ], expand=True)

    dd_bus.on_change = lambda e: refresh_asientos()

    # ESTADO
    stat_total = ft.Text()
    stat_libres = ft.Text()
    stat_vendidos = ft.Text()
    prog = ft.ProgressBar(width=400, value=0.0)

    def refresh_estado():
        total_plazas = sum(b.capacidad for b in buses)
        plazas_vendidas = len(billetes)
        plazas_libres = total_plazas - plazas_vendidas
        stat_total.value = f"Total de asientos: {total_plazas}"
        stat_libres.value = f"Plazas libres: {plazas_libres}"
        stat_vendidos.value = f"Plazas vendidas: {plazas_vendidas}"
        prog.value = (plazas_vendidas / total_plazas) if total_plazas else 0.0
        page.update()

    estado_view = ft.Column([
        ft.Text("Estado general", size=20, weight=ft.FontWeight.BOLD),
        stat_total, stat_libres, stat_vendidos,
        prog
    ], expand=True)

    tabs = ft.Tabs(
        selected_index=0,
        tabs=[
            ft.Tab(text="Buses", content=buses_view),
            ft.Tab(text="Clientes", content=clientes_view),
            ft.Tab(text="Billetes", content=billetes_view),
            ft.Tab(text="Estado", content=estado_view),
        ],
        expand=1
    )
    page.add(tabs)

    # Initial load
    refresh_buses()
    refresh_clientes()
    refresh_dropdowns()
    refresh_billetes_table()
    refresh_estado()

ft.app(target=app)
