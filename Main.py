import random as rnd
import os
import math


class Mazo:
    def __init__(self):
        self.Mazo = self.crear_mazo()

    def crear_mazo(self):
        valores = ["A", 2, 3, 4, 5, 6, 7, 8, 9, 10, "J", "Q", "K"]
        palos = ["♥", "♦", "♣", "♠"]
        mazo = []
        for valor in valores:
            for palo in palos:
                carta = str(valor) + palo
                mazo.append(carta)
        rnd.shuffle(mazo)
        return mazo

    def obtener_numero(self, cadena):
        numero = ""
        for caracter in cadena:
            if caracter.isdigit():
                numero += caracter
        return int(numero)

    def contar_valor(self, carta, Lista, i):
        if "J" in carta or "Q" in carta or "K" in carta:
            return 10
        if "A" in carta:
            if Lista[i].id == 0:
                print(Lista[i].Mano)
                valor_as = input("Tienes un as, ¿deseas que sea 11? (s/n): ")
                if valor_as.lower() == "s":
                    return 11
                else:
                    return 1
            else:
                if Lista[i].DecidirAs():
                    return 11
                else:
                    return 1
        else:
            return self.obtener_numero(carta)

    def repartir(self, cant, Lista, id):
        for i in range(cant):
            if self.Mazo:
                carta = self.Mazo.pop()
                Lista[id].Mano.append(carta)
                Lista[id].score += self.contar_valor(carta, Lista, id)
            else:
                raise ValueError("No hay suficientes cartas en el mazo para repartir")


class Jugador:
    def __init__(self, id=None):
        self.id = id
        self.score = 0
        self.Saldo = 0
        self.Mano = []

    def EstaVivo(self):
        if self.score > 0:
            return True
        elif self.score == -1:
            return False

    def BorrarMano(self):
        self.score = 0
        self.Mano = []


class Humano(Jugador):
    def __init__(self):
        super().__init__(id=0)
        self.Nombre = input("Cual es tu nombre? ")
        self.Saldo = 300
        self.Apuesta = 0

    def Decidir(self):
        if (
            str(input(f"Tienes {self.score} puntos, deseas pedir otra carta? (s/n)"))
            == "s"
        ):
            return True
        else:
            return False

    def DecidirAs(self):
        if str(input("Tienes un as, quieres que sea un 11? (s/n) ")) == "s":
            return 11
        else:
            return 1

    def Apostar(self):
        self.Apuesta = abs(int(input(f"Tienes {self.Saldo}, Cuanto deseas apostar? ")))
        return self.Apuesta


class Ia(Jugador):
    def __init__(self, id=None):
        super().__init__(id)
        self.Nombre = self.GenerarNombre()
        self.mbti = self.GenerarMbti()
        self.Potenciador = self.MbtiAPotenciador(self.mbti)
        self.Saldo = rnd.randrange(200, 400)
        self.Apuesta = 0

    nombres = [
        "Carlos",
        "María",
        "Pedro",
        "Laura",
        "Javier",
        "Ana",
        "Luis",
        "Elena",
        "Francisco",
        "Carmen",
        "Andrés",
        "Sofía",
        "Diego",
        "Isabel",
        "Manuel",
        "Lucía",
        "Roberto",
        "Marta",
        "Raúl",
        "Paula",
        "José",
        "Silvia",
        "Fernando",
        "Gabriela",
        "Álvaro",
        "Clara",
        "Daniel",
        "Beatriz",
        "Antonio",
        "Alicia",
        "Miguel",
        "Patricia",
        "Ricardo",
        "Sara",
        "David",
        "Lorena",
        "Juan",
        "Verónica",
        "Sergio",
        "Rosa",
    ]
    apellidos = [
        "García",
        "Rodríguez",
        "Martínez",
        "Hernández",
        "López",
        "González",
        "Pérez",
        "Sánchez",
        "Ramírez",
        "Torres",
        "Fernández",
        "Álvarez",
        "Morales",
        "Romero",
        "Vargas",
        "Ortiz",
        "Castro",
        "Núñez",
        "Mendoza",
        "Jiménez",
        "Ramos",
        "Flores",
        "Gutiérrez",
        "Vega",
        "Reyes",
        "Rivas",
        "Díaz",
        "Campos",
        "Molina",
        "Ruiz",
        "Cruz",
        "Guzmán",
        "Suárez",
        "Blanco",
        "Méndez",
        "Roldán",
        "Escobar",
        "Vargas",
        "Navarro",
        "Paredes",
    ]

    def GenerarNombre(self):
        nombre = rnd.choice(self.nombres)
        apellido = rnd.choice(self.apellidos)
        return f"{nombre} {apellido}"

    def GenerarMbti(self):
        Letras = [
            rnd.choice(["E", "I"]),
            rnd.choice(["S", "N"]),
            rnd.choice(["T", "F"]),
            rnd.choice(["J", "P"]),
        ]
        Mbti = "".join(Letras)
        return Mbti

    def MbtiAPotenciador(self, Mbti):
        Potenciadores = {
            "E": {"Pot": rnd.uniform(6.0, 8.0)},
            "I": {"Pot": rnd.uniform(-9.0, -7.0)},
            "S": {"Pot": rnd.uniform(-6.0, -2.0)},
            "N": {"Pot": rnd.uniform(7.0, 9.0)},
            "T": {"Pot": rnd.uniform(-4.0, -1.0)},
            "F": {"Pot": rnd.uniform(4.0, 6.0)},
            "J": {"Pot": rnd.uniform(-8.0, -6.0)},
            "P": {"Pot": rnd.uniform(3.0, 4.0)},
        }
        Potenciador = 0
        for Letra in Mbti:
            Potenciador += Potenciadores[Letra]["Pot"]
        return Potenciador

    def DecidirAs(self):
        if self.score <= 10:
            return True
        else:
            return False

    def Decidir(self):
        random = rnd.uniform(0, 100)
        Req = self.f(self.score)
        if random < Req:
            return True
        else:
            return False

    def f(self, x):
        threshold = rnd.uniform(0.3, 0.4) + (self.Potenciador / 75)
        Nodo = rnd.uniform(12, 13) + (self.Potenciador / 10)
        return 100 * ((1) / (1 + math.e ** (threshold * (x - Nodo))))

    def Apostar(self, Recomendado):
        self.Apuesta = abs(
            int(
                self.Saldo
                / (1 + math.e ** (-0.1) * self.Potenciador)
                * math.tanh(Recomendado / self.Saldo)
            )
        )
        return self.Apuesta


class Crupier(Ia):
    def __init__(self):
        super().__init__(id=10)
        self.Nombre = "Crupier"
        self.id = id
        self.Saldo = 1000

    def DecidirAs(self):
        if self.score <= 17:
            if self.score <= 10:
                return True
            else:
                return False
        else:
            return False

    def Decidir(self):
        if self.score < 17:
            return True
        else:
            random = rnd.uniform(0, 100)
            Req = self.f(self.score)
            if random < Req:
                return True
            else:
                return False


class Casa:
    def __init__(self, SaldoInicial):
        self.Saldo = SaldoInicial
        self.SaldoMesa = 0
        self.Recomendado = 30
        pass

    def Pagar(self, Lista, id, cantidad):
        self.Saldo -= cantidad
        Lista[id].Saldo += cantidad

    def Cobrar(self, Lista, id, cantidad):
        self.Saldo += cantidad
        Lista[id].Saldo -= cantidad

    def PagarGanador(self, Lista, id, cantidad):
        self.SaldoMesa -= cantidad
        Lista[id].Saldo += cantidad

    def CobrarJugador(self, Lista, id, cantidad):
        self.SaldoMesa += cantidad
        Lista[id].Saldo -= cantidad

    def CobrarRonda(self, Lista):
        for i in range(len(Lista)):
            if Lista[i].id == 0:
                CantidadJugador = Lista[i].Apostar()
                self.CobrarJugador(Lista, i, CantidadJugador)
            else:
                CantidadAi = Lista[i].Apostar(self.Recomendado)
                self.CobrarJugador(Lista, i, CantidadAi)

    def EstadoCasa(self):
        print(f"La casa tiene ${self.Saldo}")

    def EstadoMesa(self):
        print(f"La mesa tiene ${self.SaldoMesa}")

    def ApuestaRecomendada(self):
        print(f"La apuesta recomendada está fijada en: {self.Recomendado}")


class Juego:
    def __init__(self, Banca, Jugadores):
        self.Casa = Banca
        self.Jugadores = Jugadores
        pass

    def MejorScore(self):
        MejorIndice = -1
        MejorDif = 22

        for i, jugador in enumerate(self.Jugadores):
            if 0 <= jugador.score <= 21:
                dif_actual = 21 - jugador.score
                if dif_actual < MejorDif or (
                    dif_actual == MejorDif and i != MejorIndice
                ):
                    MejorDif = dif_actual
                    MejorIndice = i

        return MejorIndice

    def DetectarGanador(self, Ronda, Banca):
        n = len(self.Jugadores)
        MejorIndice = self.MejorScore()

        for i in range(n):
            if self.Jugadores[i].score == 21:
                cls()
                print(f"Ganador: {self.Jugadores[i].Nombre} --> Blackjack")
                print(f"{self.Jugadores[i].Mano}")
                print(f"{self.Jugadores[i].Nombre} se lleva: ${Banca.SaldoMesa}")
                pause()

                return False

        if all(self.Jugadores[j].score == -1 for j in range(n)):
            cls()
            print("No hay ganador, todos los Jugadores fueron eliminados")
            pause()
            return False

        if Ronda >= 4:
            cls()
            print(
                f"Ganador: {self.Jugadores[MejorIndice].Nombre}, con {self.Jugadores[MejorIndice].score} puntos"
            )
            print(f"{self.Jugadores[MejorIndice].Mano}")
            print(f"{self.Jugadores[MejorIndice].Nombre} se lleva: ${Banca.SaldoMesa}")
            pause()
            return False
        else:
            return True

    def ImprimirDatos(self):
        n = len(self.Jugadores)
        print("-----------------------------------------")
        for i in range(n):
            print(
                f"{f'{self.Jugadores[i].Nombre} -> Jugador eliminado' if self.Jugadores[i].score == -1 else f'{self.Jugadores[i].Mano} >> {self.Jugadores[i].Nombre} (${self.Jugadores[i].Saldo}) >> ({self.Jugadores[i].Apuesta}) >> {f" Mbti: {self.Jugadores[i].mbti}" if self.Jugadores[i].id != 0 or self.Jugadores[i].id == len(self.Jugadores) - 1 else ""} \nSuma: {self.Jugadores[i].score} '}"
            )
            print("*******************")
        print("-----------------------------------------")
        self.Casa.EstadoMesa()
        pause()

    def Partida(self, Mazo, Banca):
        Cartas = Mazo
        n = len(self.Jugadores)
        NumRonda = 0
        Banca.CobrarRonda(self.Jugadores)
        for i in range(n):
            self.Jugadores[i].BorrarMano()
            Cartas.repartir(2, self.Jugadores, i)
        while self.DetectarGanador(NumRonda, Banca):
            print(f"\n\t\tRonda {NumRonda + 1}")
            self.ImprimirDatos()
            self.Ronda(Cartas)
            NumRonda += 1
        Banca.Recomendado += 30 * 0.7
        Banca.PagarGanador(self.Jugadores, self.MejorScore(), Banca.SaldoMesa)

    def Ronda(self, Cartas):
        n = len(self.Jugadores)
        for i in range(n):
            if self.Jugadores[i].score > 21:
                self.Jugadores[i].score = -1
            if self.Jugadores[i].EstaVivo() and self.Jugadores[i].Decidir():
                Cartas.repartir(1, self.Jugadores, i)


def GenerarIa(n):
    Lista = []
    for i in range(n):
        jugador = Ia(i + 1)
        Lista.append(jugador)
    return Lista


def Sesion(n):
    cls()
    Banca = Casa(5000)
    P1 = Humano()
    Crup = Crupier()
    BotCant = 3
    Jugadores = GenerarIa(BotCant + 1)
    Jugadores[0] = P1
    Jugadores.append(Crup)
    JuegoActual = Juego(Banca, Jugadores)
    cls()
    print("\t\tLista de jugadores:\n")
    for i in range(BotCant + 2):
        print(f"\t{Jugadores[i].Nombre}")
    print("\t")
    pause()

    for i in range(n):
        Cartas = Mazo()
        print(f"---------------Partida {i + 1}---------------")
        Banca.ApuestaRecomendada()

        JuegoActual.Partida(Cartas, Banca)


def cls():
    os.system("clear")


def pause():
    input("Presiona Enter para continuar...")


num = int(input("\nCuantas rondas? "))
Sesion(num)
