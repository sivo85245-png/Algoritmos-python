import csv # para manipulação de arquivos de logs em formato csv
import time # para medir tempo de execução
from datetime import datetime # para manipulação de data e hora
import matplotlib.pyplot as plt # para geração de graficos 

# ===============================,,
# Leitura do arquivo CSV de logs
# ===============================
def ler_logs_csv(caminho):# lê o arquivo csv e retorna uma lista de dicionarios 
    logs = [] # lista para armazenar os logs
    with open(caminho, newline='', encoding='utf-8') as arquivo:
        leitor = csv.DictReader(arquivo) #usa DictReader para facilitar o acesso a chave
        for linha in leitor: # Converte tipos apropriados
            linha["timestamp"] = datetime.fromisoformat(linha["timestamp"]) # Converte string Iso para datetime
            linha["status"] = int(linha["status"]) # converte status para inteiro
            linha["tamanho_bytes"] = int(linha["tamanho_bytes"]) # converte tamanho para inteiro
            logs.append(linha) # adiciona o log processado na lista
    return logs # retorna a lista de logs processados

# ===============================
# Algoritmos de ordenação
# ===============================

def bubble_sort_logs(logs, chave):
    lista = logs[:]
    n = len(lista)
    for i in range(n - 1):
        for j in range(n - 1 - i):
            if lista[j][chave] > lista[j + 1][chave]:
                lista[j], lista[j + 1] = lista[j + 1], lista[j]
    return lista

def selection_sort_logs(logs, chave):
    lista = logs[:]
    n = len(lista)
    for i in range(n - 1):
        min_index = i
        for j in range(i + 1, n):
            if lista[j][chave] < lista[min_index][chave]:
                min_index = j
        lista[i], lista[min_index] = lista[min_index], lista[i]
    return lista

def merge_sort_logs(logs, chave):# ordena usando merge sort
    if len(logs) <= 1:
        return logs
    meio = len(logs) // 2
    esquerda = merge_sort_logs(logs[:meio], chave)
    direita = merge_sort_logs(logs[meio:], chave)
    return merge_logs(esquerda, direita, chave)

def merge_logs(esquerda, direita, chave):# mescla duas listas ordenadas
    resultado = []
    i = j = 0
    while i < len(esquerda) and j < len(direita):
        if esquerda[i][chave] <= direita[j][chave]:
            resultado.append(esquerda[i])
            i += 1
        else:
            resultado.append(direita[j])
            j += 1
    resultado.extend(esquerda[i:])
    resultado.extend(direita[j:])
    return resultado

def quick_sort_logs(logs, chave):
    if len(logs) <= 1:
        return logs
    pivo = logs[0]
    menores = [item for item in logs[1:] if item[chave] <= pivo[chave]]
    maiores = [item for item in logs[1:] if item[chave] > pivo[chave]]
    return quick_sort_logs(menores, chave) + [pivo] + quick_sort_logs(maiores, chave)

# ===============================
# Funções de apoio
# ===============================

def imprimir_logs(logs): # impreme os logs no console 
    for log in logs:
        print(log["timestamp"], log["ip"], log["metodo"], log["rota"], log["status"])

def medir_tempo(funcao, logs, chave):# mede o tempo de execução de uma função de ordenação
    inicio = time.time()
    ordenado = funcao(logs, chave)
    fim = time.time()
    return (ordenado, fim - inicio)

def gerar_grafico_individual(nome_algoritmo, tempo_execucao):# gera um grafico de barras para o tempo de execução de um algoritmo
    plt.figure(figsize=(6,4))
    plt.bar([nome_algoritmo], [tempo_execucao])
    plt.title(f"Desempenho do {nome_algoritmo}")
    plt.ylabel("Tempo de Execução (segundos)")
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.show()

def gerar_grafico_comparacao(resultados):# gera um grafico comparativo entre os tempos de execução dos algortimos
    nomes = list(resultados.keys())
    tempos = list(resultados.values())

    plt.figure(figsize=(8,5))
    plt.bar(nomes, tempos)
    plt.title("Comparação de Desempenho dos Algoritmos de Ordenação")
    plt.xlabel("Algoritmo")
    plt.ylabel("Tempo de Execução (segundos)")
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.show()

# ===============================
# Função extra (análise avançada)
# ===============================
def analise_avancada(logs, chave): # analise avançada com mais detalhes 
    """
    - Mostra antes e depois
    - Mostra quantas linhas de log foram processadas
    - Calcula logs por segundo de cada algoritmo
    - Deixa pronto pra tu falar da aplicação real
    """

    total_logs = len(logs)
    print("\n[ANÁLISE AVANÇADA]")
    print(f"Total de linhas de log carregadas: {total_logs}\n")

    # medir cada algoritmo
    ordenado_bubble, t_bubble = medir_tempo(bubble_sort_logs, logs, chave)
    ordenado_selection, t_selection = medir_tempo(selection_sort_logs, logs, chave)
    ordenado_merge, t_merge = medir_tempo(merge_sort_logs, logs, chave)
    ordenado_quick, t_quick = medir_tempo(quick_sort_logs, logs, chave)

    # calcular logs/segundo (throughput)
    def taxa(logs_processados, tempo):
        if tempo == 0:
            return float('inf')
        return logs_processados / tempo

    bubble_rate    = taxa(total_logs, t_bubble)
    selection_rate = taxa(total_logs, t_selection)
    merge_rate     = taxa(total_logs, t_merge)
    quick_rate     = taxa(total_logs, t_quick)

    print("Tempo de execução (segundos):")
    print(f"- Bubble Sort:    {t_bubble:.8f} s  | {bubble_rate:.2f} logs/seg")
    print(f"- Selection Sort: {t_selection:.8f} s  | {selection_rate:.2f} logs/seg")
    print(f"- Merge Sort:     {t_merge:.8f} s  | {merge_rate:.2f} logs/seg")
    print(f"- Quick Sort:     {t_quick:.8f} s  | {quick_rate:.2f} logs/seg")

    # mostrar “antes e depois”
    print("\nPRIMEIROS 5 LOGS (ORIGINAL / NÃO ORDENADO):")
    for item in logs[:5]:
        print(item["timestamp"], item["ip"], item["rota"], item["status"])

    print("\nPRIMEIROS 5 LOGS (ORDENADO PELO QUICK SORT):")
    for item in ordenado_quick[:5]:
        print(item["timestamp"], item["ip"], item["rota"], item["status"])

    # gráfico de throughput (logs/segundo)
    nomes = ["Bubble", "Selection", "Merge", "Quick"]
    taxas = [bubble_rate, selection_rate, merge_rate, quick_rate]

    plt.figure(figsize=(8,5))
    plt.bar(nomes, taxas)
    plt.title("Taxa de Processamento (logs processados por segundo)")
    plt.xlabel("Algoritmo")
    plt.ylabel("Logs por segundo (maior é melhor)")
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.show()

    # esse retorno é so para facilitar testes automaticos
    return {
        "Bubble Sort":    {"tempo": t_bubble,    "logs_por_seg": bubble_rate},
        "Selection Sort": {"tempo": t_selection, "logs_por_seg": selection_rate},
        "Merge Sort":     {"tempo": t_merge,     "logs_por_seg": merge_rate},
        "Quick Sort":     {"tempo": t_quick,     "logs_por_seg": quick_rate},
    }

# ===============================
# Menu
# ===============================
def menu():
    print("\n======================")
    print("   APS - Ordenação")
    print("======================")
    print("1 - Bubble Sort")
    print("2 - Selection Sort")
    print("3 - Merge Sort")
    print("4 - Quick Sort")
    print("5 - Comparar desempenho (tempo de cada um)")
    print("6 - Análise avançada (antes/depois + logs por segundo)")
    print("0 - Sair")
    print("======================")
    escolha = input("Escolha uma opção: ")
    return escolha

# ===============================
# Programa principal
# ===============================
if __name__ == "__main__": # ponto de entrada do programa 
    caminho_csv = "logs_servidor.csv"
    logs_originais = ler_logs_csv(caminho_csv)
    chave_ordenacao = "timestamp"

    while True:
        opcao = menu()

        if opcao == "0":
            print("Encerrando...")
            break

        elif opcao == "1":
            print("\n[BUBBLE SORT]")
            ordenado, tempo_exec = medir_tempo(bubble_sort_logs, logs_originais, chave_ordenacao)
            print(f"Tempo de execução: {tempo_exec:.8f} segundos\n")
            imprimir_logs(ordenado)
            gerar_grafico_individual("Bubble Sort", tempo_exec)

        elif opcao == "2":
            print("\n[SELECTION SORT]")
            ordenado, tempo_exec = medir_tempo(selection_sort_logs, logs_originais, chave_ordenacao)
            print(f"Tempo de execução: {tempo_exec:.8f} segundos\n")
            imprimir_logs(ordenado)
            gerar_grafico_individual("Selection Sort", tempo_exec)

        elif opcao == "3":
            print("\n[MERGE SORT]")
            ordenado, tempo_exec = medir_tempo(merge_sort_logs, logs_originais, chave_ordenacao)
            print(f"Tempo de execução: {tempo_exec:.8f} segundos\n")
            imprimir_logs(ordenado)
            gerar_grafico_individual("Merge Sort", tempo_exec)

        elif opcao == "4":
            print("\n[QUICK SORT]")
            ordenado, tempo_exec = medir_tempo(quick_sort_logs, logs_originais, chave_ordenacao)
            print(f"Tempo de execução: {tempo_exec:.8f} segundos\n")
            imprimir_logs(ordenado)
            gerar_grafico_individual("Quick Sort", tempo_exec)

        elif opcao == "5":
            print("\n[COMPARAÇÃO DE DESEMPENHO - TEMPO TOTAL]")
            resultados_tempos = {}

            _, t_bubble    = medir_tempo(bubble_sort_logs,    logs_originais, chave_ordenacao)
            _, t_selection = medir_tempo(selection_sort_logs, logs_originais, chave_ordenacao)
            _, t_merge     = medir_tempo(merge_sort_logs,     logs_originais, chave_ordenacao)
            _, t_quick     = medir_tempo(quick_sort_logs,     logs_originais, chave_ordenacao)

            resultados_tempos["Bubble Sort"]    = t_bubble
            resultados_tempos["Selection Sort"] = t_selection
            resultados_tempos["Merge Sort"]     = t_merge
            resultados_tempos["Quick Sort"]     = t_quick

            print("\nTempos de execução (segundos):")
            for nome, t in resultados_tempos.items():
                print(f"- {nome}: {t:.8f}")

            gerar_grafico_comparacao(resultados_tempos)

        elif opcao == "6":
            analise_avancada(logs_originais, chave_ordenacao)

        else:
            print("\nOpção inválida. Tenta de novo.")
