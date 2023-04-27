import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

temperatura = ctrl.Antecedent(np.arange(0, 101, 1), 'temperatura')
velocidade = ctrl.Consequent(np.arange(0, 101, 1), 'velocidade')

temperatura['fria'] = fuzz.trimf(temperatura.universe, [0, 20, 40])
temperatura['morna'] = fuzz.trimf(temperatura.universe, [20, 50, 80])
temperatura['quente'] = fuzz.trimf(temperatura.universe, [50, 100, 100])

velocidade['fraca'] = fuzz.trimf(velocidade.universe, [0, 30, 60])
velocidade['media'] = fuzz.trimf(velocidade.universe, [30, 60, 90])
velocidade['forte'] = fuzz.trimf(velocidade.universe, [60, 100, 100])

regra1 = ctrl.Rule(temperatura['fria'], velocidade['fraca'])
regra2 = ctrl.Rule(temperatura['morna'], velocidade['media'])
regra3 = ctrl.Rule(temperatura['quente'], velocidade['forte'])

sistema_controle = ctrl.ControlSystem([regra1, regra2, regra3])
sistema = ctrl.ControlSystemSimulation(sistema_controle)

temperatura_desejada = float(input("Digite a temperatura desejada para o chuveiro: "))

sistema.input['temperatura'] = temperatura_desejada

# RESULTADOS OBTIDOS DE ACORDO COM AS R1,2,3
sistema.compute()

velocidade_ideal = sistema.output['velocidade']
print("A velocidade ideal para a temperatura de %.1f°C é de %.1f%%." % (temperatura_desejada, velocidade_ideal))

# PLOTANDO OS GRÁFICOS DAS FUNÇÕES DE PERTINENCIA
temperatura.view(sim=sistema)
velocidade.view(sim=sistema)

plt.show(block=True)
plt.pause(5) 
plt.close()
