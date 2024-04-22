from simbolo import Simbolo

class Analizador:

    '''
    Por ahora obvia los errores. No los loguea en ninguna parte ni los recupera
    '''

    def __init__(self, entrada) -> None:
        self.analisis(entrada=entrada)
        self.dict

    def analisis(self, entrada):
        entrada += "해"
        state = 0
        aux = ""
        lista = []
        for i in range(len(entrada)):
            sym = entrada[i]
            if state == 0:
                if sym == "\n" or sym == "\r\n" or sym == "\r" or sym == "\t" or ord(sym) == 32:
                    if aux != "":
                        lista.append(self.recognize(aux))
                        aux = ""
                elif (ord(sym) >= 65 and ord(sym) <= 90 or sym == "_"):  
                    aux += sym 
                elif (ord(sym) >= 48 and ord(sym) <= 57):
                    if aux == "":
                        aux = sym
                        state = 2
                    else:
                        aux += sym 
                elif sym == ";":
                    if aux != "":
                        lista.append(self.recognize(aux))
                        aux = ""
                    lista.append(Simbolo("PCOMA", sym))
                elif sym == "(":
                    if aux != "":
                        lista.append(self.recognize(aux))
                        aux = ""
                    lista.append(Simbolo("PAR1", sym))
                elif sym == ")":
                    if aux != "":
                        lista.append(self.recognize(aux))
                        aux = ""
                    lista.append(Simbolo("PAR2", sym)) 
                elif sym == ",":
                    if aux != "":
                        lista.append(self.recognize(aux))                        
                        aux = ""
                    lista.append(Simbolo("COMA", sym))
                elif sym == "#":
                    if aux != "":
                        lista.append(self.recognize(aux))
                        aux = ""
                    state = 1
                elif sym == "해":
                    if aux != "":
                        lista.append(self.recognize(aux))
                        break
            elif state == 1:
                if sym == "\n" or sym == "\r\n" or sym == "\r" or sym == "\t":
                    state = 0
                else:
                    pass
            elif state == 2:
                if (ord(sym) >= 48 and ord(sym) <= 57):
                    aux += sym 
                else: 
                    lista.append(Simbolo("Numero", aux))
                    aux = ""
                    i = i - 1
                    state = 0

        self.dict = self.sintactico(lista)

    def recognize(self, string):
        #Siempre debe dar una respuesta
        if string == "SET_PRINT_O":
            return Simbolo("Jugada", "Jugador_O")
        elif string == "SET_PRINT_X":
            return Simbolo("Jugada", "Jugador_X")
        elif string == "SET_PRINT_TRIANGULO":
            return Simbolo("Jugada", "Jugador_Triangulo")
        elif string == "SET_PRINT_ESTRELLA":
            return Simbolo("Jugada", "Jugador_Estrella")
        elif string == "NEW_PRINT":
            return Simbolo("Start", string)
        elif string == "END_PRINT":
            return Simbolo("Final", string)
        elif string == "CYAN":
            return Simbolo("Color", string)
        elif string == "MAGENTA":
            return Simbolo("Color", string)
        elif string == "AMARILLO":
            return Simbolo("Color", string)
        elif string == "NEGRO":
            return Simbolo("Color", string)
        else:
            return Simbolo("ID", string)
    
    def sintactico(self, tabla):
        local_dict = {}
        id_var = ""
        jugador = ""
        x = 0
        y = 0
        c = ""
        state = 0
        # El estado 3 en la gramatica representaria Instruccion Instrucciones
        for i in range(len(tabla)):
            simbolo = tabla[i]
            if state == 0:
                if simbolo.tipo == "Start":
                    state = 1
            elif state == 1:
                if simbolo.tipo == "ID":
                    state = 2
            elif state == 2:
                if simbolo.valor == ";":
                    id_var = tabla[i - 1].valor
                    state = 3
            elif state == 3:
                if simbolo.tipo == "Jugada":
                    # Se guarda que jugador es desde simbolo.valor, de no completarse debería de volver a 
                    # este estado y dar error. No implementado aún. 
                    jugador = simbolo.valor
                    
                    if jugador in local_dict:
                        pass
                    else:
                        local_dict[jugador] = []
                    
                    state = 4
                elif simbolo.tipo == "Final":
                    state = 9
            elif state == 4:
                if simbolo.valor == "(":
                    state = 5
                elif simbolo.valor == ")":
                    state = 8
            elif state == 5:
                if simbolo.tipo == "Numero":
                    x = int(simbolo.valor)
                    state = 6
            elif state == 6:
                if simbolo.tipo == "Numero":
                    y = int(simbolo.valor)
                    state = 7
            elif state == 7:
                if simbolo.tipo == "Color":
                    c = simbolo.valor
                    state = 4
            elif state == 8:
                if simbolo.valor == ";":
                    local_dict[jugador].append({'x': x, 'y': y, 'color': c})
                    state = 3
            elif state == 9:
                if simbolo.valor == ";":
                  print("FINISH :)")
                  return {id_var : local_dict}  
            
            #print("Tipo: ", value.tipo, "Valor: ", value.valor)
        # START ID PCOMA INSTRUCCIONES FINAL PCOMA
        
    def get_dictionary(self):
        return self.dict