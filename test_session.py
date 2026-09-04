import json
import os
import time
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://agendamiento.dian.gov.co/"
VALIDATOR_URL = BASE_URL + "Player.aspx/ValidadorValidar"

NO_AVAILABLE = "NO_AVAILABLE"
AVAILABLE = "AVAILABLE"
UNKNOWN = "UNKNOWN"
CHECK_INTERVAL_SECONDS = 30 * 60


def create_session():
    """Crea una sesión DIAN nueva y obtiene su token inicial."""
    session = requests.Session()
    response = session.get(
        BASE_URL,
        params={"recurso": "CitasDIAN"},
        timeout=60,
    )
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    token_input = soup.find("input", {"name": "anticsrf"})
    if token_input is None:
        raise RuntimeError("No se encontró el campo anticsrf en el HTML.")

    token = token_input.get("value")
    if not token:
        raise RuntimeError("Se encontró anticsrf, pero no contiene un token.")

    return session, token


def post_validator(session, token, body):
    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Content-Type": "application/json; charset=UTF-8",
        "Origin": "https://agendamiento.dian.gov.co",
        "X-Requested-With": "XMLHttpRequest",
        "RequestVerificationToken": token,
        "g-recaptcha-response": "",
    }

    response = session.post(
        VALIDATOR_URL,
        headers=headers,
        data=body,
        timeout=60,
    )

    response.raise_for_status()

    new_token = response.headers.get("X-token")

    if new_token:
        token = new_token

    return response, token


def parse_validator_response(response):
    outer = response.json()

    if "d" not in outer:
        raise RuntimeError("La respuesta de DIAN no contiene la propiedad 'd'.")

    data = json.loads(outer["d"])

    return data


body = """{nombre:'ValidadorDatos.CitasWeb',
configuracion:{
"ControlesGeolocalizacion":[],
"FormatoCitas":"{cita.codigo}    {cita.fecha}    {cita.Oficina.Nombre}    img/icono1.png    img/icono2.png    img/icono3.png",
"IdPais":1,
"DistanciaMinima":0,
"TopOficinasCercanas":0,
"FormatoEncabezadoOficina":"",
"FormatoOficina":"{0}",
"ModoWebPlayer":true,
"Archivo":{
"Ruta":"Recursos/CitasDIAN/",
"FechaActualizacion":"2026-05-19T09:54:52.4205344-05:00"
},
"TipoPolitica":0,
"ObtenerEspecialidadesVirtuales":false,
"ObtenerEspecialidadesPresenciales":false,
"GenerarTurno":false,
"ConfiguracionServicioRestEncriptado": "n6ch/SV/k+dI4u2UFdFZt/brXMA9zVn5kM201dC5IYv7J3PpQUXUWqySuM59vvO2Emx2PVFvYTtaJ7Rd6sSsRSlPtbn2zrNctjIsohWmnJHvHUPuBieiBA0jm0eX62xUQ+6BFWhtYjg1ePMyZSQYL79D2dZBRPWvmBFKvDrg50aJU/0Tsgpc2oALqH1hAXFJfBsx+jJJ6QvEZWmJH+3a/g=="
},
respuestaBase:{
"Fuente":"Validador",
"Encontrado":false,
"DetalleAdicional":"manejadorEncontroTiposCliente",
"ObjetosEncontrados":[],
"Recurso":"CitasDIAN"
}}"""

persona_natural_body = """{nombre:'ValidadorDatos.CitasWeb',
configuracion:{
"ControlesGeolocalizacion":[],
"FormatoCitas":"{cita.codigo}    {cita.fecha}    {cita.Oficina.Nombre}    img/icono1.png    img/icono2.png    img/icono3.png",
"IdPais":1,
"DistanciaMinima":0,
"TopOficinasCercanas":0,
"FormatoEncabezadoOficina":"",
"FormatoOficina":"{0}",
"ModoWebPlayer":true,
"Archivo":{
"Ruta":"Recursos/CitasDIAN/",
"FechaActualizacion":"2026-05-19T09:54:52.4205344-05:00"
},
"TipoPolitica":0,
"ObtenerEspecialidadesVirtuales":false,
"ObtenerEspecialidadesPresenciales":false,
"GenerarTurno":false,
"ConfiguracionServicioRestEncriptado": "n6ch/SV/k+dI4u2UFdFZt/brXMA9zVn5kM201dC5IYv7J3PpQUXUWqySuM59vvO2Emx2PVFvYTtaJ7Rd6sSsRSlPtbn2zrNctjIsohWmnJHvHUPuBieiBA0jm0eX62xUQ+6BFWhtYjg1ePMyZSQYL79D2dZBRPWvmBFKvDrg50aJU/0Tsgpc2oALqH1hAXFJfBsx+jJJ6QvEZWmJH+3a/g=="
},
respuestaBase:{
"Fuente":"Validador",
"Encontrado":false,
"DetalleAdicional":"manejadorEncontroTiposEspecialidad",
"ObjetosEncontrados":[
"{\\"CodigoCita\\":null,\\"CodigoCitaModificada\\":null,\\"Cola\\":{\\"IdEspecialidad\\":\\"0\\",\\"Nombre\\":null},\\"TipoEspecialidad\\":{\\"IdTipoEspecialidad\\":0,\\"Nombre\\":null},\\"Oficina\\":{\\"IdOficina\\":0,\\"Nombre\\":null,\\"Latitud\\":0,\\"Longitud\\":0},\\"UsuarioCliente\\":{\\"IdTipoCliente\\":\\"1\\",\\"IdTipoDocumento\\":0,\\"Nombre\\":null,\\"Apellido\\":null,\\"NumeroDocumento\\":null,\\"CorreoElectronico\\":null,\\"Celular\\":null,\\"Telefono\\":null,\\"Direccion\\":null,\\"IdCiudad\\":0,\\"IdEstado\\":0,\\"AceptaPoliticaDatos\\":false},\\"Fecha\\":\\"2001-01-01T17:00:00.000Z\\",\\"Hora\\":\\"2001-01-01T17:00:00.000Z\\",\\"IdAgenda\\":0,\\"Estado\\":{\\"IdEstado\\":0,\\"Nombre\\":null},\\"Funcionario\\":{\\"NombreAMostrar\\":null,\\"Id\\":null},\\"Archivo\\":null,\\"CamposAdicionales\\":null,\\"EsFlujoCitaCreacion\\":\\"true\\"}"
],
"Recurso":"CitasDIAN"
}}"""

virtual_body = """{nombre:'ValidadorDatos.CitasWeb',
configuracion:{
"ControlesGeolocalizacion":[],
"FormatoCitas":"{cita.codigo}    {cita.fecha}    {cita.Oficina.Nombre}    img/icono1.png    img/icono2.png    img/icono3.png",
"IdPais":1,
"DistanciaMinima":0,
"TopOficinasCercanas":0,
"FormatoEncabezadoOficina":"",
"FormatoOficina":"{0}",
"ModoWebPlayer":true,
"Archivo":{
"Ruta":"Recursos/CitasDIAN/",
"FechaActualizacion":"2026-05-19T09:54:52.4205344-05:00"
},
"TipoPolitica":0,
"ObtenerEspecialidadesVirtuales":false,
"ObtenerEspecialidadesPresenciales":false,
"GenerarTurno":false,
"ConfiguracionServicioRestEncriptado": "n6ch/SV/k+dI4u2UFdFZt/brXMA9zVn5kM201dC5IYv7J3PpQUXUWqySuM59vvO2Emx2PVFvYTtaJ7Rd6sSsRSlPtbn2zrNctjIsohWmnJHvHUPuBieiBA0jm0eX62xUQ+6BFWhtYjg1ePMyZSQYL79D2dZBRPWvmBFKvDrg50aJU/0Tsgpc2oALqH1hAXFJfBsx+jJJ6QvEZWmJH+3a/g=="
},
respuestaBase:{
"Fuente":"Validador",
"Encontrado":false,
"DetalleAdicional":"manejadorEncontroCategoria",
"ObjetosEncontrados":["2"],
"Recurso":"CitasDIAN"
}}"""

devoluciones_body = """{nombre:'ValidadorDatos.CitasWeb',
configuracion:{
"ControlesGeolocalizacion":[],
"FormatoCitas":"{cita.codigo}    {cita.fecha}    {cita.Oficina.Nombre}    img/icono1.png    img/icono2.png    img/icono3.png",
"IdPais":1,
"DistanciaMinima":0,
"TopOficinasCercanas":0,
"FormatoEncabezadoOficina":"",
"FormatoOficina":"{0}",
"ModoWebPlayer":true,
"Archivo":{
"Ruta":"Recursos/CitasDIAN/",
"FechaActualizacion":"2026-05-19T09:54:52.4205344-05:00"
},
"TipoPolitica":0,
"ObtenerEspecialidadesVirtuales":false,
"ObtenerEspecialidadesPresenciales":false,
"GenerarTurno":false,
"ConfiguracionServicioRestEncriptado": "n6ch/SV/k+dI4u2UFdFZt/brXMA9zVn5kM201dC5IYv7J3PpQUXUWqySuM59vvO2Emx2PVFvYTtaJ7Rd6sSsRSlPtbn2zrNctjIsohWmnJHvHUPuBieiBA0jm0eX62xUQ+6BFWhtYjg1ePMyZSQYL79D2dZBRPWvmBFKvDrg50aJU/0Tsgpc2oALqH1hAXFJfBsx+jJJ6QvEZWmJH+3a/g=="
},
respuestaBase:{
"Fuente":"Validador",
"Encontrado":false,
"DetalleAdicional":"manejadorEncontroColas",
"ObjetosEncontrados":[
"{\\"CodigoCita\\":null,\\"CodigoCitaModificada\\":null,\\"Cola\\":{\\"IdEspecialidad\\":\\"0\\",\\"Nombre\\":null},\\"TipoEspecialidad\\":{\\"IdTipoEspecialidad\\":2,\\"Nombre\\":\\"Virtual\\"},\\"Oficina\\":{\\"IdOficina\\":\\"001\\",\\"Nombre\\":null,\\"Latitud\\":0,\\"Longitud\\":0},\\"UsuarioCliente\\":{\\"IdTipoCliente\\":\\"1\\",\\"IdTipoDocumento\\":0,\\"Nombre\\":null,\\"Apellido\\":null,\\"NumeroDocumento\\":null,\\"CorreoElectronico\\":null,\\"Celular\\":null,\\"Telefono\\":null,\\"Direccion\\":null,\\"IdCiudad\\":0,\\"IdEstado\\":0,\\"AceptaPoliticaDatos\\":false},\\"Fecha\\":\\"2001-01-01T17:00:00.000Z\\",\\"Hora\\":\\"2001-01-01T17:00:00.000Z\\",\\"IdAgenda\\":0,\\"Estado\\":{\\"IdEstado\\":0,\\"Nombre\\":null},\\"Funcionario\\":{\\"NombreAMostrar\\":null,\\"Id\\":null},\\"Archivo\\":null,\\"CamposAdicionales\\":null,\\"EsFlujoCitaCreacion\\":\\"true\\"}",
"Nombre",
"1",
"13",
"2"
],
"Recurso":"CitasDIAN"
}}"""



def check_dian():
    """Ejecuta una consulta completa con una sesión nueva."""
    print("Conectando con DIAN...")
    session = None
    try:
        session, token = create_session()

        for step_name, request_body in (
            ("Inicialización", body),
            ("Persona Natural", persona_natural_body),
            ("Atención Virtual", virtual_body),
            ("Devoluciones", devoluciones_body),
        ):
            response, token = post_validator(session, token, request_body)
            print(f"{step_name}: HTTP {response.status_code}")

        data = parse_validator_response(response)
    except requests.exceptions.ReadTimeout:
        print("⚠️ DIAN tardó demasiado en responder.")
        return UNKNOWN, []
    except (
        requests.exceptions.RequestException,
        TypeError,
        ValueError,
        RuntimeError,
    ) as error:
        print(f"⚠️ No fue posible completar la consulta: {error}")
        return UNKNOWN, []
    finally:
        if session is not None:
            session.close()

    handler = data.get("DetalleAdicional")
    total = data.get("TotalObjetosEncontrados", 0)
    objetos = data.get("ObjetosEncontrados") or []

    if handler == "manejadorNoEncontroColas" or total == 0:
        return NO_AVAILABLE, []
    if handler == "manejadorEncontroColas":
        return AVAILABLE, objetos

    print("⚠️ Respuesta desconocida de DIAN:")
    print(json.dumps(data, indent=2, ensure_ascii=False))
    return UNKNOWN, []


def options_signature(options):
    """Genera una firma estable sin asumir todavía la estructura de cada opción."""
    return frozenset(
        json.dumps(option, sort_keys=True, ensure_ascii=False)
        for option in options
    )


def build_telegram_message(options):
    options_text = json.dumps(options, indent=2, ensure_ascii=False)
    max_options_length = 3000
    if len(options_text) > max_options_length:
        options_text = options_text[:max_options_length] + "\n..."

    return (
        "🚨 Citas DIAN disponibles\n\n"
        "Trámite: Devoluciones\n"
        "Modalidad: Atención Virtual\n\n"
        "Opciones encontradas:\n"
        f"{options_text}\n\n"
        "Portal oficial:\n"
        "https://agendamiento.dian.gov.co/?recurso=CitasDIAN"
    )


def send_telegram_alert(options):
    """Publica la alerta sin mostrar el token en logs."""
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    if not token or not chat_id:
        print("⚠️ Telegram no está configurado en las variables de entorno.")
        return False

    try:
        response = requests.post(
            f"https://api.telegram.org/bot{token}/sendMessage",
            json={
                "chat_id": chat_id,
                "text": build_telegram_message(options),
                "disable_web_page_preview": True,
            },
            timeout=20,
        )
    except requests.exceptions.RequestException:
        print("⚠️ No fue posible conectar con Telegram.")
        return False

    if not response.ok:
        try:
            description = response.json().get("description", "Error desconocido")
        except ValueError:
            description = "Respuesta no válida de Telegram"
        print(f"⚠️ Telegram rechazó el mensaje: {description}")
        return False

    print("✅ Alerta publicada en Telegram.")
    return True


def run_monitor(interval_seconds=CHECK_INTERVAL_SECONDS):
    previous_status = None
    previous_options = frozenset()

    while True:
        status, options = check_dian()
        current_options = options_signature(options)

        if status == NO_AVAILABLE:
            print("No hay citas disponibles para Devoluciones.")
        elif status == AVAILABLE:
            changed = current_options != previous_options
            became_available = previous_status != AVAILABLE
            if became_available or changed:
                print("🚨 NUEVA DISPONIBILIDAD PARA DEVOLUCIONES")
                print("ObjetosEncontrados completos:")
                print(json.dumps(options, indent=2, ensure_ascii=False))
                send_telegram_alert(options)
            else:
                print("La disponibilidad continúa sin cambios; no se repite la alerta.")
        else:
            print("Estado desconocido; se conservará el estado anterior.")

        if status != UNKNOWN:
            previous_status = status
            previous_options = current_options

        print(f"Próxima consulta en {interval_seconds // 60} minutos.")
        time.sleep(interval_seconds)


if __name__ == "__main__":
    try:
        run_monitor()
    except KeyboardInterrupt:
        print("\nMonitor detenido.")
