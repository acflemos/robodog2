# -*- coding: utf-8 -*-

# =============================================================================
# rbd_md.py — Modelo de Domínio do robodog2
#
# Portado do robodog1 (ROS1) para ROS2 Humble.
# Principais mudanças:
#   - goal.target_pose.* → goal.pose.* (estrutura do NavigateToPose.Goal)
#   - Bug corrigido: TAREFAS.tarefa() agora decrementa self.pesos_tarefas em vez
#     de chamar decrementa_peso_tarefa() que modificava apenas a lista global
#   - Adicionado TAREFAS.verifica_pesos_negativos() e chamada em prioriza_tarefas()
# =============================================================================

from random import choice
from .rbd_funcoes import move_to_goal, goal  # goal usado via "global goal" em direciona()


# Cômodo onde o robô está no momento; atualizado em corre_pontos_destino()
Comodo_Atual = 1


# =============================================================================
class CASA:
# =============================================================================
    def __init__(self, comodos, posicoes_destino, rotas, rotas_centrais, pontos_troca):
        self.cm = comodos
        self.pd = posicoes_destino
        self.rt = rotas
        self.rc = rotas_centrais
        self.pt = pontos_troca


# =============================================================================
class TAREFAS:
# =============================================================================
    def __init__(self, existentes, ativas, pesos, incrementos, decrementos, casa):
        self.tarefas         = existentes
        self.tarefas_ativas  = ativas
        self.pesos_tarefas   = pesos
        self.incrementa_peso = incrementos
        self.decrementa_peso = decrementos
        self.cs = casa
        self.rt = casa.rt
        self.pc = casa.rc
        self.pt = casa.pt
        self.p1 = self.cs.pd[0]
        self.p2 = self.cs.pd[42]

    # -------------------------------------------------------------------------
    def direciona(self, d):
    # -------------------------------------------------------------------------
    # Define orientação final do robô via quaternion no goal do NavigateToPose.
    # Valores calibrados para o mapa da casa (portados do robodog1 sem alteração).
    # ROS2: goal.pose.pose.orientation (era goal.target_pose.pose.orientation)
    # -------------------------------------------------------------------------
        global goal
        goal.pose.pose.orientation.x = 0.0
        goal.pose.pose.orientation.y = 0.0
        goal.pose.pose.orientation.z = -0.000818293461172
        goal.pose.pose.orientation.w =  0.999999665198
        if d == 'S':
            goal.pose.pose.orientation.z = -0.999999258742
            goal.pose.pose.orientation.w =  0.00121758601645
        elif d == 'L':
            goal.pose.pose.orientation.z = -0.699192503488
            goal.pose.pose.orientation.w =  0.714933453593
        elif d == 'O':
            goal.pose.pose.orientation.z =  0.707695904306
            goal.pose.pose.orientation.w =  0.706517166832

    # -------------------------------------------------------------------------
    def vai_para(self, posicao_objetivo):
    # -------------------------------------------------------------------------
        po = posicao_objetivo
        self.direciona(po[2])
        print('vou para:', po[3], 'x=', po[0], 'y=', po[1])
        return move_to_goal(po[0], po[1])

    # -------------------------------------------------------------------------
    def tarefa(self, t):
    # -------------------------------------------------------------------------
        print('=' * 60)
        print('vou fazer a tarefa', t)
        if 0 <= t <= 18:
            self.corre_comodos([t])
        print('terminei tarefa', t)
        print('=' * 60)
        # decrementa no estado interno da instância (bug corrigido do robodog1)
        itc = self.tarefas_ativas.index(t)
        self.pesos_tarefas[itc] = self.decrementa_peso[itc]

    # -------------------------------------------------------------------------
    def corre_pontos_destino(self, rota_de_pontos, numero_comodo_destino):
    # -------------------------------------------------------------------------
        global Comodo_Atual
        PD = self.cs.pd
        r = rota_de_pontos
        print('rota:', r[0], '— total de pontos:', len(r) - 1)
        p1_inicial = self.p1
        i = 1
        while i <= len(r) - 1:
            pdi = int(r[i])
            ponto = [PD[pdi][0], PD[pdi][1], PD[pdi][2], PD[pdi][3]]
            self.p1 = ponto
            if self.vai_para(ponto):
                Comodo_Atual = numero_comodo_destino
            i += 1
        self.p1 = p1_inicial

    # -------------------------------------------------------------------------
    def corre_comodos(self, lista_de_comodos):
    # -------------------------------------------------------------------------
        global Comodo_Atual
        CM = self.cs.cm
        for comodo_destino in lista_de_comodos:
            print('vou para o cômodo:', CM[comodo_destino][0])
            self.procura_centro_de_partida(comodo_destino)
            rota = CM[comodo_destino][1]
            self.corre_pontos_destino(rota, comodo_destino)

    # -------------------------------------------------------------------------
    def procura_centro_de_partida(self, comodo_destino):
    # -------------------------------------------------------------------------
        global Comodo_Atual
        PC  = self.pc
        PD  = self.cs.pd
        CM  = self.cs.cm
        PT  = self.pt

        pca = CM[Comodo_Atual][7]
        pcd = CM[comodo_destino][7]
        print('centro atual:', pca, '— centro destino:', pcd)

        if pca == pcd:
            print('destino próximo — indo ao ponto central')
            self.vai_para(PD[pca])
            return

        indices_encontrados = []
        for i in range(len(PC)):
            pca_loc = pct_loc = pcd_loc = False
            pca_i = pca_ic = pct_i = pct_ic = pcd_i = pcd_ic = -1
            for ic in range(len(PC[i])):
                if PC[i][ic] == pca:
                    pca_loc = True; pca_i = i; pca_ic = ic
                if PC[i][ic] == PT[0]:
                    pct_loc = True; pct_i = i; pct_ic = ic
                if PC[i][ic] == pcd:
                    pcd_loc = True; pcd_i = i; pcd_ic = ic
            indices_encontrados.append([
                [pca_loc, pca_i, pca_ic],
                [pct_loc, pct_i, pct_ic],
                [pcd_loc, pcd_i, pcd_ic]
            ])

        lista_pcs = []
        lista_pat = []
        lista_pdt = []
        for i, idx in enumerate(indices_encontrados):
            ipca, ipct, ipcd = idx
            if ipca[0] and ipcd[0]:
                if ipca[2] < ipcd[2]:
                    lista_pcs = PC[i][ipca[2]:ipcd[2]+1]
                else:
                    lista_pcs = PC[i][ipcd[2]:ipca[2]+1]
            else:
                if ipca[0] and not ipcd[0]:
                    if ipca[2] < ipct[2]:
                        lista_pat = PC[i][ipca[2]:ipct[2]+1]
                    else:
                        lista_pat = PC[i][ipct[2]:ipca[2]+1]
                if not ipca[0] and ipcd[0]:
                    if ipcd[2] > ipct[2]:
                        lista_pdt = PC[i][ipct[2]:ipcd[2]+1]
                    else:
                        lista_pdt = PC[i][ipcd[2]:ipct[2]+1]

        if not lista_pcs and lista_pat and lista_pdt:
            if lista_pat.index(PT[0]) == 0:
                lista_pat.reverse()
            if lista_pdt.index(PT[0]) != 0:
                lista_pdt.reverse()
            lista_pcs = lista_pat + lista_pdt

        for ponto_idx in lista_pcs:
            self.vai_para(PD[ponto_idx])

    # -------------------------------------------------------------------------
    def verifica_pesos_negativos(self):
    # -------------------------------------------------------------------------
    # Reinicia o ciclo de pesos quando todos ficam negativos.
    # Ausente no robodog1 (causava IndexError ao esvaziar lista ponderada).
    # -------------------------------------------------------------------------
        nta = len(self.tarefas_ativas)
        total_neg = sum(1 for p in self.pesos_tarefas if p <= 0)
        if total_neg >= nta:
            peso_min = min(self.pesos_tarefas)
            incrementador = peso_min * -1 + 1
            self.pesos_tarefas = [p + incrementador for p in self.pesos_tarefas]

    # -------------------------------------------------------------------------
    def incrementa_pesos(self):
    # -------------------------------------------------------------------------
        for i in range(len(self.tarefas_ativas)):
            self.pesos_tarefas[i] += self.incrementa_peso[i]

    # -------------------------------------------------------------------------
    def prioriza_tarefas(self):
    # -------------------------------------------------------------------------
        self.verifica_pesos_negativos()
        lista = []
        for i, tarefa in enumerate(self.tarefas_ativas):
            peso = self.pesos_tarefas[i]
            if peso > 0:
                lista.extend([tarefa] * peso)
        return lista

    # -------------------------------------------------------------------------
    def escolhe_tarefa_maior_peso(self):
    # -------------------------------------------------------------------------
        peso_max = max(self.pesos_tarefas)
        candidatas = [
            self.tarefas_ativas[i]
            for i, p in enumerate(self.pesos_tarefas)
            if p == peso_max
        ]
        escolhida = choice(candidatas)
        print('tarefa escolhida:', escolhida, '(peso_max=', peso_max, ')')
        return escolhida


# =============================================================================
class ROBO:
# =============================================================================
    def __init__(self, casa, tarefas):
        self.cs  = casa.cm
        self.trf = tarefas

    # -------------------------------------------------------------------------
    def escolhe_tarefas(self):
    # -------------------------------------------------------------------------
    # Loop principal de comportamento autônomo (bloqueante — rodar em thread).
    # -------------------------------------------------------------------------
        while True:
            self.trf.incrementa_pesos()
            tarefa_maior_peso = self.trf.escolhe_tarefa_maior_peso()
            self.trf.tarefa(tarefa_maior_peso)
