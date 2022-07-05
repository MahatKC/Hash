import time
import pandas as pd
from os.path import exists
pd.set_option("display.precision", 6)

def abrir_arquivos(tamanho_conjunto):
    with open("C10/Construir"+str(tamanho_conjunto)+".txt", "r") as arquivo_construir:
        string_elements = arquivo_construir.readline().split(' ')
        build_list = [int(ele) for ele in string_elements[:-1]]
    
    with open("C10/Consultar"+str(tamanho_conjunto)+".txt", "r") as arquivo_consultar:
        string_elements = arquivo_consultar.readline().split(' ')
        query_list = [int(ele) for ele in string_elements[:-1]]

    return build_list, query_list

def build_encadeamento(build_list, funcao_hash, alfa):

    tamanho = int(len(build_list)/alfa)
    num_build_encadeamento = 0
    t0 = time.time()
    tab_encadeamento = [ [] for _ in range(tamanho) ] 

    for elemento in build_list:
        index = funcao_hash(elemento, tamanho)
        num_build_encadeamento += len(tab_encadeamento[index])
        tab_encadeamento[index].append(elemento)

    num_empty_positions = 0
    for lista_encadeada in tab_encadeamento:
        if len(lista_encadeada) == 0:
            num_empty_positions += 1

    t1 = time.time()
    t_build_encadeamento = t1-t0
    return t_build_encadeamento, num_build_encadeamento, tab_encadeamento, num_empty_positions

def build_end_aberto(build_list, funcao_hash, alfa):

    tamanho = int(len(build_list)/alfa)
    num_elementos_colisores = 0
    num_build_end_aberto = 0
    t0 = time.time()
    tab_end_aberto = ['']*tamanho

    for elemento in build_list:
        index = funcao_hash(elemento, tamanho)
        colidiu = False
        while tab_end_aberto[index%tamanho] != '':
            colidiu = True
            index += 1
            num_build_end_aberto +=1
        if colidiu:
            num_elementos_colisores += 1
        tab_end_aberto[index%tamanho] = elemento
            
    t1 = time.time()
    t_build_end_aberto = t1-t0

    return t_build_end_aberto, num_build_end_aberto, tab_end_aberto, num_elementos_colisores

def query_encadeamento(query_list, tab_encadeamento, funcao_hash, alfa):

    tamanho = int(len(query_list)/alfa)
    num_query_encadeamento, num_hits_encadeamento = 0,0
    t0 = time.time()

    for elemento in query_list:
        index = funcao_hash(elemento, tamanho)
        lista_encadeada = tab_encadeamento[index]
        for no in lista_encadeada:
            num_query_encadeamento += 1
            if(no == elemento):
                num_hits_encadeamento += 1
                break
        
    t1 = time.time()
    t_query_encadeamento = t1-t0

    return t_query_encadeamento, num_query_encadeamento, num_hits_encadeamento

def query_end_aberto(query_list, tab_end_aberto, funcao_hash, alfa):

    tamanho = int(len(query_list)/alfa)
    num_query_end_aberto, num_miss_end_aberto = 1,0
    t0 = time.time()

    for elemento in query_list:
        index = funcao_hash(elemento, tamanho)
        valor = tab_end_aberto[index]
        index_ini = index
        while valor != elemento:
            index += 1
            num_query_end_aberto += 1
            valor = tab_end_aberto[index%tamanho]
            if (index%tamanho) == index_ini:
                num_miss_end_aberto += 1
                break
       
    t1 = time.time()
    t_query_end_aberto = t1-t0

    return t_query_end_aberto, num_query_end_aberto, num_miss_end_aberto

def mod_tam(val, tam):
    key = val%(int(tam))

    return key

def mod_quarter_tam(val, tam):
    key = (val%(int(tam/4)))*4

    return key

def constant(val, tam):
    return 25

if __name__=="__main__":
    #tamanhos_conjuntos = [100000]
    #tamanhos_conjuntos = [50, 100, 200, 300, 500, 750, 1000, 1500, 2000, 3000] #, 
    tamanhos_conjuntos = [5000, 7500, 10000, 12500, 15000, 20000, 25000, 30000, 40000, 50000, 75000, 100000]
    funcoes_hash = [mod_tam, mod_quarter_tam, constant]
    alfas = [0.5, 1]

    for funcao_hash in funcoes_hash:
        for alfa in alfas:
            for tamanho_conjunto in tamanhos_conjuntos:
                print(f"Tamanho {tamanho_conjunto}")
                t0 = time.time()
                build_list, query_list = abrir_arquivos(tamanho_conjunto)

                t_build_encadeamento, num_build_encadeamento, tab_encadeamento, num_empty_positions = build_encadeamento(build_list, funcao_hash, alfa)
                t_build_end_aberto, num_build_end_aberto, tab_end_aberto, num_elementos_colisores = build_end_aberto(build_list, funcao_hash, alfa)
                
                t_query_encadeamento, num_query_encadeamento, num_hits_encadeamento = query_encadeamento(query_list, tab_encadeamento, funcao_hash, alfa)
                t_query_end_aberto, num_query_end_aberto, num_miss_end_aberto = query_end_aberto(query_list, tab_end_aberto, funcao_hash, alfa)

                num_hits_end_aberto = tamanho_conjunto - num_miss_end_aberto
                if alfa==0.5:
                    percentual_colisao_encadeamento = (num_empty_positions-tamanho_conjunto)/tamanho_conjunto
                else:
                    percentual_colisao_encadeamento = num_empty_positions/tamanho_conjunto

                #print(tab_encadeamento)
                #print(num_empty_positions)

                results = pd.DataFrame({
                        'Função Hash': [funcao_hash.__name__],
                        'Percentual colisão encadeamento':[percentual_colisao_encadeamento],
                        'Percentual colisão endereçamento aberto':[num_elementos_colisores/tamanho_conjunto],
                        'Tamanho': [tamanho_conjunto],
                        'Alfa': [alfa],
                        'Tempo Construção Encadeamento': [t_build_encadeamento],
                        'Número Comparações Construção Encadeamento': [num_build_encadeamento],
                        'Tempo Construção Endereçamento Aberto': [t_build_end_aberto],
                        'Número Comparações Construção Endereçamento Aberto': [num_build_end_aberto],
                        'Tempo Consulta Encadeamento': [t_query_encadeamento],
                        'Número Comparações Consulta Encadeamento': [num_query_encadeamento],
                        'Tempo Consulta Endereçamento Aberto': [t_query_end_aberto],
                        'Número Comparações Consulta Endereçamento Aberto': [num_query_end_aberto],
                        'Número de Hits Encadeamento': [num_hits_encadeamento],
                        'Número de Hits Endereçamento Aberto': [num_hits_end_aberto]
                    })
                
                if exists("Reultados.csv"):
                    file_df = pd.read_csv("Reultados.csv")
                    file_df = pd.concat([file_df,results], ignore_index=True)
                    file_df.to_csv("Reultados.csv",index=False)
                else:
                    results.to_csv("Reultados.csv",index=False)
                    
                t1 = time.time()
                print(f"Tempo decorrido: {round(t1-t0,6)} seg")
                print("-"*10)