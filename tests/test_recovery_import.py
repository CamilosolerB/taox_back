from pathlib import Path

from openpyxl import Workbook

from scripts.import_latest_workbook import build_plan


def _add_sheet(workbook: Workbook, name: str, headers: list[str], rows: list[list]):
    sheet = workbook.create_sheet(name)
    sheet.append(headers)
    for row in rows:
        sheet.append(row)
    return sheet


def test_build_plan_preserves_fractional_stock_and_business_relationships(tmp_path: Path):
    workbook = Workbook()
    workbook.remove(workbook.active)
    _add_sheet(
        workbook,
        "TABLA_0_LAB",
        ["CODIGO", "NOMBRE DEL PRODUCTO", "USO DE LA SUSTANCIA", "UNID", "TOTAL INVEN", "FDS"],
        [["LAB-1", "Reactivo", "Laboratorio", "L", 0.5, ""]]
    )
    _add_sheet(
        workbook,
        "TABLA_1_INV",
        [
            "CODIGO", "NOMBRE DEL PRODUCTO", "NOMBRE GENERICO",
            "TOTAL INVENT", "UNIDAD DE MEDIDA", "PROVEEDOR PRINCIPAL",
        ],
        [["ITEM-1", "Producto", "Genérico", 2.25, "KG", "Proveedor Uno"]]
    )
    _add_sheet(workbook, "TABLA_3_ALMACEN", ["CODIGO", "ITEM"], [["ITEM-1", "Nombre abreviado"]])
    _add_sheet(
        workbook,
        "TABLA_4_BODEGA",
        ["UBICACIÓN", "NIVEL", "POSICION", "LOCALIZADOR", "CODIGO", "DESCRIPCION", "CANTIDAD", "UNIDAD"],
        [["Zona A", "1", "P1", "R1", "LOC-1", "Producto ubicado", 0.75, "KG"]]
    )
    _add_sheet(
        workbook,
        "TABLA_2_MASTER",
        [
            "COD PROVEEDOR", "NOMBRE PROVEEDOR", "CONTACTO", "DIRECCION",
            "TELEFONO", "CELULAR", "WEB", "CORREO", "CODIGO MAT",
            "NOMBRE DEL PRODUCTO", "PRECIO",
        ],
        [["P-1", "Proveedor Uno", "Contacto", "Dirección", "6011234567", "3001234567", None, "p@example.com", "ITEM-1", "Producto", 12.5]]
    )
    _add_sheet(
        workbook,
        "TABLA_5_CLIENTES",
        [
            "CODIGO", "CLIENTE", "RAZON SOCIAL", "TELEFONO 1", "TELEFONO 2",
            "CONTACTO", "CORREO", "CIUDAD", "TIPO DE AGUA", "CANTIDAD PROMEDIO KG",
        ],
        [["C-1", "Cliente", "Cliente S.A.", "1234567", None, "Contacto", "c@example.com", "Ciudad", "Tipo", 1.5]]
    )
    _add_sheet(workbook, "TABLA_6_PRODUCTO TERMINADO", ["PRODUCTO"], [["No model"]])

    workbook_path = tmp_path / "source.xlsx"
    workbook.save(workbook_path)

    plan = build_plan(workbook_path)

    assert len(plan["products"]) == 3
    assert plan["products"]["ITEM-1"]["name"] == "Producto"
    assert plan["products"]["LAB-1"]["warehouse_name"] == "Laboratorio"
    assert plan["products"]["ITEM-1"]["warehouse_name"] == "Inventario general"
    assert plan["products"]["LOC-1"]["warehouse_name"] == "Bodega física"
    assert plan["warehouse_quantities"] == {
        "LAB-1": 0.5,
        "ITEM-1": 2.25,
        "LOC-1": 0.75,
    }
    assert list(plan["location_stock"].values()) == [0.75]
    assert len(plan["provider_products"]) == 1
    assert plan["providers_skipped"] == 0
    assert plan["product_name_variants"] == 1
    assert plan["clients"][0]["razon_social"] == "Cliente S.A."
    assert plan["unsupported_sheets"] == ["TABLA_6_PRODUCTO TERMINADO"]
