# Recomendação de Compra e Venda de Imóveis

Neste projeto de insights se resolve um problema de negócio de uma imobiliária. Baseado em dados públicos é realizada uma limpeza e análise nos dados coletados para encontrar possíveis soluções a várias questões que poderiam surgir num ambiente deste tipo.  

## Problema de Negócio

A House Rocket (HR) é uma empresa que tem como modelo de negócio, a compra e venda de imóveis usando tecnologia. E, devido a que o seu portfólio de imóveis é muito grande e com muitos atributos (ou características), não tem como realizar o trabalho de forma manual. O intuito da empresa é maximizar a sua receita comprando imóveis baratos, idealmente bem localizados, e vendê-los, posteriormente, a preços mais altos. Desta forma, o modelo de receita (ou lucro) da empresa estaria determinado pela diferença entre os valores de compra e venda. 

De acordo com o anterior, se busca dar resposta às seguintes perguntas:

1. Quais são os imóveis que a HR deveria comprar e por qual preço?
2. Uma vez a casa comprada, qual o melhor momento para vendê-la e por qual preço?
3. A HR deveria fazer uma reforma para aumentar o preço da venda? Quais seriam as sugestões de mudanças? Qual o incremento no preço dado por cada opção de reforma?
4. Dos imóveis comprados quantos e quais a HR vender, como mínimo, para o projeto se pagar?

## Premissas de Negócio

 1. A região (atributo *zipcode*) influencia fortemente os preços dos imóveis.
 
 2. Os imóveis baratos estão abaixo da mediana de preços e os caros estão acima. Imóveis com preço igual à mediana são considerados como caros.
 
 3. Temos, ao longo do ano, duas faixas para a sazonalidade das regiões, inverno e verão.    
   
 4. O lucro por revenda é de 10% ou 30% acima do preço de compra. Imóveis comprados abaixo da mediana do preço numa determinada região e sazonalidade são revendidos com lucro de 30%. Imóveis comprados com valor igual ou maior à mediana são revendidos para terem lucro de 10%.

 5. Os imóveis com nota (atributo *condition*) 1 ou 2 se consideram em más condições, os que tem nota 3 em condições regulares e os que tem nota 4 ou 5 em boas condições.

 6. Um imóvel fica como novo se foi reformado (atributo *yr_renovated*). O valor de 0 para essa coluna corresponde a um imóvel não-formado.
    
 7. Os imóveis antigos são aqueles que tem uma idade superior ou igual a 20 anos.

 8. Imóveis em condições regulares e/ou antigos se valorizam entre 5% e 25%, acima do preço de compra, quando feitas reformas pequenas. Para os imóveis novos e em boas condições não se sugerem reformas deste tipo.
    
 9. Um imóvel reformado com um incremento no número de quartos, igual a um, se valoriza em 25% acima do preço de compra.
    
 10. Um imóvel de três (03) quartos, com área construída (atributo *sqft_living*) superior à mediana dos imóveis com três (03) quartos e inferior à mediana dos imóveis com quatro (04) quartos, tem o potencial de ser reformado com um incremento no número de quartos, igual a um.
    
 11. Imóveis sem porão (atributo *basement*) tem o potencial de reforma para ter um. Os imóveis se valorizam em 15% acima do preço de compra.
 
 12. Imóveis com preços acima de 1300000 são desconsiderados da análise (possíveis erros do sistema).

 13. Reformas por condição e idade deixam os imóveis como novos e em boas condições.
 
## Planejamento da Solução

1. Coletar os dados (https://www.kaggle.com/datasets/harlfoxem/housesalesprediction).
2. Limpar os dados (Data Cleaning). Este passo aborda a descrição dos dados (*Data Description*), engenharia de features (*Feature Engineering*) e a filtragem de variáveis (*Variable Filtering*).
3. Análise exploratória dos dados (*Exploratory Data Analysis* - EDA). Este passo aborda a formulação e validação das hipóteses de negócio.
4. Possíveis soluções às questões de negócio. 

## Principais *Insights*

1. Os imóveis mais novos que estão em boas condições deveriam ser 30% mais caros, na média, que os imóveis antigos em condições regulares (Hipótese verdadeira).

2. Imóveis novos e em boas condições são 70% mais ofertados que imóveis antigos e em condições regulares (Hipótese falsa).
   - Hipótese validada: Por cada imóvel novo em boas condições temos, aproximadamente, 64 imóveis antigos em condições regulares ofertados.

3. Imóveis de 3 quartos com reforma para ter mais um, se valorizam em 30%, na média (Hipótese verdadeira).

4. Imóveis próximos do centro da cidade deveriam ser um 30% mais caros, na média, dos que estão mais afastados (Hipótese verdadeira).   

5. Imóveis com porão são 40% mais caros, na média, do que os imóveis sem porão (Hipótese falsa).
   - Hipótese validada: Imóveis com porão são 27% mais caros, na média, do que os imóveis sem porão.

## Resultados Financeiros para o Negócio

O lucro por revenda dos imóveis recomendados para compra, isto é, imóveis baratos e em boas condições, é de 19,4%. Considerando, ainda, lucros maiores para imóveis com melhor localização (0,8%) e com vista para água (0,2%). A planilha 01 mostra os imóveis recomendados para compra e, a planilha 02, mostra os preços de venda, os lucros e a datas de venda, entre outros atributos. O percentual dos imóveis sugeridos para compra é de 18,4 % sobre o total do portfólio.

Se considerarmos os imóveis em condições regulares para compra, se reformam e se aumenta o preço de venda, o percentual de lucro total vai para 89%. As reformas sugeridas são: 1. reforma por aumento no número de quartos em 01 (lucro de 7%), 2. reforma por construção de porão (lucro de 13%), e 3. reformas "pequenas" em imóveis velhos e/ou novos que se encontram em condições regulares (42%). A planilha 03 mostra os imóveis sugeridos para compra. O percentual dos imóveis sugeridos para compra é de 49 % sobre o total do portfólio.

Sobre as condiciones mencionadas anteriormente, o percentual mínimo de imóveis que a HR deve vender para o projeto se pagar é de 38%. Ou, 3976 imóveis de 10498. A planilha 04 mostra a ordem, preço e data de venda em que se deveriam vender os imóveis, entre outros atributos.

Como parte deste projeto também foi criado um *dashboard* interativo na nuvem, usando o Streamlit Cloud. Para ver o modelo em produção visite o link: https://yavalenzuelae-python-do-zero-ao-ds-my-dashboard-9315bj.streamlit.app/.   

## Conclusão

A EDA no portfólio da HR permitiu encontrar os imóveis recomendados para compra e venda. Dos 21416 imóveis considerados no portfólio 10498 são recomendados, 49% do total. O lucro estimado é de 89% sobre o investimento nos imóveis recomendados e, se um 38% dos imóveis comprados são vendidos, se consegue pagar o projeto.

## Perspectivas

Desenvolvimento de um modelo de Aprendizado de Máquina (*Machine Learning*) para previsão de preços de venda.    
