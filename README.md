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

# Mas atenção !
para executar, não basta apenas rodar o código, precisa de uma credencial.json criada pelo google cloud.

<img width="942" height="466" alt="Captura de tela 2026-03-29 171020" src="https://github.com/user-attachments/assets/6057bb44-1214-4d48-988a-285118964a74" />

# Resultados

<img width="1200" height="688" alt="Captura de tela 2026-03-29 171710" src="https://github.com/user-attachments/assets/348fdf29-ac8d-4041-8a02-6304cce58adf" />


<img width="1003" height="672" alt="Captura de tela 2026-03-29 171900" src="https://github.com/user-attachments/assets/bdebfaa1-ca41-4666-ae29-cf0a5c8fae42" />


