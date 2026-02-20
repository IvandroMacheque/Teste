import flet as ft
import data_service as ds
import pandas as pd
import utils
import time

def ApartmentsView(page: ft.Page):
    # --- State ---
    current_filter = "Todos"

    item_selecionado = [] 
    apto_origem = []
    
    txt_nome_item = ft.Text("", weight="bold", size=16)
    campo_qtd = ft.TextField(label="Quantidade", width=150)
    drop_destino = ft.Dropdown(label="Destino", width=250)
    campo_obs = ft.TextField(label="Observação (Opcional)")

    # Função para salvar a transferência
    def salvar_transferencia(e):
        try:
            if not campo_qtd.value or not drop_destino.value:
                page.snack_bar = ft.SnackBar(ft.Text("Preencha quantidade e destino!"))
                page.snack_bar.open = True
                page.update()
                return

            ds.add_movement(
                item_id=item_selecionado[0]["id"],
                origem_id=apto_origem[0]["id"],
                destino_id=int(drop_destino.value),
                quantidade=float(campo_qtd.value),
                tipo="Transferência",
                observacao=campo_obs.value
            )

            modal_transferir.open = False
            open_inventory(apto_origem[0])
            page.snack_bar = ft.SnackBar(ft.Text("Transferência concluída!"), bgcolor="green")
            page.snack_bar.open = True
            page.update()
        except Exception as ex:
            print(f"Erro: {ex}")

    # O "Caixote" (Modal)
    modal_transferir = ft.AlertDialog(
        title=ft.Text("Transferir Item"),
        content=ft.Column([txt_nome_item, campo_qtd, drop_destino, campo_obs], tight=True),
        actions=[
            ft.TextButton("Cancelar", on_click=lambda _: setattr(modal_transferir, "open", False) or page.update()),
            ft.ElevatedButton("Confirmar", on_click=salvar_transferencia)
        ]
    )
    page.overlay.append(modal_transferir)

    def abrir_transferencia(item, apt):
        item_selecionado.clear()
        item_selecionado.append(item)
        apto_origem.clear()
        apto_origem.append(apt)

        txt_nome_item.value = f"Item: {item['nome']}"
        campo_qtd.value = ""
        campo_obs.value = ""
        
        drop_destino.options = [
            ft.dropdown.Option(str(loc["id"]), loc["nome"]) 
            for loc in ds.locations if loc["id"] != apt["id"] and loc["ativo"]
        ]
        
        modal_transferir.open = True
        page.update()

    # --- UI Refs ---
    grid_container = ft.Container()
    
    search_field = ft.TextField(
        label="Pesquisar apartamentos...",
        prefix_icon=ft.Icons.SEARCH,
        on_change=lambda _: render_list(),
        expand=True
    )
    
    # --- Modals ---
    # 1. New Apartment Modal
    new_apt_name = ft.TextField(label="Nome do Apartamento")
    new_apt_status = ft.Dropdown(
        label="Status Inicial",
        options=[ft.dropdown.Option("DISPONIVEL"), ft.dropdown.Option("OCUPADO")],
        value="DISPONIVEL"
    )

    def save_new_apartment(e):
        e.control.disabled = True
        page.update()
        
        new_apt_name.error_text = None
        if not new_apt_name.value:
            new_apt_name.error_text = "Campo obrigatório"
            e.control.disabled = False
            page.update()
            return
        ds.add_apartment(new_apt_name.value, new_apt_status.value)
        new_apt_dialog.open = False
        new_apt_name.value = ""
        render_list()
        page.snack_bar = ft.SnackBar(ft.Text("Apartamento cadastrado com sucesso!"))
        page.snack_bar.open = True
        page.update()

    new_apt_dialog = ft.AlertDialog(
        title=ft.Text("Novo Apartamento"),
        content=ft.Container(
            content=ft.Column([new_apt_name, new_apt_status], tight=True),
            width=600
        ),
        actions=[
            ft.TextButton("Cancelar", on_click=lambda _: setattr(new_apt_dialog, "open", False) or page.update()),
            ft.ElevatedButton("Salvar", on_click=save_new_apartment, bgcolor=ft.Colors.BLUE_700, color=ft.Colors.WHITE),
        ]
    )
    page.overlay.append(new_apt_dialog)

    # 2. Inventory Modal
    inventory_table = ft.Column()
    current_apt_for_export = None

    def on_file_result(e: ft.FilePickerResultEvent):
        if e.path and current_apt_for_export:
            try:
                save_inventory_excel(e.path, current_apt_for_export)
                page.snack_bar = ft.SnackBar(ft.Text(f"Inventário exportado com sucesso: {e.path}"), bgcolor=ft.Colors.GREEN_700)
            except Exception as ex:
                page.snack_bar = ft.SnackBar(ft.Text(f"Erro ao exportar: {str(ex)}"), bgcolor=ft.Colors.RED_700)
            page.snack_bar.open = True
            page.update()

    # file_picker = ft.FilePicker(on_result=on_file_result)
    # page.overlay.append(file_picker)

    def save_inventory_excel(apt):
        try:
            filename = f"inventario_{apt['nome'].replace(' ', '_').lower()}.xlsx"
            export_path = os.path.join(utils.get_exports_dir(), filename)
            
            data = []
            # Forçamos a busca de todos os itens para checar o saldo deste apartamento
            for item in ds.get_items():
                balance = ds.get_balance(item["id"], apt["id"])
                if balance > 0:
                    data.append({
                        "Item": item["nome"],
                        "Categoria": item.get("categoria") or "Geral",
                        "Quantidade": balance
                    })
            
            if not data:
                data.append({"Item": "Nenhum item encontrado", "Categoria": "-", "Quantidade": 0})

            df = pd.DataFrame(data)
            df.to_excel(export_path, index=False, engine='openpyxl')
            return filename
        except Exception as e:
            raise Exception(f"Erro ao gerar inventário: {str(e)}")

    def open_inventory(apt):
        is_dark = page.theme_mode == ft.ThemeMode.DARK
        
        def build_inventory_card(item, balance):
            return ft.Container(
                content=ft.Row([
                    ft.Text(item["nome"], size=14, weight="bold", expand=True),
                    ft.Text(item["categoria"] or "Geral", size=12, color=ft.Colors.GREY_500, width=120),
                    ft.Container(content=ft.Text(str(balance), size=14, weight="bold"), width=60, alignment=ft.alignment.center),
                    ft.IconButton(
                        icon=ft.Icons.SEND_ROUNDED, 
                        icon_size=18, 
                        on_click=lambda _: abrir_transferencia(item, apt)
                    ),
                ])
            )

        cards = []
        itens_ordenados = sorted(
            ds.items, 
            key=lambda x: (x.get("categoria") or "Geral", x["nome"].lower())
        )
        
        ultima_categoria = None

        for item in itens_ordenados:
            balance = ds.get_balance(item["id"], apt["id"])
            
            if balance > 0:
                categoria_atual = item.get("categoria") or "Geral"

                if categoria_atual != ultima_categoria:
                    if ultima_categoria is not None:
                        cards.append(ft.Container(height=10)) 
                    
                    cards.append(
                        ft.Container(
                            content=ft.Row([
                                ft.Icon(ft.icons.LABEL_IMPORTANT, color=ft.Colors.BLUE_700, size=20),
                                ft.Text(categoria_atual.upper(), size=14, weight="bold", color=ft.Colors.BLUE_700),
                            ]),
                            padding=ft.padding.only(top=10, bottom=5),
                        )
                    )
                    cards.append(ft.Divider(height=1, color=ft.Colors.BLUE_200))
                    
                    ultima_categoria = categoria_atual
                cards.append(build_inventory_card(item, balance))

        
        inventory_table.controls = [
            ft.Container(content=ft.Row([
                ft.Text("ITEM", size=10, weight="bold", color=ft.Colors.GREY_500, expand=True),
                ft.Text("CATEGORIA", size=10, weight="bold", color=ft.Colors.GREY_500, width=120),
                ft.Text("QTDE", size=10, weight="bold", color=ft.Colors.GREY_500, width=60, text_align=ft.TextAlign.CENTER),
            ]), padding=ft.padding.symmetric(horizontal=12)) if cards else ft.Container(),
            ft.Column(cards, spacing=5, scroll=ft.ScrollMode.AUTO, height=400) if cards else ft.Text("Nenhum item neste apartamento.", italic=True)
        ]
        
        inventory_dialog.actions = [
            ft.TextButton("Fechar", on_click=lambda _: setattr(inventory_dialog, "open", False) or page.update()),
            ft.ElevatedButton(
                "Transferir Item", 
                on_click=lambda _: (
                    setattr(inventory_dialog, "open", False),
                    page.change_view(1, initial_data={
                        "origem_id": apt["id"],
                        "tipo": "Transferência"
                    })
                ),
                bgcolor=ft.Colors.BLUE_700,
                color=ft.Colors.WHITE
            ),
            ft.ElevatedButton(
                "Exportar Relatório", 
                on_click=lambda _: export_inventory_click(apt),
                icon=ft.Icons.FILE_DOWNLOAD
            ),
        ]
        
        inventory_dialog.title = ft.Text(f"Inventário - {apt['nome']}")
        inventory_dialog.open = True
        page.update()

    def export_inventory_click(apt):
        page.snack_bar = ft.SnackBar(ft.Text("Gerando relatório..."), bgcolor=ft.Colors.BLUE_700)
        page.snack_bar.open = True
        page.update()
        try:
            filename = save_inventory_excel(apt)
            download_url = utils.get_download_url(filename)
            page.launch_url(f"{download_url}?_={int(time.time())}", web_window_name="_blank")
            page.snack_bar = ft.SnackBar(ft.Text("Download iniciado!"), bgcolor=ft.Colors.GREEN_700)
        except Exception as ex:
            page.snack_bar = ft.SnackBar(ft.Text(f"Erro ao exportar: {str(ex)}"), bgcolor=ft.Colors.RED_700)
        page.snack_bar.open = True
        page.update()

    inventory_dialog = ft.AlertDialog(
        title=ft.Text("Inventário"),
        content=ft.Container(content=inventory_table, width=600),
    )
    page.overlay.append(inventory_dialog)

    # --- Actions ---
    def toggle_status(apt):
        ds.toggle_apartment_status(apt["id"])
        render_list()
        page.update()

    def toggle_active(apt):
        ds.toggle_apartment_active(apt["id"])
        render_list()
        page.update()

    def set_filter(e):
        nonlocal current_filter
        current_filter = e.control.text
        render_list()
        page.update()

    # --- Render ---
    def render_list():
        search_query = search_field.value.lower() if search_field.value else ""
        cards = []
        filtered_locations = [l for l in ds.locations if l["tipo"] == "APARTAMENTO"]
        
        # Filter by search
        if search_query:
            filtered_locations = [
                l for l in filtered_locations 
                if search_query in l["nome"].lower()
            ]

        # Ordenar por nome
        filtered_locations.sort(key=lambda x: x["nome"].lower())

        if current_filter == "Ocupados":
            filtered_locations = [l for l in filtered_locations if l["status_ocupacao"] == "OCUPADO" and l["ativo"]]
        elif current_filter == "Disponíveis":
            filtered_locations = [l for l in filtered_locations if l["status_ocupacao"] == "DISPONIVEL" and l["ativo"]]
        elif current_filter == "Inativos":
            filtered_locations = [l for l in filtered_locations if not l["ativo"]]
        else: # Todos
            pass

        for apt in filtered_locations:
            status_color = ft.Colors.GREEN_700 if apt["status_ocupacao"] == "DISPONIVEL" else ft.Colors.ORANGE_700
            if not apt["ativo"]: status_color = ft.Colors.RED_700
            
            cards.append(
                ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Text(apt["nome"], size=18, weight=ft.FontWeight.BOLD),
                            ft.Container(
                                content=ft.Text(
                                    "INATIVO" if not apt["ativo"] else apt["status_ocupacao"], 
                                    size=12, color=ft.Colors.WHITE
                                ),
                                bgcolor=status_color,
                                padding=ft.padding.symmetric(horizontal=10, vertical=2),
                                border_radius=10
                            )
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        ft.Divider(),
                        ft.Row([
                            ft.TextButton("Ver Inventário", icon=ft.Icons.INVENTORY, on_click=lambda e, a=apt: open_inventory(a)),
                            ft.IconButton(
                                ft.Icons.SWAP_HORIZ, 
                                tooltip="Alterar Status", 
                                on_click=lambda e, a=apt: toggle_status(a),
                                disabled=not apt["ativo"]
                            ),
                            ft.IconButton(
                                ft.Icons.PLAY_ARROW if not apt["ativo"] else ft.Icons.DELETE_FOREVER, 
                                tooltip="Ativar" if not apt["ativo"] else "Desativar", 
                                icon_color=ft.Colors.GREEN_400 if not apt["ativo"] else ft.Colors.RED_300,
                                on_click=lambda e, a=apt: toggle_active(a),
                            ),
                        ], alignment=ft.MainAxisAlignment.END)
                    ]),
                    padding=15,
                    border=ft.border.all(1, ft.Colors.GREY_800 if page.theme_mode == ft.ThemeMode.DARK else ft.Colors.GREY_300),
                    border_radius=10,
                    bgcolor="#1E1E1E" if page.theme_mode == ft.ThemeMode.DARK else ft.Colors.WHITE,
                    width=350,
                )
            )
        
        new_content = ft.ResponsiveRow(
            [ft.Column([c], col={"sm": 12, "md": 4, "lg": 3}) for c in cards],
            spacing=20,
            run_spacing=20
        )
        
        # Update the grid container with animation
        grid_container.content = new_content
        page.update()

    # --- Filters ---
    def on_filter_change(e):
        nonlocal current_filter
        current_filter = e.control.text
        # Visual update for buttons
        for btn in filter_row.controls:
            btn.style = ft.ButtonStyle(
                bgcolor=ft.Colors.BLUE_700 if btn.text == current_filter else ft.Colors.TRANSPARENT,
                color=ft.Colors.WHITE if btn.text == current_filter else (ft.Colors.BLUE_200 if page.theme_mode == ft.ThemeMode.DARK else ft.Colors.BLUE_700),
            )
        render_list()
        page.update()

    filter_options = ["Todos", "Ocupados", "Disponíveis", "Inativos"]
    filter_row = ft.Row(
        [
            ft.TextButton(
                text=opt, 
                on_click=on_filter_change,
                style=ft.ButtonStyle(
                    bgcolor=ft.Colors.BLUE_700 if opt == "Todos" else ft.Colors.TRANSPARENT,
                    color=ft.Colors.WHITE if opt == "Todos" else (ft.Colors.BLUE_200 if page.theme_mode == ft.ThemeMode.DARK else ft.Colors.BLUE_700),
                    padding=15
                )
            ) for opt in filter_options
        ],
        spacing=0
    )

    render_list()

    return ft.Container(
        content=ft.Column([
            ft.Row([
                ft.Text("Apartamentos", size=30, weight=ft.FontWeight.BOLD),
                ft.ElevatedButton(
                    "+ Novo Apartamento", 
                    on_click=lambda _: (
                        setattr(new_apt_dialog, "open", True),
                        setattr(new_apt_dialog.actions[1], "disabled", False),
                        page.update()
                    ),
                    bgcolor=ft.Colors.BLUE_700,
                    color=ft.Colors.WHITE
                ),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            filter_row,
            ft.Divider(),
            ft.Row([search_field]),
            ft.Column([grid_container], scroll=ft.ScrollMode.ALWAYS, expand=True)
        ], expand=True),
        padding=20,
        expand=True
    )
