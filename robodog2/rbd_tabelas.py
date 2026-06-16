#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# =============================================================================
# rbd_tabelas.py — Dados estáticos do mapa e do sistema de tarefas do robodog2
#
# Arquivo sem dependências ROS — portado do robodog1 sem alterações nos dados.
# =============================================================================


# =============================================================================
# Sistema de tarefas ponderadas
#
# Tarefas[0] = "Geral" (percurso completo) — definido mas não ativo por padrão;
# tarefa 0 percorre todos os cômodos em sequência e é muito longa para uso normal.
# =============================================================================

Tarefas         = [  0    ,  1  ,   2   ,   3 ,  4 ,   5  ,   6 ,  7 ,   8 ,  9 , 10 ,  11 , 12 ,  13 ,  14 , 15 , 16 ,  17 ,  18 ]
Tarefas_Ativas  = [          1  ,   2   ,   3 ,  4 ,   5  ,   6 ,  7 ,   8 ,  9 , 10 ,  11 , 12 ,  13 ,  14 , 15 , 16 ,  17 ,  18 ]
Pesos_Tarefas   = [         10  ,   2   ,   3 ,  40,  50  ,   6 , 7  ,   8 ,  9 , 10 ,  11 , 12 ,  13 ,  14 , 15 , 16 , 170 , 180 ]
Incrementa_Peso = [          1  ,   1   ,   2 ,  1 ,   1  ,   1 ,  1 ,   1 ,  3 ,  1 ,   1 ,  1 ,   1 ,   1 ,  1 ,  1 ,   1 ,   1 ]
Decrementa_Peso = [        -20  ,  -4   ,  -6 , -80,-100  , -12 ,-14 , -16 ,-18 ,-20 , -22 ,-24 , -26 , -28 ,-30 ,-32 ,-340 ,-360 ]


# =============================================================================
# RT — Rotas de pontos de destino por cômodo
# RT[n][0] = nome do cômodo; RT[n][1:] = índices de PD do percurso
# =============================================================================
RT = [
        ['Geral'   , 0 , 9 , 12 , 17 , 19 , 23 , 28 , 32 , 36 , 42 , 51 , 53 , 57 , 65 , 67 , 70 , 71 ] ,
        ['Estar'   , 0 , 2 , 3 , 4 , 1 , 5 , 6 , 7 ] ,
        ['Var.L'   , 8 , 9 ] ,
        ['Esc.R'   , 13 , 12 , 11 ] ,
        ['Ban.R'   , 14 ] ,
        ['Ban.S'   , 16 , 17  ] ,
        ['Esc.A'   , 19 , 20  ] ,
        ['Qt.D'    , 22 , 23 , 24 , 25 ] ,
        ['Qt.C'    , 26 , 29 ] ,
        ['Ban.C'   , 32 ] ,
        ['Corredor', 33 , 36 , 35  ] ,
        ['Sala'    , 41 , 42 , 43 , 44 , 46 , 47 , 48 ] ,
        ['Var.F'   , 50 , 52 , 51  ] ,
        ['Lav.'    , 53  ] ,
        ['Coz.'    , 55 , 58 , 59 , 60 , 56  ] ,
        ['Area'    , 65, 66 , 64  ] ,
        ['Dis.'    , 67  ] ,
        ['Qt.M'    , 68 ,  70 , 69  ] ,
        ['Ban.M'   , 71  ]
     ]


# =============================================================================
# CM — Propriedades dos cômodos
# CM[n] = [ nome, rota, x, y, l, a, A, ponto_central ]
#   x, y, l, a, A — dimensões físicas; todos 0.0 (não usados no robodog2)
#   ponto_central  — índice em PD usado por procura_centro_de_partida()
# =============================================================================
CM = [
  [ 'Geral        '        , RT[ 0] , 0.0 , 0.0 , 0.0 , 0.0 , 0.0 , 72 ] ,
  [ 'Sala de Estar'        , RT[ 1] , 0.0 , 0.0 , 0.0 , 0.0 , 0.0 , 72 ] ,
  [ 'Varanda     L'        , RT[ 2] , 0.0 , 0.0 , 0.0 , 0.0 , 0.0 , 72 ] ,
  [ 'Escritorio  R'        , RT[ 3] , 0.0 , 0.0 , 0.0 , 0.0 , 0.0 , 72 ] ,
  [ 'Banheiro    R'        , RT[ 4] , 0.0 , 0.0 , 0.0 , 0.0 , 0.0 , 13 ] ,
  [ 'Banheiro    S'        , RT[ 5] , 0.0 , 0.0 , 0.0 , 0.0 , 0.0 , 72 ] ,
  [ 'Escritorio  A'        , RT[ 6] , 0.0 , 0.0 , 0.0 , 0.0 , 0.0 , 72 ] ,
  [ 'Quarto      D'        , RT[ 7] , 0.0 , 0.0 , 0.0 , 0.0 , 0.0 , 72 ] ,
  [ 'Quarto      C'        , RT[ 8] , 0.0 , 0.0 , 0.0 , 0.0 , 0.0 , 72 ] ,
  [ 'Banheiro    C'        , RT[ 9] , 0.0 , 0.0 , 0.0 , 0.0 , 0.0 , 30 ] ,
  [ 'Corredor     '        , RT[10] , 0.0 , 0.0 , 0.0 , 0.0 , 0.0 , 34 ] ,
  [ 'Sala         '        , RT[11] , 0.0 , 0.0 , 0.0 , 0.0 , 0.0 , 49 ] ,
  [ 'Varanda     F'        , RT[12] , 0.0 , 0.0 , 0.0 , 0.0 , 0.0 , 49 ] ,
  [ 'Lavabo       '        , RT[13] , 0.0 , 0.0 , 0.0 , 0.0 , 0.0 , 49 ] ,
  [ 'Cozinha      '        , RT[14] , 0.0 , 0.0 , 0.0 , 0.0 , 0.0 , 34 ] ,
  [ 'Area         '        , RT[15] , 0.0 , 0.0 , 0.0 , 0.0 , 0.0 , 63 ] ,
  [ 'Dispensa     '        , RT[16] , 0.0 , 0.0 , 0.0 , 0.0 , 0.0 , 63 ] ,
  [ 'Quarto      M'        , RT[17] , 0.0 , 0.0 , 0.0 , 0.0 , 0.0 , 63 ] ,
  [ 'Banheiro    M'        , RT[18] , 0.0 , 0.0 , 0.0 , 0.0 , 0.0 , 70 ]
]


# =============================================================================
# PT — Pontos de Troca entre rotas de pontos centrais
# PT[0] = 34 = "Corredor - porta 2 C" — junção entre as rotas de PC
# =============================================================================
PT = [ 34 ]


# =============================================================================
# PC — Rotas de pontos centrais
# =============================================================================
PC = [
       [ 72 , 34 , 59 , 56 , 63 , 64 ] ,
       [ 72 , 34 , 59 , 56 , 63 , 64 , 70] ,
  [ 30 , 72 , 34 , 59 , 56 , 63 , 64 ] ,
  [ 13 , 72 , 34 , 59 , 56 , 63 , 64 ] ,
  [ 34 , 49 ]
]


# =============================================================================
# PD — Pontos de Destino (74 pontos, índices 0–73)
# Formato: [ x, y, orientação, nome ]
# Orientação: 'N' 'S' 'L' 'O' (calibradas para o mapa da casa)
# =============================================================================
PD = [
  [-3.0 , -2.0 , 'N' , 'Sala de Estar  - base'       ] , # 0
  [-0.5 , -1.5 , 'N' , 'Sala de Estar  - entrada C'  ] , # 1
  [-2.6 , -1.5 , 'O' , 'Sala de Estar  - porta 1 R'  ] , # 2
  [-1.2 , -1.5 , 'O' , 'Sala de Estar  - porta 2 B'  ] , # 3
  [-0.5 , -1.5 , 'O' , 'Sala de Estar  - porta 3 E'  ] , # 4
  [-1.0 , -3.2 , 'L' , 'Sala de Estar  - porta 4 Q'  ] , # 5
  [-2.9 , -3.9 , 'L' , 'Sala de Estar  - porta 5 S'  ] , # 6
  [-3.5 , -3.7 , 'S' , 'Sala de Estar  - porta 6 V'  ] , # 7

  [-6.5 , -3.6 , 'L' , 'Varanda L      - porta'      ] , # 8
  [-6.5 , -2.0 , 'S' , 'Varanda L      - base'       ] , # 9

  [-2.7 , -0.5 , 'O' , 'Escritorio R   - porta 1 S'  ] , # 10
  [-4.7 ,  2.5 , 'O' , 'Escritorio R   - porta 2 B'  ] , # 11
  [-3.3 ,  2.5 , 'N' , 'Escritorio R   - base'       ] , # 12
  [-4.7 ,  0.0 , 'O' , 'Escritorio R   - mesa'       ] , # 13

  [-4.7 , 3.6  , 'O' , 'Banheiro R    - porta'       ] , # 14
  [-5.2 , 3.75 , 'N' , 'Banheiro R    - base'        ] , # 15

  [ -1.5 , -0.4 , 'O' , 'Banheiro S    - porta'      ] , # 16
  [ -1.4 ,  1.3 , 'N' , 'Banheiro S    - base'       ] , # 17

  [ -0.5 , -0.7 , 'O' , 'Escritorio A  - porta'      ] , # 18
  [ -0.0 ,  1.7 , 'N' , 'Escritorio A  - base'       ] , # 19
  [  0.3 ,  2.0 , 'L' , 'Escritorio A  - janela'     ] , # 20
  [  1.1 ,  0.3 , 'S' , 'Escritorio A  - mesa'       ] , # 21

  [ -1.0 , -4.5 , 'L' , 'Quarto D      - porta'      ] , # 22
  [  0.5 , -6.3 , 'N' , 'Quarto D      - base'       ] , # 23
  [  0.0 , -8.0 , 'N' , 'Quarto D      - janela'     ] , # 24
  [ -1.0 , -8.0 , 'S' , 'Quarto D      - mesa'       ] , # 25

  [ -3.0 , -5.0 , 'L' , 'Quarto C      - porta 1 S'  ] , # 26
  [ -4.5 , -7.8 , 'L' , 'Quarto C      - porta 2 B'  ] , # 27
  [ -3.5 , -5.0 , 'N' , 'Quarto C      - base'       ] , # 28
  [ -3.0 , -7.3 , 'S' , 'Quarto C      - janela'     ] , # 29
  [ -4.5 , -7.3 , 'N' , 'Quarto C      - comoda'     ] , # 30

  [ -4.5 ,  -9.1 , 'L' , 'Banheiro C    - porta'     ] , # 31
  [ -5.5 ,  -9.1 , 'S' , 'Banheiro C    - base'      ] , # 32

  [  0.3 ,  -1.5 , 'S' , 'Corredor     - porta 1 S'  ] , # 33
  [  3.0 ,  -1.5 , 'N' , 'Corredor     - porta 2 C'  ] , # 34
  [  2.0 ,  -1.5 , 'L' , 'Corredor     - porta 3 T'  ] , # 35
  [  1.0 ,  -1.5 , 'S' , 'Corredor     - base'       ] , # 36

  [  6.3 ,  -1.8 , 'N' , 'Sala         - porta 1 E'  ] , # 37
  [  6.3 ,  -1.5 , 'S' , 'Sala         - porta 2 C'  ] , # 38
  [  6.3 ,  -4.3 , 'N' , 'Sala         - porta 3 B'  ] , # 39
  [  5.2 ,  -8.2 , 'L' , 'Sala         - porta 4 V'  ] , # 40
  [  2.3 ,  -2.3 , 'L' , 'Sala         - porta 3 Q'  ] , # 41
  [  0.2 ,  -2.5 , 'N' , 'Sala         - base'       ] , # 42
  [  5.0 ,  -2.5 , 'L' , 'Sala         - mesa'       ] , # 43
  [  2.0 ,  -5.0 , 'N' , 'Sala         - TV'         ] , # 44
  [  2.0 ,  -8.0 , 'N' , 'Sala         - janela'     ] , # 45
  [  6.1 ,  -7.0 , 'O' , 'Sala         - apoio'      ] , # 46
  [  6.3 ,  -3.3 , 'O' , 'Sala         - hall'       ] , # 47
  [  2.0 ,  -3.0 , 'L' , 'Sala         - centro mesa'] , # 48
  [  5.0 ,  -6.0 , 'L' , 'Sala         - centro TV'  ] , # 49

  [  5.3 ,  -9.5  , 'L' , 'Varanda F   - porta'      ] , # 50
  [  7.0 ,  -9.5  , 'S' , 'Varanda F   - base'       ] , # 51
  [  3.0 , -10.5  , 'L' , 'Varanda F   - mesa'       ] , # 52

  [  7.5 ,  -4.3 , 'S' , 'Lavabo       - porta'      ] , # 53

  [  5.5 ,  -1.6 , 'S' , 'Cozinha      - porta 1 S'  ] , # 54
  [  2.5 ,  -1.5 , 'N' , 'Cozinha      - porta 2 Q'  ] , # 55
  [  4.7 ,   3.5 , 'O' , 'Cozinha      - porta 3 A'  ] , # 56
  [  2.5 ,  -0.5 , 'N' , 'Cozinha      - base'       ] , # 57
  [  4.5 ,   0.3 , 'S' , 'Cozinha      - mesa'       ] , # 58
  [  3.5 ,   0.5 , 'O' , 'Cozinha      - centro'     ] , # 59
  [  4.0 ,   2.0 , 'O' , 'Cozinha      - geladeira'  ] , # 60

  [  5.0 ,   4.5 , 'N' , 'Area         - porta 1 S'  ] , # 61
  [  4.8 ,   4.3 , 'O' , 'Area         - porta 2 C'  ] , # 62
  [  3.5 ,   4.3 , 'S' , 'Area         - porta 3 D'  ] , # 63
  [  3.5 ,   6.2 , 'S' , 'Area         - porta 1 Q'  ] , # 64
  [  4.5 ,   5.0 , 'N' , 'Area         - base'       ] , # 65
  [  4.5 ,   6.0 , 'O' , 'Area         - meio'       ] , # 66

  [  2.5 ,   4.2 , 'S' , 'Dispensa     - porta'      ] , # 67

  [  2.7 ,   6.1 , 'S' , 'Quarto M     - porta 1 A'  ] , # 68
  [  1.3 ,   5.3 , 'L' , 'Quarto M     - porta 2 B'  ] , # 69
  [  1.2 ,   6.1 , 'L' , 'Quarto M     - base'       ] , # 70

  [ 1.3 ,  4.0 , 'L' , 'Banheiro M     - porta'      ] , # 71

  [-2.0 , -2.5 , 'N' , 'Sala de Estar  - centro'     ] , # 72  ponto central padrão
  [ 4.0 ,  4.2 , 'N' , 'Area           - centro'     ]   # 73
]
