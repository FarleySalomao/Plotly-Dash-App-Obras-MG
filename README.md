Painel analítico com dados das obras do cadastro nacional de obras (CNO) iniciadas entre 01/01/2020 a 31/05/2021 para o estado de Minas Gerais. Dashboard utilizando Plotly e Dash. O app pode ser acessado em:  https://obrasmg.herokuapp.com/ 

O painel consiste de dois componentes gráficos: 

  1. Mapa com a distribuição geográfica das obras. É possível categorizar as obras em termos da sua situação (ativa, encerrada, paralisada, suspensa), e também em termos de setor econômico de acordo com a Classificação Nacional de Atividades Econômicas (Mais informações sobre a estrutura da CNAE podem ser obtidas na página: https://cnae.ibge.gov.br/?view=estrutura). Também é possível selecionar o período de início das obras.  

  2. Gráfico de barras resumindo a informação do número totais de obras dividas por setor e por situação para o município selecionado. 

Os dados foram obtidos através do site da receita federal: https://www.gov.br/receitafederal/pt-br/assuntos/orientacao-tributaria/cadastros/consultas/dados-publicos-cno. 

O georreferenciamento foi feito utilizando a biblioteca Python Geopy (https://geopy.readthedocs.io/en/stable/) e a API de geocoding da Google  https://developers.google.com/maps/documentation/geocoding 
