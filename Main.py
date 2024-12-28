import random as rnd
import os

class Mazo:
    def __init__(self):
        self.Mazo = self.crear_mazo()

    def crear_mazo(self):
        valores = ['A', 2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K']
        palos = ['♥', '♦', '♣', '♠']
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
            if 'J' in carta or 'Q' in carta or 'K' in carta:
                return 10
            if 'A' in carta:
                if Lista[i].id == 0:
                    print(Lista[i].Mano)
                    valor_as = input('Tienes un as, ¿deseas que sea 11? (s/n): ')
                    if valor_as.lower() == 's':
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
                Lista[id].score += self.contar_valor(carta,Lista,id)
            else:
                raise ValueError("No hay suficientes cartas en el mazo para repartir")       
class Jugador:
    def __init__(self, id=None):
        self.id = id
        self.score = 0
        self.dinero = 0
        self.Mano=[]

    def EstaVivo(self):
        if self.score > 0:
            return True
        elif self.score == -1:
            return False
class Humano(Jugador):
    def __init__(self):
         super().__init__(id=0)
         self.Nombre=input("Cual es tu nombre? ")  


    def Decidir(self):
        if str(input(f"Tienes {self.score} puntos, deseas pedir otra carta? (s/n)")) == "s":
            return True
        else:
            return False
        
    def DecidirAs(self):
        if str(input("Tienes un as, quieres que sea un 11? (s/n) ")) == "s":
            return 11
        else:
            return 1
class Ia(Jugador):
    def __init__(self, id=None):
        super().__init__(id)
        self.Nombre=self.GenerarNombre()
        self.mbti = self.GenerarMbti()
        self.Potenciador = self.MbtiAPotenciador(self.mbti)

    nombres = [
        "Carlos", "María", "Pedro", "Laura", "Javier", "Ana", "Luis", "Elena", "Francisco", "Carmen",
        "Andrés", "Sofía", "Diego", "Isabel", "Manuel", "Lucía", "Roberto", "Marta", "Raúl", "Paula",
        "José", "Silvia", "Fernando", "Gabriela", "Álvaro", "Clara", "Daniel", "Beatriz", "Antonio", "Alicia",
        "Miguel", "Patricia", "Ricardo", "Sara", "David", "Lorena", "Juan", "Verónica", "Sergio", "Rosa"
    ]
    apellidos = [
        "García", "Rodríguez", "Martínez", "Hernández", "López", "González", "Pérez", "Sánchez", "Ramírez", "Torres",
        "Fernández", "Álvarez", "Morales", "Romero", "Vargas", "Ortiz", "Castro", "Núñez", "Mendoza", "Jiménez",
        "Ramos", "Flores", "Gutiérrez", "Vega", "Reyes", "Rivas", "Díaz", "Campos", "Molina", "Ruiz",
        "Cruz", "Guzmán", "Suárez", "Blanco", "Méndez", "Roldán", "Escobar", "Vargas", "Navarro", "Paredes"
    ]

    def GenerarNombre(self):
        nombre = rnd.choice(self.nombres)
        apellido = rnd.choice(self.apellidos)
        return f"{nombre} {apellido}"
    
    def GenerarMbti(self):
        Letras = [
            rnd.choice(['E', 'I']),
            rnd.choice(['S', 'N']),
            rnd.choice(['T', 'F']),
            rnd.choice(['J', 'P'])
            ]
        Mbti = ''.join(Letras)
        return Mbti
    
    def MbtiAPotenciador(self,Mbti):
        Potenciadores = {
            "E": {
                "Pot": rnd.uniform(6.0, 8.0)  
            },
            "I": {
                "Pot": rnd.uniform(-9.0, -7.0)  
            },
            "S": {
                "Pot": rnd.uniform(-4.0, -2.0)  
            },
            "N": {
                "Pot": rnd.uniform(7.0, 9.0)   
            },
            "T": {
                "Pot": rnd.uniform(-3.0, -1.0)  
            },
            "F": {
                "Pot": rnd.uniform(4.0, 6.0)   
            },
            "J": {
                "Pot": rnd.uniform(-8.0, -6.0)  
            },
            "P": {
                "Pot": rnd.uniform(3.0, 4.0)  
            }
        }
        Potenciador = 0 
        for Letra in Mbti:
            Potenciador += Potenciadores[Letra]['Pot'] 
        return Potenciador  
    
    def DecidirAs(self):
        if self.score <= 10:
            return True
        else:
            return False
        
    def Decidir(self):
        random = rnd.uniform(0,100) 
        Req = self.f(self.score)
        if random < Req:
            return True
        else:
            return False
        
    def f(self,x):
        e = 2.7182818284
        threshold = rnd.uniform(0.3,0.4)-(self.Potenciador/100)
        Nodo = rnd.uniform(12,13)+(self.Potenciador/10)
        return 100*((1)/(1+e**(threshold*(x-Nodo))))    
class Crupier(Ia):
    def __init__(self):
        super().__init__(id=10)  
        self.Nombre = "Crupier"
        self.id = id   

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
            random = rnd.uniform(0,100) 
            Req = self.f(self.score)
            if random < Req:
                return True
            else:
                return False           
def cls():
    os.system("cls")
def pause():
    os.system("pause")        
def MejorScore(Lista):
    MejorIndice = 0
    Mejor = 21 
    for i, jugador in enumerate(Lista):
        if jugador.score <= 21:
            Dif = 21 - jugador.score 
            if Dif < Mejor:
                Mejor = Dif
                MejorIndice = i
    return MejorIndice
def DetectarGanador(Lista, Ronda):
    n = len(Lista)
    MejorIndice = MejorScore(Lista)
    
    for i in range(n):
        if Lista[i].score == 21:              
            print(f"Ganador: {Lista[i].Nombre} --> Blackjack")
            print(f'{Lista[i].Mano}')
            pause() 
            return False                          
        
    if Ronda >= 4:
        print(f"Ganador: {Lista[MejorIndice].Nombre}, con {Lista[MejorIndice].score} puntos") 
        print(f'{Lista[MejorIndice].Mano}')
        pause()           
        return False
    else: 
        return True
def GenerarIa(n):
    Lista = []
    for i in range(n):
        jugador = Ia(i+1)  
        Lista.append(jugador)
    return Lista 
def ImprimirDatos(Lista):
    n = len(Lista)
    print('-----------------------------------------')
    for i in range(n):
        print(f"{f'{Lista[i].Nombre} -> Jugador eliminado' if Lista[i].score == -1 else f'{Lista[i].Mano} >> {Lista[i].Nombre} {f', Mbti: {Lista[i].mbti}' if Lista[i].id != 0 or Lista[i].id == len(Lista)-1 else ""} \nSuma: {Lista[i].score} '}")
        print('*******************')
    print('-----------------------------------------')
    input("Presiona Enter para continuar...")  # Esto pausará la ejecución esperando la entrada del usuario
def Partida():
    cls()
    P1=Humano()
    Crup=Crupier()
    BotCant = 5
    Lista = GenerarIa(BotCant+1)
    Lista[0]=P1
    Lista.append(Crup)
    cls()
    print("\t\tLista de jugadores:\n")
    for i in range(BotCant+2):
        print(f"\t{Lista[i].Nombre}")
    print("\t")
    pause()

    n = len(Lista)
    Cartas = Mazo()
    NumRonda = 0

    for i in range(n):
        Cartas.repartir(2,Lista,i)

    while DetectarGanador(Lista,NumRonda):   
        print(f"\n\t\tRonda {NumRonda+1}")  
        ImprimirDatos(Lista)     
        Ronda(Lista, Cartas)    
        NumRonda += 1    
def Ronda(Lista, Cartas):    
    n = len(Lista)
    for i in range(n):
        if Lista[i].score > 21:
            Lista[i].score = -1
        if Lista[i].EstaVivo() and Lista[i].Decidir():
            Cartas.repartir(1,Lista,i)       
               
Partida()