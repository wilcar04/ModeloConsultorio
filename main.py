import datetime
from abc import ABC, abstractmethod
from typing import Optional, Type


class Historial(ABC):

    def __init__(self, fecha: datetime.date, informacion: str):
        self.fecha: datetime.date = fecha
        self.informacion: str = informacion

    @abstractmethod
    def __str__(self):
        pass


class HistoriaClinica(Historial):

    def __init__(self, fecha: datetime.date, informacion: str):
        super().__init__(fecha, informacion)

    def __str__(self):
        return f"Fecha: {self.fecha}\n" \
               f"Resultado: {self.informacion}"


class ResultadoEcografia(Historial):

    def __init__(self, fecha: datetime.date, informacion: str, tipo_ecografia: str):
        super().__init__(fecha, informacion)
        self.tipo_ecografia: str = tipo_ecografia

    def __str__(self):
        return f"Fecha: {self.fecha}\n" \
               f"Tipo de Ecografía: {self.tipo_ecografia}\n" \
               f"Resultado: {self.informacion}"


class Cita(ABC):

    def __init__(self, fecha: datetime.date, hora: datetime.time, cedula_paciente: str):
        self.fecha: datetime.date = fecha
        self.hora: datetime.time = hora
        self.cedula_paciente: str = cedula_paciente
        self.confirmada: bool = False
        self.atendida: bool = False

    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def convertir_archivo(self, ruta_archivo: str) -> Historial:
        pass

    def cita_confirmada(self):
        self.confirmada = True

    def cita_atendida(self):
        self.atendida = True

    def obtener_fecha_hora(self) -> tuple[datetime.date, datetime.time]:
        return self.fecha, self.hora


class CitaMedica(Cita):

    def __init__(self, fecha: datetime.date, hora: datetime.time, cedula_paciente: str):
        super().__init__(fecha, hora, cedula_paciente)

    def __str__(self):
        return f"Fecha: {self.fecha}, Hora: {self.hora}"

    def convertir_archivo(self, ruta_archivo: str) -> Historial:
        pass


class CitaEcografia(Cita):

    def __init__(self, fecha: datetime.date, hora: datetime.time, cedula_paciente: str, tipo_ecografia: str):
        super().__init__(fecha, hora, cedula_paciente)
        self.tipo_ecografia: str = tipo_ecografia

    def __str__(self):
        return f"Fecha: {self.fecha}, Hora: {self.hora}, Tipo de Ecografía: {self.tipo_ecografia}"

    def convertir_archivo(self, ruta_archivo: str) -> Historial:
        pass


class Paciente:

    def __init__(self, cedula: str, nombre: str, sexo: str, fecha_nacimiento: datetime.date, celular: str):
        self.cedula: str = cedula
        self.nombre: str = nombre
        self.sexo: str = sexo
        self.fecha_nacimiento: datetime.date = fecha_nacimiento
        self.edad: int = self.calcular_edad(fecha_nacimiento)
        self.celular: str = celular
        self.cita: Optional[Cita] = None
        self.historial: list[Historial] = []

    def __str__(self):
        return f"Nombre: {self.nombre} Cedula: {self.cedula} Celular: {self.celular}"

    @staticmethod
    def calcular_edad(fecha_nacimiento: datetime.date) -> int:
        fecha_actual = datetime.date.today()
        return int(fecha_actual.strftime("%Y")) - int(fecha_nacimiento.strftime("%Y"))

    def paciente_tiene_cita(self) -> bool:
        return self.cita is not None

    def cita_confirmada(self):
        self.cita.cita_confirmada()

    def obtener_fecha_hora_de_cita(self) -> tuple[datetime.date, datetime.time]:
        return self.cita.obtener_fecha_hora()

    def eliminar_cita(self):
        self.cita = None

    def convertir_archivo(self, ruta_archivo: str) -> Historial:
        return self.cita.convertir_archivo(ruta_archivo)

    def agregar_historial(self, historial: Historial):
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

    def __init__(self, fecha: datetime.date):
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
        return hora not in self.citas

    def agregar_cita(self, fecha: datetime.date, hora: datetime.time,
                     cedula_paciente: str, tipo_ecografia: Optional[str]):
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


class Agenda:

    def __init__(self):
        self.agendas_diarias: dict[datetime.date, AgendaDiaria] = {}

    def hora_disponible(self, dia: datetime.date, hora: datetime.time) -> bool:
        if dia in self.agendas_diarias:
            return self.agendas_diarias[dia].hora_disponible(hora)
        else:
            return True

    def agregar_cita(self, fecha: datetime.date, hora: datetime.time, cedula_paciente: str, tipo_ecografia: str):
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


class Consultorio:
    HORA_INICIAL: int = 9
    HORA_FINAL: int = 16
    ECOGRAFIAS: tuple[str] = ("fetal", "abdominal", "vias urinarias", "mamaria", "muscular",
                              "cervical", "renal")

    def __init__(self):
        self.pacientes: dict[str, Paciente] = {}
        self.agenda: Agenda = Agenda()

    @staticmethod
    def obtener_numero_mes(mes: str) -> Optional[int]:
        meses = ("enero", "febrero", "marzo", "arbil", "mayo", "junio", "julio",
                 "agosto", "septiembre", "octubre", "noviembre", "diciembre")
        if mes.lower() in meses:
            return meses.index(mes.lower()) + 1
        else:
            return None

    @staticmethod
    def obtener_formato_fecha(numero_mes: int, dia: int) -> datetime.date:
        date = datetime.date.today()
        year = int(date.strftime("%Y"))
        return datetime.date(year, numero_mes, dia)

    @staticmethod
    def obtener_formato_hora(hora: int) -> datetime.time:
        return datetime.time(hora, 0)

    @staticmethod
    def dia_valido(dia: int, numero_mes: int) -> bool:
        if numero_mes in [1, 3, 5, 7, 8, 10, 12]:
            dias_del_mes = 31
        elif numero_mes in [4, 6, 9, 11]:
            dias_del_mes = 30
        else:
            dias_del_mes = 28
        return 0 < dia <= dias_del_mes

    def hora_valida(self, hora: int) -> bool:
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

    def organizar_agenda(self, lista_horas: list[datetime.time],
                         lista_informacion: list[Type[tuple]]) -> tuple[Optional[Type[tuple]]]:
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

    # Requisitos de programa:

    def registrar_ususario(self, cedula: str, nombre: str,  sexo: str, fecha_nacimiento: str, celular: str):
        if not self.usuario_existe(cedula):
            formato_fecha = None
            try:
                lista_fecha = fecha_nacimiento.split("/")
                formato_fecha = datetime.date(int(lista_fecha[2]), int(lista_fecha[1]), int(lista_fecha[0]))
            except ValueError:
                pass
                # Error: La fecha de nacimiento ingresada no es válida
            paciente = Paciente(cedula, nombre, sexo, formato_fecha, celular)
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

    def confimar_cita(self, cedula: str):
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
                self.agenda.eliminar_cita(fecha, hora)
                paciente.eliminar_cita()
            else:
                # Error: El paciente no tiene cita
                pass
        else:
            # Error: Usuario no ha sido registrado
            pass

    def atender_cita(self, cedula: str, ruta_archivo: str):
        if self.usuario_existe(cedula):
            paciente = self.pacientes[cedula]
            if paciente.paciente_tiene_cita():
                historial = paciente.convertir_archivo(ruta_archivo)
                paciente.agregar_historial(historial)
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
        fecha = self.obtener_formato_fecha(numero_mes, dia)
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
