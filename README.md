# O que esse projeto faz ?
Esse esboço já nos entrega boa parte do que vamos precisar usar o projeto de fato:

- leitura da base
- seleção das variáveis
- padronização
- treinamento do IsolationForest (O mais importante)
- classificação entre **normal** e **anomalia**
- um gráfico de disperção para visualizar o comportamento dos pontos 

# Como interpretar?
No Isolation Forest ou no IForest

- 1 -> como sendo registro normal 
- (-1) -> como sendo registro anômalo

E uma coluna score onde valores mais baixos geralmente indicam registros mais suspeitos

# Qual a base utilizada ?
foi uma planilha do google sheets com alguns dados fictícios de obras para analise e validação do treinamento.

nesse link: https://docs.google.com/spreadsheets/d/1oQgFTTb6MEdZLMJkz-Lb-93MY2DpsYz5M_Lx-Tfqi28/edit?gid=1202364595#gid=1202364595

# Mas atenção 
para executar não basta apenas rodar o código precisa de uma credencial.json criada pelo google cloud
