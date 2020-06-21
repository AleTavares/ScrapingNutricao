# Curso de Scraping
- Lab4 do curso de Scraping da https://www.datascienceacademy.com.br/

## Definição do Problema

Você já fez alguma refeição hoje? Se ainda não fez, deverá fazer em breve. Você saberia dizer quais são os ingredientes mais comuns nas refeições? E quais são os ingredientes que aparecem frequentemente juntos? E quais os métodos mais comuns no preparo de refeições? Qual a quantidade de porções usada com maior frequência? Qual a correlação entre os ingredientes para o cardápio ideal?

Responder essas e outras perguntas pode ajudar nutricionistas, escolas, restaurantes, indústrias de alimentos ou mesmo instituições de pesquisa, a fim de garantir que os padrões estejam sendo seguidos e que a saúde da população não esteja sendo comprometida com composições desbalanceadas de ingredientes.

Neste Lab trabalharemos nisso. Vamos analisar um conjunto de dados pouco comum, mas que vai ajudar você a pensar em diferentes problemas e o mais importante, em diferentes soluções. A Ciência de Dados pode ser aplicada a qualquer área, desde que nossa matéria-prima esteja disponível: dados.

E para responder nossas perguntas, vamos extrair e analisar a composição de receitas. Sim, isso mesmo. Receitas. De risoto, de frango e até de Fettuccine Alfredo!

O Web Scraping deste Lab é pesado e leva quase 50 minutos! Alguns parâmetros poderão reduzir esse tempo, mas nesse caso reduzirá também o volume de dados.

Para saber mais detalhes sobre alimentos e suas características, acesse:

<a href="https://www.abia.org.br/vsn/">ABIA - Associaçao Brasileira da Indústria de Alimentos</a>

Aqui tem um material de referência adicional que ajuda a explicar os benefícios da Ciência de Dados aplicada à Nutrição:

<a href="https://conferences.oreilly.com/strata/strata-ca-2019/public/schedule/detail/72551">Nutrition Data Science</a>


## Fonte de Dados

Nossa fonte de dados para o Web Scraping, será o portal <a href="https://www.allrecipes.com/">All Recipes</a> que contém receitas deliciosas. Navegue pelo site para compreender como os dados estão organizados. São várias páginas, cada qual com diversas receitas. Acesse o código fonte com o que você aprendeu no início do curso e análise as tags HTML.

Observe que o <a href="https://www.allrecipes.com/">All Recipes</a> possui dois layouts HTML diferentes para suas páginas de receita, um layout regular e um layout que suporta a compra de ingredientes diretamente da página da receita. Esses dois layouts têm as informações que precisamos em locais diferentes, portanto, precisamos diferenciá-los durante a raspagem dos dados. Se o elemento de título que procuramos inicialmente estiver definido como 'Nenhum', precisamos procurar os elementos onde eles estariam no segundo layout (comprador).

Vamos então extrair diversas receitas, limpar os dados e avaliar ingredientes, métodos de preparo e outros dados disponíveis.

Leia ATENTAMENTE todos os comentários e desenvolva suas habilidades em análise de dados. Elas podem ser empregadas em qualquer área, desde que dados estejam disponíveis.

## Bibliotecas
*Scraping*
- pip install bs4
- pip install json
- pip install requests
- pip install bs4

*Manipulação, Visualização e Análise de Dados*
- pip install re
- pip install numpy
- pip install pandas
- pip install seaborn
- pip install matplotlib
- pip install pathlib 

<a href="https://www.linkedin.com/in/alexandre-tavares/">Alexandre Tavares</a>