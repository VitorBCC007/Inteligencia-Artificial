import random

# Tamanho da população inicial
POPULACAO_T = 300 #POPULAÇÃO

# Número de gerações
GERADOS = 400 #Gerações

# Tamanho do genoma
GENOMA = 10 #ANALISE de genoma

# Opções de alelos para cada gene
GENESOPCOES = { #DEFININDO AS OPÇÕES (A MENOR = - CHANCES)
    'idade': range(18, 100), #IDADE
    'imc': range(10, 40), #IMC
    'pressao_sangue': range(80, 200), #
    'colesterol': range(50, 300),#TEM COLESTEROL?
    'fumante': [True, False],# É FUMANTE?
    'alcool': [True, False],# CONSOME ALCOOL?
    'diabetes': [True, False], #TEM DIABETE?
    'dor_no_peito':[True, False], #SENTE DORES NO PEITO?
    'historicoFamilia': [True, False], #HISTÓRICO DA FAMILHA (CARDIACO)
    'exercicio': [0, 1, 2, 3, 4, 5, 6, 7] #PRÁTICA DE EXERCICIOS
    
}

# Função de fitness
def fitness(individuo):
    # Calcula o risco de problemas cardíacos com base nos genes do indivíduo
    
    idade = individual['idade'] 
    imc = individual['imc']
    pressao_sangue = individuo['pressao_sangue']
    colesterol = individuo['colesterol']
    fumante = individuo['fumante']
    alcool = individuo['alcool']
    diabetes = individuo['diabetes']
    dor_no_peito = individuo ['dor_no_peito']
    historicoFamilia = individuo['historicoFamilia']
    exercicio = individuo['exercicio']
    
    
    risco = 0  #RISCO inicial 
    
    if idade >= 45: 
        risco += 2
    
    if imc >= 25 and imc <= 30:#Abaixo / Normal
        risco += 1
    elif imc > 30: #Obesidade
        risco += 2
    
    if pressao_sangue >= 130 and pressao_sangue <= 139: #Normal / Pré Hipertensão  
        risco += 1
    elif pressao_sangue >= 140: #Hipertensão
        risco += 2
    
    if colesterol >= 131 and colesterol <= 160: #Normal/Alto
        risco += 1
    elif colesterol >= 240: #Alto demais
        risco += 2
    
    if fumante: 
        risco += 2
    
    if alcool:
        risco += 2

    if diabetes:
        risco += 2
    
    if dor_no_peito:
        risco +=2  
        
    if historicoFamilia:
        risco += 2  
    
    if exercicio <= 3:  #Abaixo de 3 a pessoa pratica pouco exercicio
        risco += 2

    

    return 1 / (risco + 1)
#LEMBRANDO: Mesmo que a idade seja alta a pessoa pode ter aspectos que a deixam em aptidão
#De acordo com as regras a cima.
#Exemplo uma pessoa com 80 anos que não fuma não tem problema de pressão nem colesterol alto
#não fuma, nem tem diabete . . . se torna mais apta que alguem que tem 18 fuma bebe colesterol. . .

# Função de seleção
def selection(population):
    # Seleciona os indivíduos mais aptos para se reproduzirem
    return sorted(population, key=fitness, reverse=True)[:int(POPULACAO_T/2)]

# Função de recombinação
def crossover(individuo1, individuo2):
    # Mistura os genes dos indivíduos selecionados para gerar novos indivíduos
    novo_individuo = {}
    
    for gene in individuo1:
        if random.random() < 0.5:
            novo_individuo[gene] = individuo1[gene]
        else:
            novo_individuo[gene] = individuo2[gene]
    
    return novo_individuo

# Função de mutação
def mutation(individual):
    # Altera aleatoriamente alguns dos genes de alguns indivíduos
    for gene in individual:
        if random.random() < 0.1:
            individual[gene] = random.choice(GENESOPCOES[gene])
    
    return individual

# Cria a população inicial
populacao = []

for i in range(POPULACAO_T):
    individual = {}
    
    for gene in GENESOPCOES:
        individual[gene] = random.choice(GENESOPCOES[gene])
    
    populacao.append(individual)

# Executa o algoritmo genético
for generation in range(GERADOS):
    print(f"Generation {generation + 1}")

    # Seleciona os indivíduos mais aptos para a reprodução
selected_population = selection(populacao)

# CRIANDO NOVOS INDIVIDUOS POR RECOMBINAÇÃO
mudoupopulacao = []

for i in range(int(POPULACAO_T/2)):
    parent1 = random.choice(selected_population) #CRIANDO UM DESCENTENTE 
    parent2 = random.choice(selected_population)
    
    filho1 = crossover(parent1, parent2)
    filho2 = crossover(parent1, parent2)
    
    mudoupopulacao.append(filho1) #Gerados por cruzamento P1+P2 (filhos/as)
    mudoupopulacao.append(filho2)
    

# Listando mutações
mutated_population = []

for individual in mudoupopulacao:
    if random.random() < 0.1:
        mutated_individual = mutation(individual)
        mutated_population.append(mutated_individual)
    else:
        mutated_population.append(individual)

# Substitui a população antiga pela nova
population = mutated_population


# Exibe o melhor indivíduo da geração atual
best_individual = max(population, key=fitness) #PEGANDO O MELHOR INDIVIDUO 
print(f"Melhor GENE possível: {best_individual}")
print(f"Fitness: {fitness(best_individual)}")
print("="*130)

print(f"\nPopulação final:\n\n {population}") #Toda população 
