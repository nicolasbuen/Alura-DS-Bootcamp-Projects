# Import libs
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def criar_dicionario_respostas(cod_pergunta: str, df, dicionario):

    '''
    Essa função serve como uma função helper para a criar_tab_freq(). Ela aceita
    um código de pergunta como argumento e retorna um dicionário com as váriaveis 
    como keys e as alternativas de resposta como values, além do index dessa pergunta
    no dicionário.

    cod_pergunta: string contendo o código da pergunta. Ex.: "VB02001"

    dicionario: variável em que está armazenado o dataframe contendo o arquivo 
    Dicionario_PENSE_Microdados_AMOSTRA2.xls.

    '''

    # fazendo a query e selecionando o index da pergunta no dicionário
    busca = dicionario.loc[dicionario['VARIÁVEL'] == cod_pergunta]
    index_pergunta = (busca.index).tolist()[0]

    # criando um dataframe somente para as possiveis respostas
    dataframe_respostas = pd.DataFrame(columns= ['VARIÁVEL','QUESTIONÁRIO DO ALUNO'])

    for index in range(index_pergunta + 1, index_pergunta + 20):
        if str(dicionario.loc[index]['VARIÁVEL'])[0].isalpha():
            break
        else:
            try:
                new_row = {'VARIÁVEL': int(dicionario.loc[index]['VARIÁVEL']),
                                  'QUESTIONÁRIO DO ALUNO' : dicionario.loc[index]['QUESTIONÁRIO DO ALUNO']}

                dataframe_respostas = dataframe_respostas.append(new_row, ignore_index = True)
            except ValueError:
                return dataframe_respostas.set_index("VARIÁVEL").to_dict(), index_pergunta

    return dataframe_respostas.set_index("VARIÁVEL").to_dict(), index_pergunta

def criar_tab_freq(cod_pergunta: str, df, dicionario, titulo_perg = '', plot = False):

    ''' 
    Essa função pede um código de pergunta e retorna um dataframe contendo a tabela
    de frequencia das respostas dessa pergunta na PeNSE 2015. 
    Ela aceita os seguintes argumentos:
  
    cod_pergunta: string contendo o código da pergunta. Ex.: "VB02001"
  
    titulo_pergunta: string contendo um novo titulo para a pergunta. Se deixado em
    branco, utiliza o original.

    dicionario: variável em que está armazenado o dataframe contendo o arquivo 
    Dicionario_PENSE_Microdados_AMOSTRA2.xls.

    df: variável em que está armazenado o dataframe contendo o arquivo 
    PENSE_AMOSTRA2_ALUNO.csv.

    plot: Aceita um boolean. Em caso de True, a função também plotara
    automaticamente um gráfico de barras da tabela de frequencia utilizando o sns.

    '''  

    # Criando o dict com as respostas e pegando index da pergunta no dicionario
    dict_respostas, idx = criar_dicionario_respostas(cod_pergunta, df, dicionario)

    # Calculando os dados de frequencia para a tabela
    frequencia = df[cod_pergunta].value_counts()
    percentual = df[cod_pergunta].value_counts(normalize = True) * 100

    # Selecionando o título da pergunta
    if titulo_perg == '':
        titulo_perg = dicionario.iloc[idx, 1] 

    # Criando a tabela
    tab_frequencia = pd.DataFrame({"frequencia":frequencia, "percentual":percentual})

    # Renomeando o index e as váriaveis
    tab_frequencia.rename(index = dict_respostas['QUESTIONÁRIO DO ALUNO'], inplace = True)

    tab_frequencia.rename_axis(titulo_perg, axis = 1, inplace = True)

    # Plotando
    if plot == True:
        fig, ax = plt.subplots(figsize = (7,5))
        sns.barplot(data = tab_frequencia, x = "percentual",
                    y = tab_frequencia.index,
                    ax = ax, alpha = 0.8, palette = 'colorblind')
    
        sns.despine()
        sns.set_context('notebook', font_scale = 1.3)
        plt.title(titulo_perg)
        plt.grid(axis = "x")
        plt.show()
        ax;

    return tab_frequencia

def plot_hist_e_estatisticas_de_centralidade(cod_pergunta: str, df, dicionario, hue = None, bins = 'auto'):
  
    '''
    Essa função plota um histograma utilizando o codigo de pergunta da base de
    dados PENSe e o seaborn, retornando objetos fig e ax. Ela aceita os seguintes 
    argumentos: 

    cod_pergunta: string contendo o código da pergunta. Ex.: "VB02001"
  
    hue: argumento da função histplot referente à coloração do histograma. 

    bins: número de containers utilizados no histograma.

    df: variável em que está armazenado o dataframe contendo o arquivo 
    PENSE_AMOSTRA2_ALUNO.csv.
    '''

    # Plot
    pal = sns.color_palette('colorblind')

    plt.figure(dpi=350)
    fig, ax = plt.subplots(figsize = (7,5))
    
    sns.boxplot(data = df, x = cod_pergunta, ax = ax,
              hue = hue,  dodge=False,  color = pal[0],
              saturation = 0.6)
    
    sns.despine()
    sns.set_context('notebook', font_scale = 1.3)

    # Hist Extras

    # media
  
    media = df[cod_pergunta].mean()
    moda = df[cod_pergunta].mode()
    print(f"\n=========\nMédia:{media} \nMediana:{np.median(df[cod_pergunta])}\nModa:{moda}\n=========\n\n")

    # desvio padrao
    desv_pad = [media - df[cod_pergunta].std(), df[cod_pergunta].std() + media]
    ax.axvspan(desv_pad[0], desv_pad[1], color = 'grey', alpha = 0.2, label = f"+/- 1 Desvio Padrão - {str(df[cod_pergunta].std())[:5]}") 

    # Customização
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2)
    ax.set_title(f"Distribuição de frequencia - {dicionario.loc[dicionario['VARIÁVEL'] == cod_pergunta]['QUESTIONÁRIO DO ALUNO']}")

    return fig, ax

def tldr_point_plot(df, title, grupos):
    
    '''
    Essa função plota um pointplot utilizando um dataframe de frequências já limo e o
    seaborn. Ela aceita os seguintes argumentos: 

    df: dataframe limpo
  
    title: titulo da pergunta. 

    grupos: categorias da frequencia no df.

    '''
    
    df_melted = pd.melt(df, id_vars = 'index', value_vars = grupos, var_name = 'grupo', value_name = 'percentual')
    
    fig, ax = plt.subplots(figsize = (7,5))

    sns.pointplot(data = df_melted,  y = 'index', x = 'percentual', hue = 'grupo',
                 alpha = 0.8, palette= 'colorblind')
    print(title)
    
    # Customização plot
    
    plt.grid()
    ax.legend(loc="lower right", bbox_to_anchor=(1.4, -0.0))
    sns.set_context("notebook", font_scale = 1.3)
    sns.despine()
    ax;