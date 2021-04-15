import pickle 

instrucciones={
                'MOV' : (0x0,2),
                'ADD' : (0x1,2),
                'SUB' : (0x2,2),
                'SWAP': (0x3,2),
                'MUL' : (0x4,2),
                'DIV' : (0x5,2),
                'CMP' : (0x6,2),
                'SHL' : (0x7,2),
                'SHR' : (0x8,2),
                'AND' : (0x9,2),
                'OR'  : (0xA,2),
                'XOR' : (0xB,2),
                'SYS' : (0xF0,1),
                'JMP' : (0xF1,1),
                'JZ'  : (0xF2,1),
                'JP'  : (0xF3,1),
                'JN'  : (0xF4,1),
                'JNZ' : (0xF5,1),
                'JNP' : (0xF6,1),
                'JNN' : (0xF7,1),
                'LDL' : (0xF8,1),
                'LDH' : (0xF9,1),
                'RND' : (0xFA,1),
                'NOT' : (0xFB,1),
                'STOP': (0xFF1,0),
            }

ram=[]
posGlobal=-1
posRotulos=[]

class Operando:
    #recibe el operando de la operacion
    global posRotulos
    def __init__(self,dato):
        self.dato = dato
        self.tipo=-1000
        self.valor=''

    def calculoTipo(self):
        if self.dato[0]=='[':
            self.tipo=0x2
            self.dato=self.dato[1:-1]#funciona si viene sin espacios
        else:
            if self.dato.upper().find('X')!=-1:
                self.tipo=0x01
            else:   
                self.tipo=0x00

        
    def caluloValor(self):
        if self.tipo==0x2 or self.tipo==0x0 :
            if self.dato.find('@')!=-1:
                #Octal
                self.valor=hex(int(self.dato[1:],8))#Probar 
            else:               
                if self.dato.find('%')!=-1:
                    #hexadecimal
                    self.valor=hex(int(self.dato[1:],16))                
                else:
                    if self.dato.find("'")!=-1:
                        #codigo ascii
                        aux=self.dato.split("'")
                        aux=''.join(aux)
                        self.valor=hex(ord(aux))
                    else:
                        if self.dato.isalpha():
                            #Rotulo
                            self.dato=self.dato.lstrip()
                            self.valor=0x0
                            for rotulo in posRotulos:                               
                                if rotulo[0] == self.dato:
                                    self.valor=hex(int(rotulo[1]))                  
                            if self.valor== 0x0:
                                print("NO EXISTE ROTULO")
                        else:
                            #Decimal
                            aux=self.dato.split('#')
                            aux=''.join(aux)
                            self.valor=hex(int(aux))
        else:
            self.valor=hex(int(('0x'+self.dato[0]),16))

    def magia(self):
        self.calculoTipo()
        self.caluloValor()


class Linea:
    def __init__(self,reglon):
        global posGlobal
        self.reglon = reglon.strip() 
        self.codigo=-1
        self.hexa=0x0
        self.rotulo=''
        self.comando=''
        self.comentario=''
        self.separaCodigo()

        if self.comando!= '':
            posGlobal=posGlobal+1
            self.codigo=posGlobal
            if self.rotulo!='':
                posRotulos.append((self.rotulo,posGlobal))
            else:
                self.rotulo=posGlobal+1
    

    def muestra(self):
        if self.codigo!=-1:
            print('{0:x}'.format(self.hexa),self.rotulo,":",self.comando,";",self.comentario)
        else:
            if self.comentario!='':
                print(";",self.comentario)
            else: print("")
    
    def sacaEspacios(self):
        self.comando=self.comando.strip()
        self.comentario=self.comentario.strip()

    
    def separaCodigo(self):
        aux=self.reglon.split(';')
        if len(aux)==2:
            self.comentario=aux[1]
           
        self.reglon=aux[0]
        aux=self.reglon.split(':')
        if  len(aux)==2:
             
            self.rotulo=aux[0]
            self.comando=aux[1]
        else:
            self.comando=aux[0]
        self.comando.split()

        self.sacaEspacios()

    def creaHexa(self):

        datosMemo=""
        aux=self.comando.split()
        self.instruccion=aux[0].upper()
        aux=''.join(aux[1:])
        aux.strip()
        try:
            datosMemo=instrucciones.get(self.instruccion)
        except:
            self.comando= 0xFFFFFFFF
            return -1
        
        if datosMemo[1] == 2:
            aux=aux.split(',')
            arg_a=Operando(aux[0])
            arg_a.magia()
            arg_b=Operando(aux[1])
            arg_b.magia()
            self.hexa= (instrucciones.get(self.instruccion)[0] <<28 | ((arg_a.tipo <<26) & 0x0C000000) | ((arg_b.tipo <<24) & 0x03000000) |((int(arg_a.valor,16) <<12) & 0x00FFF000) | (int(arg_b.valor,16) & 0x00000FFF))  
        else:
            if datosMemo[1] == 1:
                arg_a=Operando(aux)
                arg_a.magia()
                self.hexa= (instrucciones.get(self.instruccion)[0] <<24 |((arg_a.tipo <<22) & 0x00C00000) |(int(arg_a.valor,16) & 0x00000FFF))
            else:
                self.hexa=instrucciones.get(self.instruccion)[0] <<20 

    def creoLinea(self):
        if self.comando!='':
            self.sacaEspacios()
            self.creaHexa()





   
with open('arcentrada.txt','r') as archivo:
    reglones=archivo.readlines()

for line in reglones:
    a=Linea(line)
    ram.append(a)
    #a.muestra()
    
for line in ram:
    line.creaHexa()
    line.muestra()




