# Imports para manipulação, visualização e análise de dados
import re
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import Path

# Começamos carregando o arquivo
dados = pd.read_json(r'dados/dataset.json')

# Vamos organizar as colunas
dados = dados[['titulo', 
               'porcoes', 
               'tempo_cozimento', 
               'tempo_preparo', 
               'tempo_adicional', 
               'tempo_total', 
               'ingredientes', 
               'metodo', 
               'layout', 
               'imagem']]

# Visualiza os dados
print(dados.head(3))

# Lista de palavras que representam medidas de unidade. Não pecisaremos disso.
medidas_unidades = ['gallon',
                    'quart',
                    'pint',
                    'cup',
                    'teaspoon',
                    'tablespoon',
                    'ounce',
                    'pound',
                    'can',
                    'pinch',
                    'serving',
                    'slice',
                    'package',
                    'bottle']

# Lista de descritores. Isso também não será necessário.
descritores = ['small', 'medium', 'large']

# Lista para os ingredientes depois da limpeza
lista_ingredientes_limpos = []

# Loop pela coluna de ingredientes de cada receita
for item in dados['ingredientes']:
    
    # Ingrediente a ser processado
    lista_ings = item
    
    # Remove medidas de unidade e descritores
    for palavra in medidas_unidades + descritores:
        plural = palavra + "s"
        lista_ings = [item.replace(' ' + plural + ' ', ' ') for item in lista_ings]
        lista_ings = [item.replace(' ' + palavra + ' ',' ') for item in lista_ings]    
    
    # Remove outros descritores comuns
    lista_ings = [item.replace('boneless,','') for item in lista_ings] 
    lista_ings = [item.replace('skinless,','') for item in lista_ings] 
    lista_ings = [item.replace('boneless','') for item in lista_ings] 
    lista_ings = [item.replace('skinless','') for item in lista_ings] 
    
    # Remove parenteses
    lista_ings = [re.sub(r'\([^()]*\)','', item) for item in lista_ings]
    
    # Divide texto depois de vírgulas
    lista_ings = [item.partition(',')[0] for item in lista_ings] 
    
    # Remove qualquer coisa que não seja caracter
    lista_ings = [re.sub(r'[^a-zA-Z]', ' ', item) for item in lista_ings]
    
    # Removemos espaços adicionais que ficaram depois de remover os itens anteriores
    lista_ings = [item.strip() for item in lista_ings] 

    # Substituímos o plural pelo singular
    lista_ings = [item.replace('eggs', 'egg') for item in lista_ings] 
    
    # Passamos os dados para um objeto temporário
    temp = lista_ings
    
    # Limpamos a lista
    lista_ings = []
    
    # Checamos pelos últimos elementos
    for item in temp:
        if 'chicken breast' in item:
            ing = 'chicken breast'
        elif 'chicken thigh' in item:
            ing = 'chicken thigh'
        elif 'chicken stock' in item:
            ing = 'chicken stock'
        elif 'ground beef' in item:
            ing = 'ground beef'
            
        # Adicionamos o item à lista    
        lista_ings.append(item)
    
    lista_ingredientes_limpos.append(lista_ings)

# Criamos uma nova coluna no dataset após a limpeza
dados['ingredientes_limpos'] = lista_ingredientes_limpos

# Visualizamos os dados antes e depois da limpeza
print(dados[['ingredientes', 'ingredientes_limpos']].head())

# Lista de ingredientes
lista_ingredientes = []

# Loop
for linha in dados['ingredientes_limpos']:
    for item in linha:
        lista_ingredientes.append(item)

# Dataframe de ingredientes
ingredientes = pd.DataFrame(lista_ingredientes, columns = ['ingrediente'])

# Visualiza os dados
print(ingredientes.head(10))

# Plot dos ingredientes mais comuns
n = 30
fig, ax = plt.subplots(figsize = (12, 12))
bar_positions = np.arange(n)
bar_heights = ingredientes['ingrediente'].value_counts().head(n)
bar_names = ingredientes['ingrediente'].value_counts().head(n).index
ax.barh(bar_positions, bar_heights, 0.6, color = 'green')
ax.set_yticks(bar_positions)
ax.set_yticklabels(bar_names)
ax.set_title('30 Ingredientes Mais Comuns (em ' + str(dados.shape[0]) + ' Receitas)')
ax.set_ylabel('\nIngredientes')
ax.set_xlabel('\nFrequência')
ax.invert_yaxis()
plt.show()

# Quais a distribuição dos tamanhos das porções?
# Plot
max = 30
fig = plt.figure(figsize = (14,14))
ax1 = fig.add_subplot(2, 1, 1)
ax2 = fig.add_subplot(2, 1, 2)
tick_values = 2 * np.arange(int(max/2))
tick_positions = tick_values + 0.5
ax1.hist(dados['porcoes'], bins = max, range = (0,max), color = 'purple')
ax1.set_title('\nDistribuição dos Tamanhos das Porções (em ' + str(dados.shape[0]) + ' Receitas)\n')
ax1.set_xticklabels(tick_values)
ax1.set_xticks(tick_positions)
ax1.set_ylabel('\nFrequência')
ax2.boxplot(dados['porcoes'], vert = False, sym = '')
ax2.set_xlim(0,max)
ax2.set_xticklabels(tick_values)
ax2.set_xticks(tick_positions)
ax2.set_yticks([])
ax2.set_xlabel('\nNúmero de Porções')
plt.show()

# Média de porções
print('São produzida em media {} porções por recceita.'.format(dados.porcoes.mean()))

# Quais as tendências que podem ser observadas nos títulos das receitas, com relação aos alimentos?
# Podemos examinar os títulos de cada receita para encontrar tendências comuns entre todas elas.

# Lista de palavras nos títulos
lista_palavras_titulos = []

# Palavras que serão evitadas
palavras_evitar = ['I', 'II', 'III', 'and', 'with']

# Loop para extrair as palavras
for linha in dados['titulo']:
    for palavra in linha.split(' '):
        
        # Extrai somente os caracteres
        palavra = re.sub('[^a-zA-Z]', '', palavra)
        
        # Verifica a palavra e grava na lista final
        if not palavra in palavras_evitar:
            lista_palavras_titulos.append(palavra)

# Cria o dataframe com as palavras extraídas dos títulos
lista_palavras = pd.DataFrame(lista_palavras_titulos, columns = ['palavra'])

# Plot
n = 50
fig, ax = plt.subplots(figsize = (15, 12))
bar_positions = np.arange(n)
bar_heights = lista_palavras['palavra'].value_counts().head(n)
bar_names = lista_palavras['palavra'].value_counts().head(n).index
ax.barh(bar_positions, bar_heights, 0.5, color = 'blue')
ax.set_yticks(bar_positions)
ax.set_yticklabels(bar_names)
ax.set_title('\nPalavras Mais Comuns nos Títulos (em ' + str(dados.shape[0]) + ' Receitas)\n')
ax.set_ylabel('\nPalavras')
ax.set_xlabel('\nFrequência')
ax.invert_yaxis()
plt.show()

# Quais os verbos mais usados no preparo dos alimentos?
# Lista de palavras
lista_palavras = []

# Loop pelos métodos de preparo
for metodo in dados['metodo']:
    for instruction in metodo:
        palavras = instruction.split(' ')
        for palavra in palavras:
            palavra = re.sub('[^a-zA-Z]', '', palavra).lower()
            lista_palavras.append(palavra)

# Cria o dataframe
palavras_metodo = pd.DataFrame(lista_palavras, columns = ['palavra'])

# Lista de palavras que representam "verbos culinários" (como cozinhar, mexer, misturar, etc...)
palavras_para_incluir = ['stir',
                         'cook',
                         'mix',
                         'place',
                         'add',
                         'bake',
                         'preheat',
                         'pour',
                         'cover',
                         'combine',
                         'remove',
                         'boil',
                         'cool',
                         'bring',
                         'simmer',
                         'set',
                         'sprinkle',
                         'beat',
                         'serve',
                         'drain',
                         'let']

# Lista
nova_lista = []

# Loop para criar a nova lista inserindo a lista de palavras acima
for metodo in dados['metodo']:
    for instruction in metodo:
        palavras = instruction.split(' ')
        for palavra in palavras:
            palavra = re.sub('[^a-zA-Z]', '', palavra).lower().strip()
            if palavra in palavras_para_incluir:
                nova_lista.append(palavra)

# Cria o dataframe
nova_lista_metodo = pd.DataFrame(nova_lista, columns = ['palavra'])

# Plot
n = len(nova_lista_metodo['palavra'].value_counts())
fig, ax = plt.subplots(figsize = (12,12))
bar_positions = np.arange(n)
bar_heights = nova_lista_metodo['palavra'].value_counts().head(n)
bar_names = nova_lista_metodo['palavra'].value_counts().head(n).index
ax.barh(bar_positions, bar_heights, 0.5, color = 'magenta')
ax.set_yticks(bar_positions)
ax.set_yticklabels(bar_names)
ax.set_title('\nPalavras Comuns nas Instruções de Preparo dos Alimentos (em ' + str(dados.shape[0]) + ' Receitas)\n')
ax.set_ylabel('\nInstruções')
ax.set_xlabel('\nFrequência')
ax.invert_yaxis()
plt.show()

# Quais ingredientes aparecem juntos com maior frequência?
# A parte final da análise será extrair pares de ingredientes comuns. Abordaremos esse problema relativamente complexo em duas etapas.

# Primeiro, vamos pegar um determinado ingrediente e encontrar seus pares mais comuns. Que tal batatas?

# Define um determinado ingrediente
ingrediente_escolhido = 'potatoes'

# Lista de valores booleanos
lista_verifica_ingrediente = []

# Lista para os pares dos ingredientes
pares_ingredientes = []

# Loop que verifica se o ingrediente que escolhemos ("potatoes") existe na lista de ingredientes limpos
for linha in dados['ingredientes_limpos']:
    
    tem_ing = False
    
    for item in linha:
        if item == ingrediente_escolhido:
            tem_ing = True
            
    lista_verifica_ingrediente.append(tem_ing)

# Loop para buscar os ingredientes que aparecem sempre que "potatoes" aparece na receita
for linha in dados[lista_verifica_ingrediente]['ingredientes_limpos']:
    
    for item in linha:
        if item == ingrediente_escolhido:
            continue
        else:
            pares_ingredientes.append(item)

# Cria o dataframe
df_pares_ingredientes = pd.DataFrame(pares_ingredientes, columns = ['pares'])

# Plot
n = 20
fig, ax = plt.subplots(figsize = (14,12))
bar_positions = np.arange(n)
bar_heights = df_pares_ingredientes['pares'].value_counts().head(n)
bar_names = df_pares_ingredientes['pares'].value_counts().head(n).index
print(bar_names)
print(bar_heights)
ax.barh(bar_names, bar_heights, 0.5, color = 'cyan')
ax.set_yticks(bar_positions)
ax.set_yticklabels(bar_names)
ax.set_title('\nIngredientes Mais Comuns com ' + ingrediente_escolhido.lower().capitalize() 
             + ' (' + str(dados.shape[0]) + ' Receitas)\n')
ax.set_ylabel('\nIngredientes')
ax.set_xlabel('\nFrequência')
ax.invert_yaxis()
plt.show()

# Especifica quantos dos ingredientes mais comuns devem ser considerados
top_n = 100  
top_n_ingredientes = ingredientes['ingrediente'].value_counts().head(top_n).index

# Listas de controle
todos_pares_ingredientes = []
lista_verificados = [] 

# Loop
for ing in top_n_ingredientes:
    
    lista_verifica_ingrediente = []
    
    # Cria uma máscara booleana para encontrar todas as linhas que contêm o ingrediente atual
    for linha in dados['ingredientes_limpos']:
        tem_ing = False
        for item in linha:
            if item == ingrediente_escolhido:
                tem_ing = True
                
        lista_verifica_ingrediente.append(tem_ing)
        
    # Pesquisa cada linha identificada pela máscara booleana e registra quais ingredientes aparecem com ela
    for linha in dados[lista_verifica_ingrediente]['ingredientes_limpos']:
        for item in linha:
            if item == ingrediente_escolhido:
                continue
            elif item in lista_verificados:
                continue
            else:
                tupla = (ingrediente_escolhido, item)
                todos_pares_ingredientes.append(tupla)
                
    lista_verificados.append(ingrediente_escolhido)

# Dataframe com pares de ingredientes
pares_ingredientes = pd.DataFrame(todos_pares_ingredientes, columns = ['ing1', 'ing2'])

# Combina os pares de ingredientes
pares_ingredientes['combinados'] = pares_ingredientes['ing1'] + ' / ' + pares_ingredientes['ing2']

# Visualiza os dados
print(pares_ingredientes.head(10))

# Conta os elementos
print(pares_ingredientes['combinados'].value_counts().head())



# Plot
n = 20
fig, ax = plt.subplots(figsize = (14,12))
bar_positions = np.arange(n)
bar_heights = pares_ingredientes['combinados'].value_counts().head(n)
bar_names = pares_ingredientes['combinados'].value_counts().head(n).index
ax.barh(bar_names, bar_heights, 0.5, color = 'red')
ax.set_yticks(bar_positions)
ax.set_yticklabels(bar_names)
ax.set_title('\nIngredientes Mais Comuns em Pares (em ' + str(dados.shape[0]) + ' Receitas)\n')
ax.set_ylabel('\nPares de Ingredientes')
ax.set_xlabel('\nFrequência')
ax.invert_yaxis()
plt.show()



