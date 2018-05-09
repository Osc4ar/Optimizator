import random
import math

def entradaEc():
    numVar = int(input("\tIngresa el numero de variables:\n\t -> "))
    fObjetivo = []
    print("\t\tIngresa los datos de la funcion objetivo")
    for i in range(0, numVar):
        a = float(
            input("\tIngresa el coeficiente de x(" + str(i + 1) + "):\n\t -> "))
        fObjetivo.append(a)
    prec = int(input("\tIngresa la precision:\n\t -> "))
    numRest = int(input("\tIngresa el numero de restricciones:\n\t -> "))
    fRest = []
    for i in range(0, numRest):
        fRest.append([])
        print("\t\tIngresa los datos de la restriccion " + str(i + 1))
        for j in range(0, numVar):
            a = float(input("\tIngresa el coeficiente de x(" + str(j + 1) + "):\n\t -> "))
            fRest[i].append(a)
        signo = int(input("\tIngresa la condicion de la restriccion:\n\t -> "))
        fRest[i].append(signo)
        aux = float(input("\tIngresa el otro lado de la restriccion:\n\t -> "))
        fRest[i].append(aux)
    listaLimites = calcLimite(numVar, fRest)
    #print(listaLimites)
    listaMJ = []
    tamV = 0
    for i in range(0, numVar):
        nC = numeroCromo(listaLimites[i][0], listaLimites[i][1], prec)
        tamV = tamV + nC
        listaMJ.append(nC)
    pob = int(input("\tIngresa el tamanio de la poblacion:\n\t -> "))
    it = int(input("\tIngresa el numero de iteraciones:\n\t -> "))
    return [listaMJ, tamV, it, pob, listaLimites, fObjetivo, fRest]

def calcLimite(numVar, rest):
    numRes = len(rest)
    tablaLim = []
    for i in range(0, numRes):
        tablaLim.append([])
        for j in range(0, numVar):
            if rest[i][j] > 0:
                lim = rest[i][numVar + 1] / rest[i][j]
            else:
                lim = 0
            tablaLim[i].append(lim)
    limites = []
    for i in range(0, numVar):
        limites.append([])
        menor = 0
        mayor = 0
        for j in range(0, numRes):
            if menor > tablaLim[j][i]:
                menor = tablaLim[j][i]
            if mayor < tablaLim[j][i]:
                mayor = tablaLim[j][i]
        limites[i].append(menor)
        limites[i].append(mayor)
    return limites

def entradaLim():
    numVar = int(input("\tIngresa el numero de variables:\n\t -> "))
    fObjetivo = []
    print("\t\tIngresa los datos de la funcion objetivo")
    for i in range(0, numVar):
        a = float(input("\tIngresa el coeficiente de x(" + str(i + 1) + "):\n\t -> "))
        fObjetivo.append(a)
    prec = int(input("\tIngresa la precision:\n\t -> "))
    listaMJ = []
    listaLimites = []
    tamV = 0
    for i in range(0, numVar):
        limites = []
        aj = int(input("\tIngresa el limite inferior de x(" + str(i + 1) + "):\n\t -> "))
        bj = int(input("\tIngresa el limite superior de x(" + str(i + 1) + "):\n\t -> "))
        limites.append(aj)
        limites.append(bj)
        listaLimites.append(limites)
        nC = numeroCromo(aj, bj, prec)
        tamV = tamV + nC
        listaMJ.append(nC)
    pob = int(input("\tIngresa el tamanio de la poblacion:\n\t -> "))
    it = int(input("\tIngresa el numero de iteraciones:\n\t -> "))
    return [listaMJ, tamV, it, pob, listaLimites, fObjetivo]

def numeroCromo(inf, sup, prec):
    aux = (sup - inf)*10**prec
    mj = math.log(aux, 2)
    mj = math.ceil(mj)
    return mj

def validacion(restricciones, valores):
    numRes = len(restricciones)
    numVar = len(valores)
    for i in range(0, numRes):
        resultado = 0.0
        for j in range(0, numVar):
            resultado = resultado + restricciones[i][j] * valores[j]
        if restricciones[i][numVar] == 0:
            if (resultado > restricciones[i][numVar + 1] + restricciones[i][numVar + 1] * 0.05) or (resultado < restricciones[i][numVar + 1] - restricciones[i][numVar + 1] * 0.05):
                return False
        elif restricciones[i][numVar] == 1:
            if resultado > restricciones[i][numVar + 1]:
                return False
        elif restricciones[i][numVar] == 2:
            if resultado < restricciones[i][numVar + 1]:
                return False
        elif restricciones[i][numVar] == 3:
            if resultado >= restricciones[i][numVar + 1]:
                return False
        elif restricciones[i][numVar] == 4:
            if resultado <= restricciones[i][numVar + 1]:
                return False
    return True

def creaVec(sistema):
    if len(sistema) == 7:
        correcto = False
        while not correcto:
            v = []
            for i in range(0, sistema[1]):
                v.append(random.randint(0, 1))
            correcto = validacion(sistema[6], getValues(sistema, v))
        return v
    else:
        v = []
        for i in range(0, sistema[1]):
            v.append(random.randint(0, 1))
        return v

def mutacion(vOr):
    v = vOr[:]
    numMut = random.randrange(1, int(len(v)/2) + int(len(v)/6), 1)
    #print("Mutaciones: " + str(numMut))
    prevIndex = []
    for i in range(0, numMut):
        index = random.randrange(0, len(v) - 1, 1)
        repeat = True
        while repeat:
            repeat = False
            for e in prevIndex:
                if e == index:
                    index = random.randrange(0, len(v) - 1, 1)
                    repeat = True
        prevIndex.append(index)
        v[index] = 1 - v[index]
    return v

def cruce(v1, v2):
    index = random.randrange(1, len(v1) - 2, 1)
    #print("Indice Cruce: " + str(index))
    v = v1[:]
    v[index:len(v)] = v2[index:len(v2)]
    return v

def getValues(sistema, vector):
    mjs = sistema[0]
    index = 0
    i = 0
    values = []
    for mj in mjs:
        aj = sistema[4][i][0]
        bj = sistema[4][i][1]
        substr = "".join(str(e) for e in vector[index:index+mj])
        subint = int(substr, 2)
        v = aj + subint*((bj-aj)/(2**mj-1))
        values.append(v)
        i = i + 1
        index = index + mj
    return values

def eval(sistema, values):
    zAcum = 0
    zList = []
    survive = [False]*len(values)
    zPorList = []
    zPorAcum = []
    for value in values:
        i = 0
        z = 0
        for var in value:
            z = z + var * sistema[5][i]
            i = i + 1
        zAcum = zAcum + z
        zList.append(z)
    zPA = 0.0
    for z in zList:
        zPor = z / zAcum
        zPA = zPA + zPor
        zPorList.append(zPor)
        zPorAcum.append(zPA)
    survID = []
    for i in range(0, len(values)):
        r = random.random()
        found = False
        for j in range(0, len(survive)):
            if zPorAcum[j] > r and (not found):
                found = True
                survive[j] = True
                survID.append(j)
    return [zList, survive, list(set(survID))]

def evol(poblacion, results, sistema):
    for i in range(0, len(poblacion)):
        if not results[1][i]:
            if len(results[2]) >= 2:
                if random.random() <= 0.5:
                    index = random.choice(results[2])
                    #print("V" + str(i+1)+ " - Mutacion de V" + str(index+1))
                    poblacion[i] = mutacion(poblacion[index])
                    if len(sistema) == 7:
                        correcto = False
                        while not correcto:
                            index = random.choice(results[2])
                            poblacion[i] = mutacion(poblacion[index])
                            correcto = validacion(sistema[6], getValues(sistema, poblacion[i]))
                else:
                    index1 = random.choice(results[2])
                    index2 = index1
                    while index1 == index2:
                        index2 = random.choice(results[2])
                    #print("V" + str(i + 1) + " - Cruce de V" + str(index1+1) + " y V" + str(index2+1))
                    poblacion[i] = cruce(poblacion[index1], poblacion[index2])
                    if len(sistema) == 7:
                        correcto = False
                        while not correcto:
                            index1 = random.choice(results[2])
                            index2 = index1
                            while index1 == index2:
                                index2 = random.choice(results[2])
                            poblacion[i] = cruce(poblacion[index1], poblacion[index2])
                            correcto = validacion(sistema[6], getValues(sistema, poblacion[i]))
            else:
                index = random.choice(results[2])
                #print("V" + str(i + 1) + " - Mutacion de V" + str(index+1))
                poblacion[i] = mutacion(poblacion[index])
                if len(sistema) == 7:
                        correcto = False
                        while not correcto:
                            poblacion[i] = mutacion(poblacion[index])
                            correcto = validacion(sistema[6], getValues(sistema, poblacion[i]))
    return poblacion

def maxi(sistema):
    poblacion = []
    #print(sistema)
    for i in range(0, sistema[3]):
        poblacion.append(creaVec(sistema))
    for it in range(0, sistema[2]):
        #print("Iteracion " + str(it + 1) + ":")
        values = []
        for p in poblacion:
            #print(p)
            values.append(getValues(sistema, p))
        results = eval(sistema, values)
        poblacion = evol(poblacion, results, sistema)
    maxI = 0
    for i in range(0, len(results[0])):
        if(results[0][i] > results[0][maxI]):
            maxI = i
    print("Maximo V" + str(maxI + 1))
    print("Valor de z: " + str(results[0][maxI]))
    for i in range(0, len(values[maxI])):
        print("Valor de x(" + str(i + 1) + "): " + str(values[maxI][i]))

def mini(sistema):
    poblacion = []
    #print(sistema)
    for i in range(0, sistema[3]):
        poblacion.append(creaVec(sistema))
    for it in range(0, sistema[2]):
        #print("Iteracion " + str(it + 1) + ":")
        values = []
        for p in poblacion:
            #print(p)
            values.append(getValues(sistema, p))
        results = eval(sistema, values)
        poblacion = evol(poblacion, results, sistema)
    maxI = 0
    for i in range(0, len(results[0])):
        if(results[0][i] > results[0][maxI]):
            maxI = i
    print("Minimo V" + str(maxI + 1))
    print("Valor de z: " + str((-1)*results[0][maxI]))
    for i in range(0, len(values[maxI])):
        print("Valor de x(" + str(i + 1) + "): " + str(values[maxI][i]))


mode = int(input("\tEscoja un modo: \n\t1) Ingresar restricciones\n\t2) Ingresar limites\n\t -> "))
if mode == 1:
    sistema = entradaEc()
else:
    sistema = entradaLim()
maxi(sistema)
msistema = sistema[:]
for i in range(0, len(msistema[5])):
    msistema[5][i] = msistema[5][i] * (-1)
#print(sistema)
#print(msistema)
mini(msistema)
