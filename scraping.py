# Imports para Web Scraping
import bs4
import json
import requests
from bs4 import BeautifulSoup as bs
from pathlib import Path

# Função que salva o conteúdo de cada página (as receitas de cada página) em um arquivo JSON
def salva_receita(title, 
                  layout, 
                  picture, 
                  servings, 
                  ingredients, 
                  method, 
                  prep_time, 
                  cook_time, 
                  additional_time, 
                  total_time):
    
    # Cria uma lista para receber o conteúdo das páginas, ou seja, todas as receitas em cada página
    lista_receitas = []
        
    # Define o nome do arquivo em disco
    receitas_arquivo = Path("dados/dataset.json")
    
    # Verifica se o arquivo existe em disco e se existir carregamos o arquivo
    if receitas_arquivo.is_file():
        with open(receitas_arquivo) as in_file:
            lista_receitas = json.load(in_file)
        
        # Atribui False à variável de controle
        ja_existe = False
        
        # Vamos checar se a receita já está na lista
        for receita in lista_receitas:
            if receita['titulo'] == title:
                ja_existe = True
        
        # Se a receita não estiver na lista, então incluímos a receita
        if not ja_existe:
            print("Receita Incluída na Lista: {} ".format(title))
            nova_receita = {}
            nova_receita['titulo'] = title
            nova_receita['layout'] = layout
            nova_receita['imagem'] = picture
            nova_receita['ingredientes'] = ingredients
            nova_receita['metodo'] = method
            nova_receita['porcoes'] = servings
            nova_receita['tempo_preparo'] = prep_time
            nova_receita['tempo_cozimento'] = cook_time
            nova_receita['tempo_adicional'] = additional_time
            nova_receita['tempo_total'] = total_time
        
            # Adiciona a nova receita na lista
            lista_receitas.append(nova_receita)
    
            # Grava no arquivo
            with open('dados/dataset.json', 'w') as arquivo:
                json.dump(lista_receitas, arquivo, indent = 4)
        else:
            print("Esta Receita já está na Lista: {} ".format(title))
            
    # Se o arquivo não existir, será criado pela primeira vez já com as receitas da primeira página 
    else:
        print("Título da Receita: {} ".format(title))
        nova_receita = {}
        nova_receita['titulo'] = title
        nova_receita['layout'] = layout
        nova_receita['imagem'] = picture
        nova_receita['ingredientes'] = ingredients
        nova_receita['metodo'] = method
        nova_receita['porcoes'] = servings
        nova_receita['tempo_preparo'] = prep_time
        nova_receita['tempo_cozimento'] = cook_time
        nova_receita['tempo_adicional'] = additional_time
        nova_receita['tempo_total'] = total_time
        
        # Adiciona a nova receita na lista
        lista_receitas.append(nova_receita)
    
        # Grava no arquivo
        with open('dados/dataset.json', 'w') as arquivo:
            json.dump(lista_receitas, arquivo, indent = 4)

# Vamos definir quantas páginas de dados serão extraídas
# Evite colocar muitas páginas, pois o processo pode ser demorado
primeira_pagina = 101
ultima_pagina = 200

print("Iniciando Web Scraping! Isso vai demorar. Seja paciente!")

# Loop pelo range de páginas que você definiu com os 2 parâmetros anteriores
for page in range(primeira_pagina, ultima_pagina + 1):
    
    # Requisição à página
    source = requests.get("https://www.allrecipes.com/recipes?page=" + str(page))
    print("\nPágina Sendo Processada: {}".format(page))
    
    # Código fonte (HTML) da página
    doc = bs(source.text, 'html.parser')
    
    # Selecionamos cada receita vinculada à página e abrimos os links um por um
    recipe_cards = doc.select('a.fixed-recipe-card__title-link')

    # Loop por todas as receitas de cada página
    for card in recipe_cards:
        
        # Aqui estão os dados que iremos extrair
        # Vamos criar e inicializar as variáveis
        layout = 0
        ingredients_list = []
        method_list = []
        title, picture = '', ''
        prep_time, cook_time, total_time, additional_time, servings, = '','','','',''
        
        # Abrimos então a página de cada receita e fazemos o parse do código HTML
        recipe_page_source = requests.get(card['href'])    
        
        # Copiamos então o conteúdo principal da página (texto da receita)
        recipe_main = bs(recipe_page_source.text, 'html.parser')
        
        # Agora pesquisamos pelos dados que declaramos acima
        title = recipe_main.select_one('.recipe-summary__h1')
        
        # Se o título não estiver em branco, extraímos os dados e nesse caso o layout é 1
        if title is not None:
            layout = 1
            title = title.text
            picture = recipe_main.select_one('.rec-photo').attrs['src']
            ingredients = recipe_main.select('.recipe-ingred_txt')
            method = recipe_main.select('.recipe-directions__list--item')
            servings = recipe_main.select_one('#metaRecipeServings')['content']
            meta_item_types = recipe_main.select('.prepTime__item--type')
            meta_item_times = recipe_main.select('.prepTime__item--time')
            
            # Queremos os tempos de preparo de cada receita. Vamos extrair.
            for label, time in zip(meta_item_types, meta_item_times):
                if label.text == 'Prep':
                    prep_time = time.text
                elif label.text =='Cook':
                    cook_time = time.text
                elif label.text == 'Additional':
                    additional_time = time.text
                elif label.text == 'Ready In':
                    total_time = time.text                
                
        # Se o título for None, a página é diferente e nesse caso o layout é igual a 2
        else:
            layout = 2
            title = recipe_main.select_one('h1.headline.heading-content').text
            picture = recipe_main.select_one('.inner-container > img').attrs['src']
            ingredients = recipe_main.select('span.ingredients-item-name')
            method = recipe_main.select('div.paragraph > p')
            meta_items = recipe_main.select('div.recipe-meta-item')
            
            for item in meta_items:
                parts = item.select('div')
                header = parts[0].text.strip()
                body = parts[1].text.strip()
                    
                if header == 'prep:':
                    prep_time = body
                elif header =='cook:':
                    cook_time = body
                elif header == 'additional:':
                    additional_time = body
                elif header == 'total:':
                    total_time = body
                elif header == 'Servings:':
                    servings = body
        
        # Compilamos a lista de ingredientes da receita
        for ingredient in ingredients:
            if ingredient.text != 'Add all ingredients to list' and ingredient.text != '':
                ingredients_list.append(ingredient.text.strip())
            
        # Compilamos a lista de métodos da receita
        for instruction in method:
            method_list.append(instruction.text.strip())
        
        # Se ingredientes ou lista de métodos estiverem vazios, não gravamos os dados
        if len(ingredients_list)==0 and len(method_list) == 0:
            pass
        else:
            # Se tudo ok chamamos a função e gravamos os dados em disco
            salva_receita(title, layout, picture, servings, ingredients_list, method_list, 
                          prep_time, cook_time, additional_time, total_time)
        
print("Web Scraping Concluído com Sucesso!")