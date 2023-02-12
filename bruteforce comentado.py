# Projeto Interdisplicinar para Sistemas de Informação II
# Caio César Farias da Silva
# Algoritmo de Força Bruta para o Problema do Caixeiro Viajante
# Código com comentários 

def leitura(nome_arquivo):
    pontos = {} #Dicionário onde serão armazenadas as coordenadas.
    with open(nome_arquivo, 'r') as arquivo:
        linhas = arquivo.readlines()[1:] #A primeira linha do arquivo de texto contém a informação a respeito do tamanho da matriz, então ela é ignorada.
        for i in range(len(linhas)): #Para cada linha, onde i é a coordenada na posição da matriz.
            elementos = linhas[i].split() #Armazena os elementos, divindo eles em string.
            for j in range(len(elementos)): 
                elemento = elementos[j]
                if elemento != '0': #Se o elemento é diferente de 0, ele armazena em pontos.
                    pontos[elemento] = (i, j) #Retorna o ponto (chave), e as coordenadas i,j em uma tupla.
    return pontos #Todos os pontos diferentes do 0 e suas respectivas coordenadas.

#coordenadas = matriz('entrada1.txt')
#print(coord)
#{'D': (0, 4), 'A': (1, 1), 'C': (2, 4), 'R': (3, 0), 'B': (3, 2)}
entrada = leitura('entrada1.txt')
lista_de_pontos = list(entrada.keys()) #Transforma as chaves do dicionário em uma lista para poder ser permutada.
lista_de_pontos.remove('R') #Remover R das permutações.

def permutacao(pontos): #Vai gerar TODAS as combinações de rotas.
    if len(pontos) <= 1:
        return [pontos] #Casos base.
    permutacoes = [] #lista que armazenará cada permutação.
    for indice in range(len(pontos)): #Itera cada elemento da lista, travando-o e fazendo todas as suas comb. possíveis.
        elem_preso = pontos[indice] #elemento que vai ser "travado" e adicionado posteriormente nas permutações
        lista_solta = pontos[:indice] + pontos[indice + 1:] #O + 1: Remove o elemento chave da lista pontos e adiciona ele nessa lista.
        for p in permutacao(lista_solta): # 'p' é cada uma das permutações geradas com a lista sem chave.
            permutacoes.append([elem_preso] + p) # Adiciona o elemento que estava trancado, ao inicio de todas as permutações geradas sem ele.
    return permutacoes #retorna a lista de permutações
#Ex: [A, B, C] -> A travado -> BC/CB (p) -> A+BC // A+CB.

#teste2 = permutacao(lista_de_pontos)
#print(teste2)

perms = permutacao(lista_de_pontos)

def calculo_das_distancia(coord, rotas): #Essa função recebe o dicionário e as rotas possíveis (permutadas)
    menor_custo = 10**8 #inicialmente com um valor muito alto, para que qualquer custo calculado a seguir seja menor, e armazenado.
    melhor_rota = '' #string inicialmente vazia, que armazenará a melhor rota mediante o melhor valor.
    for r in rotas:
        custo = 0 #custo da rota que está sendo calculada
        r = ['R'] + r + ['R'] #adiciona o ponto R no começo e final de cada rota que for calculada, pois a lista_de_pontos não possui R.
        for i in range(len(r) - 1):
            x1, y1 = coord[r[i]] #coodenadas do primeiro elemento
            x2, y2 = coord[r[i+1]] #coordenadas do segundo elemento
            custo += abs(x1 - x2) + abs(y1 - y2) #incrementação do custo mediante a geometria euclidiana
        if custo < menor_cust: #condicional de comparação, que armazenará o custo caso ele seja menor que 10^8.
            menor_cust = custo 
            melhor_rota = ''.join(r) #se o custo for menor, a rota correspondente 'r', é armazenada na string.
    return f'O menor trajeto foi {melhor_rota}, custando {menor_custo} dronometros.' #Resposta quando a função for impressa.

print(calculo_das_distancia(entrada, perms)) #utiliza os dois parametros (de dicionário e de permutação), para efetuar o cálculo e então imprimir a mensagem de retorno da função.