import random

def entradaEc():
    numVar = int(input("\tIngresa el numero de variables:\n\t -> "))
    fObjetivo = []
    print("\t\tIngresa los datos de la funcion objetivo")
    for i in range(0, numVar):
        a = float(input("\tIngresa el coeficiente de x(" + str(i + 1) + "):\n\t -> "))
        fObjetivo.append(a)
    numRest = int(input("\tIngresa el numero de restricciones:\n\t -> "))
    fRest = []
    for i in range(0, numRest):
        fRest.append([])
        print("\t\tIngresa los datos de la restriccion " + str(i+1))
        for j in range(0, numVar):
            a = float(input("\tIngresa el coeficiente de x(" + str(j + 1) + "):\n\t -> "))
            fRest[i].append(a)
        signo = int(input("\tIngresa la condicion de la restriccion:\n\t -> "))
        fRest[i].append(signo)
        aux = float(input("\tIngresa el otro lado de la restriccion:\n\t -> "))
        fRest[i].append(aux)
    it = int(input("\tIngresa el numero de iteraciones:\n\t -> "))
    pob = int(input("\tIngresa el tamanio de la poblacion:\n\t -> "))
    retorno = []
    retorno.append(fObjetivo)
    retorno.append(fRest)
    retorno.append(it)
    retorno.append(pob)
    return retorno

def calcLimite(sistema):
    numVar = len(sistema[0])
    numRes = len(sistema[1])
    tablaLim = []
    for i in range(0, numRes):
        tablaLim.append([])
        for j in range(0, numVar):
            if sistema[1][i][j] > 0:
                lim = sistema[1][i][numVar+1] / sistema[1][i][j]
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

def creaRand(limites, sistema):
    numVar = len(limites)
    aleatorios = []
    for i in range(0, numVar):
        aleatorios.append([])
        for j in range(0, sistema[3]):
            aleatorio = random.random()*(int(limites[i][1])-int(limites[i][0])) + int(limites[i][0])
            aleatorios[i].append(aleatorio)
    return aleatorios

def validacion(restricciones, valores):
    numRes = len(restricciones)
    numVar = len(valores)
    for i in range(0, numRes):
        resultado = 0.0
        for j in range(0, numVar):
            resultado = resultado + restricciones[i][j] * valores[j]
        if restricciones[i][numVar] == 0:
            if (resultado > restricciones[i][numVar + 1] + restricciones[i][numVar + 1] * 0.05) or (resultado < restricciones[i][numVar + 1] - restricciones[i][numVar + 1]*0.05):
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

def eval(sistema, aleatorios):
    numVar = len(sistema[0])
    resultados = []
    indiceMay = 0
    indiceMen = 0
    priB = True
    for i in range(0, sistema[3]):
        vAValidar = []
        for columna in aleatorios:
            vAValidar.append(columna[i])
        if validacion(sistema[1], vAValidar):
            resultado = 0.0
            for j in range(0, numVar):
                resultado = resultado + sistema[0][j] * aleatorios[j][i]
            resultados.append(resultado)
            if priB:
                indiceMay = i
                indiceMen = i
                priB = False
            if resultados[indiceMay] < resultados[i]:
                indiceMay = i
            if resultados[indiceMen] > resultados[i]:
                indiceMen = i
        else:
            resultados.append("X")
    print("Valor de funcion objetivo mayor: " + str(resultados[indiceMay]))
    for i in range(0, numVar):
        print("Valor de x(" + str(i+1) + ") = " + str(aleatorios[i][indiceMay]))
    print("Valor de funcion objetivo menor: " + str(resultados[indiceMen]))
    for i in range(0, numVar):
        print("Valor de x(" + str(i+1) + ") = " + str(aleatorios[i][indiceMen]))
    #return [[resultados[indiceMay], aleatorios[:][indiceMay]], [resultados[indiceMen], aleatorios[:][indiceMen]]]

sistema = entradaEc()
limites = calcLimite(sistema)
print("Limites:", limites)
results = []
for i in range(0, sistema[2]):
    print("Iteracion: " + str(i+1))
    aleatorios = creaRand(limites, sistema)
    results.append(eval(sistema, aleatorios))
#maxI = 0
#minI = 0
#for i in range(0, len(results)):
    #if results[maxI][0][0] < results[i][0][0]:
        #maxI = i
    #if results[minI][1][0] > results[i][1][0]:
        #minI = i
#print("Maximo: " + str(results[maxI][0][0]))
#for i in range(0, len(results[maxI][0][1])):
    #print("Valor de x(" + str(i + 1) + ") = " + str(results[maxI][0][1][i]))
#print("Minimo: " + str(results[minI][0][0]))
#for i in range(0, len(results[minI][0][1])):
    #print("Valor de x(" + str(i + 1) + ") = " + str(results[minI][0][1][i]))
