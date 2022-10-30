import datetime
from abc import ABC, abstractmethod
from typing import Optional, Type


class Historial(ABC):

    def __init__(self, fecha, informacion):
        self.fecha: datetime.date = fecha
        self.informacion: str = informacion

    @abstractmethod
    def __str__(self):
        pass


class ResultadoEcografia(Historial):

    def __init__(self, fecha, informacion, tipo_ecografia):
        super().__init__(fecha, informacion)
        self.tipo_ecografia: str = tipo_ecografia

    def __str__(self):
        return f"Fecha: {self.fecha}\n" \
               f"Tipo de Ecografía: {self.tipo_ecografia}\n" \
               f"Resultado: {self.informacion}"


class HistoriaClinica(Historial):

    def __init__(self, fecha, informacion):
        super().__init__(fecha, informacion)

    def __str__(self):
        return f"Fecha: {self.fecha}\n" \
               f"Resultado: {self.informacion}"


class Cita(ABC):

    def __init__(self, fecha, hora, cedula_paciente):
        self.fecha: datetime.date = fecha
        self.hora: datetime.time = hora
        self.cedula_paciente: str = cedula_paciente
        self.confirmada: bool = False
        self.atendida: bool = False

    def cita_confirmada(self):
        self.confirmada = True

    def obtener_fecha_hora(self) -> tuple[datetime.date, datetime.time]:
        return self.fecha, self.hora

    def cita_atendida(self):
        self.atendida = True

    @abstractmethod
    def convertir_archivo(self, archivo):
        pass

    @abstractmethod
    def __str__(self):
        pass


class CitaEcografia(Cita):

    def __init__(self, fecha, hora, cedula_paciente, tipo_ecografia):
        super().__init__(fecha, hora, cedula_paciente)
        self.tipo_ecografia: str = tipo_ecografia

    def convertir_archivo(self, archivo):
        pass

    def __str__(self):
        return f"Fecha: {self.fecha}, Hora: {self.hora}, Tipo de Ecografía: {self.tipo_ecografia}"


class CitaMedica(Cita):

    def __init__(self, fecha, hora, cedula_paciente):
        super().__init__(fecha, hora, cedula_paciente)

    def convertir_archivo(self, archivo):
        pass

    def __str__(self):
        return f"Fecha: {self.fecha}, Hora: {self.hora}"


class Paciente:

    def __init__(self, nombre, cedula, sexo, fecha_nacimiento, celular):
        self.nombre: str = nombre
        self.cedula: str = cedula
        self.sexo: str = sexo
        self.fecha_nacimiento: datetime.date = fecha_nacimiento
        self.edad: int =
        self.celular: str = celular
        self.cita: Optional[Cita] = None
        self.historial: list[Historial] = []

    def __str__(self):
        return f"Nombre: {self.nombre} Cedula: {self.cedula} Celular: {self.celular}"

    def paciente_tiene_cita(self) -> bool:
        return self.cita is not None

    def cita_confirmada(self):
        self.cita.cita_confirmada()

    def obtener_fecha_hora_de_cita(self) -> tuple[datetime.date, datetime.time]:
        return self.cita.obtener_fecha_hora()

    def eliminar_cita(self):
        self.cita = None

    def convertir_archivo(self, archivo) -> Historial:
        self.cita.convertir_archivo(archivo)

    def agregar_historia(self, historial: Historial):
        self.historial.append(historial)

    def cita_atendida(self):
        self.cita.cita_atendida()

    def tiene_historial(self) -> bool:
        return self.historial != []

    def informacion_historia(self) -> list[str]:
        informacion_historial = []
        for historial in self.historial:
            informacion_historial.append(str(historial))
        return informacion_historial


class AgendaDiaria:

    def __init__(self, fecha):
        self.fecha: datetime.date = fecha
        self.citas: dict[datetime.time, Cita] = {}

    @staticmethod
    def cedula_paciente_por_cita(lista_citas: list[Cita]) -> list[Type[tuple]]:
        lista_cedulas_con_citas = []
        for cita in lista_citas:
            cedula = cita.cedula_paciente
            lista_cedulas_con_citas.append(tuple[cedula, cita])
        return lista_cedulas_con_citas

    def hora_disponible(self, hora: datetime.time) -> bool:
        return not hora in self.citas

    def agregar_cita(self, fecha, hora, cedula_paciente, tipo_ecografia):
        if tipo_ecografia is not None:
            cita = CitaEcografia(fecha, hora, cedula_paciente, tipo_ecografia)
        else:
            cita = CitaMedica(fecha, hora, cedula_paciente)
        self.citas[hora] = cita

    def eliminar_cita(self, hora: datetime.time):
        del self.citas[hora]

    def lista_citas(self) -> list[Cita]:
        return [v for v in self.citas.values()]

    def obtener_horas(self) -> list[datetime.time]:
        horas = []
        for cita in self.citas.values():
            horas.append(cita.hora)
        return horas

    def lista_citas_sin_confirmar(self):
        pass


class Agenda:

    def __init__(self):
        self.agendas_diarias: dict[datetime.date, AgendaDiaria] = {}

    def hora_disponible(self, dia: datetime.date, hora: datetime.time) -> bool:
        if dia in self.agendas_diarias:
            return self.agendas_diarias[dia].hora_disponible(hora)
        else:
            return True

    def agregar_cita(self, fecha, hora, cedula_paciente, tipo_ecografia):
        if fecha not in self.agendas_diarias:
            self.agendas_diarias[fecha] = AgendaDiaria(fecha)
        self.agendas_diarias[fecha].agregar_cita(fecha, hora, cedula_paciente, tipo_ecografia)

    def eliminar_cita(self, fecha: datetime.date, hora: datetime.time):
        self.agendas_diarias[fecha].eliminar_cita(hora)

    def fecha_tiene_citas(self, fecha: datetime.date) -> bool:
        return fecha in self.agendas_diarias

    def lista_citas_en_fecha(self, fecha: datetime.date) -> list[Cita]:
        return self.agendas_diarias[fecha].lista_citas()

    def cedula_paciente_por_cita(self, fecha: datetime.date, lista_citas: list[Cita]) -> list[Type[tuple]]:
        return self.agendas_diarias[fecha].cedula_paciente_por_cita(lista_citas)

    def obtener_horas(self, fecha: datetime.date) -> list[datetime.time]:
        return self.agendas_diarias[fecha].obtener_horas()

    def lista_citas_sin_confirmar(self):
        pass


class Consultorio:
    HORA_INICIAL = 9
    HORA_FINAL = 16
    ECOGRAFIAS = ("fetal", "abdominal", "vias urinarias", "mamaria", "muscular",
                  "cervical", "renal")

    def __init__(self):
        self.pacientes: dict[str, Paciente] = {}
        self.agenda: Agenda = Agenda()

    @staticmethod
    def obtener_numero_mes(mes) -> Optional[int]:
        meses = ("enero", "febrero", "marzo", "arbil", "mayo", "junio", "julio",
                 "agosto", "septiembre", "octubre", "noviembre", "diciembre")
        if mes.lower() in meses:
            return meses.index(mes.lower()) + 1
        else:
            return None

    @staticmethod
    def obtener_formato_fecha(mes, dia) -> datetime.date:
        date = datetime.date.today()
        year = int(date.strftime("%Y"))
        return datetime.date(year, mes, dia)

    @staticmethod
    def obtener_formato_hora(hora) -> datetime.time:
        return datetime.time(hora, 0)

    @staticmethod
    def dia_valido(dia, numero_mes) -> bool:
        if numero_mes in [1, 3, 5, 7, 8, 10, 12]:
            dias_del_mes = 31
        elif numero_mes in [4, 6, 9, 11]:
            dias_del_mes = 30
        else:
            dias_del_mes = 28
        return 0 < dia <= dias_del_mes

    def hora_valida(self, hora) -> bool:
        return self.HORA_INICIAL <= hora <= self.HORA_FINAL

    def usuario_existe(self, cedula: str) -> bool:
        return cedula in self.pacientes

    def buscar_paciente(self, cedula: str) -> Paciente:
        return self.pacientes[cedula]

    def informacion_paciente_por_cita(self, lista_cedulas_con_citas: list[Type[tuple]]) -> list[Type[tuple]]:
        informacion = []
        for cedula, cita in lista_cedulas_con_citas:
            paciente = self.buscar_paciente(cedula)
            informacion.append(tuple[str(paciente), str(cita)])
        return informacion

    def organizar_agenda(self, lista_horas: list[datetime.time], lista_informacion: list[Type[tuple]]) -> tuple[Optional[Type[tuple]]]:
        agenda_organizada = []
        for hora in range(self.HORA_INICIAL, self.HORA_FINAL + 1):
            for hora_cita in lista_horas:
                if hora_cita.hour == hora:
                    index_hora_coincidente = lista_horas.index(hora_cita)
                    agenda_organizada.append(lista_informacion.pop(index_hora_coincidente))
                    lista_horas.pop(index_hora_coincidente)
                    break
            else:
                agenda_organizada.append(None)
        return tuple(agenda_organizada)

    def lista_organizada_disponibilidad(self, lista_horas: list[datetime.time]) -> list[bool]:
        lista_disponibilidad = []
        for hora in range(self.HORA_INICIAL, self.HORA_FINAL + 1):
            for hora_cita in lista_horas:
                if hora_cita.hour == hora:
                    lista_disponibilidad.append(False)
                    lista_horas.remove(hora_cita)
                    break
            else:
                lista_disponibilidad.append(True)
        return lista_disponibilidad

    # Requisitos de programa:

    def registrar_ususario(self, nombre: str, cedula: str, sexo: str, fecha_nacimiento: list[str], celular: str):
        if not self.usuario_existe(cedula):
            paciente = Paciente(nombre, cedula, sexo, fecha_nacimiento, celular)
            self.pacientes[cedula] = paciente
        else:
            # Error: Usuario ya registrado
            pass

    def eliminar_paciente(self, cedula: str):
        if not self.usuario_existe(cedula):
            # Error: El usuario no está registrado
            pass
        paciente = self.buscar_paciente(cedula)
        if paciente.paciente_tiene_cita():
            self.cancelar_cita(cedula)
        del self.pacientes[cedula]

    def asignar_cita(self, cedula: str, mes: str, dia: int, hora: int, tipo_ecografia: str = None):
        if not self.usuario_existe(cedula):
            # Error: Usuario no ha sido registrado
            pass
        paciente = self.buscar_paciente(cedula)
        if paciente.paciente_tiene_cita():
            # Error: El paciente ya tiene una cita agendada
            pass
        numero_mes = self.obtener_numero_mes(mes)
        if numero_mes is None:
            # Error: El mes ingresado no es válido
            pass
        if not self.dia_valido(dia, numero_mes):
            # Error: El día ingresado no es válido
            pass
        formato_fecha = self.obtener_formato_fecha(numero_mes, dia)
        if not self.hora_valida(hora):
            # Error: La hora ingresada no es válida
            pass
        formato_hora = self.obtener_formato_hora(hora)
        if not self.agenda.hora_disponible(formato_fecha, formato_hora):
            # Error: La hora indicada ya está ocupada
            pass
        if tipo_ecografia not in self.ECOGRAFIAS and tipo_ecografia is not None:
            # Error: El tipo de ecografía ingresado no es válido
            pass
        self.agenda.agregar_cita(formato_fecha, formato_hora, cedula, tipo_ecografia)

    def confimar_cita(self, cedula):
        if self.usuario_existe(cedula):
            paciente = self.pacientes[cedula]
            if paciente.paciente_tiene_cita():
                paciente.cita_confirmada()
            else:
                # Error: El paciente no tiene cita
                pass
        else:
            # Error: Usuario no ha sido registrado
            pass

    def cancelar_cita(self, cedula: str):
        if self.usuario_existe(cedula):
            paciente = self.pacientes[cedula]
            if paciente.paciente_tiene_cita():
                (fecha, hora) = paciente.obtener_fecha_hora_de_cita()
                paciente.eliminar_cita()
                self.agenda.eliminar_cita(fecha, hora)
            else:
                # Error: El paciente no tiene cita
                pass
        else:
            # Error: Usuario no ha sido registrado
            pass

    def atender_cita(self, cedula: str, archivo: str):
        if self.usuario_existe(cedula):
            paciente = self.pacientes[cedula]
            if paciente.paciente_tiene_cita():
                historial = paciente.convertir_archivo(archivo)
                paciente.agregar_historia(historial)
                paciente.cita_atendida()
            else:
                # Error: El paciente no tiene cita
                pass
        else:
            # Error: Usuario no ha sido registrado
            pass

    def obtener_agenda_dia(self, mes: str, dia: int) -> tuple[Optional[Type[tuple]]]:
        numero_mes = self.obtener_numero_mes(mes)
        if numero_mes is None:
            # Error: El mes ingresado no es válido
            pass
        if not self.dia_valido(dia, numero_mes):
            # Error: El día ingresado no es válido
            pass
        fecha = self.obtener_formato_fecha(mes, dia)
        if not self.agenda.fecha_tiene_citas(fecha):
            # Error: La fecha ingresada no tiene citas
            pass
        lista_citas = self.agenda.lista_citas_en_fecha(fecha)
        lista_cedulas_con_citas = self.agenda.cedula_paciente_por_cita(fecha, lista_citas)
        lista_informacion = self.informacion_paciente_por_cita(lista_cedulas_con_citas)
        lista_horas = self.agenda.obtener_horas(fecha)
        return self.organizar_agenda(lista_horas, lista_informacion)

    def obtener_historial_paciente(self, cedula: str):
        if not self.usuario_existe(cedula):
            # Error: El usuario no está registrado
            pass
        paciente = self.buscar_paciente(cedula)
        if paciente.tiene_historial():
            return paciente.informacion_historia()
        else:
            # Error: El paciente no tiene historial
            pass

    def recuperar_informacion(self):
        pass
