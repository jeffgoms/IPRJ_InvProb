#!/usr/bin/env python3


Inicializacao da funcao
Ler Vetores: K_exp, V_exp, S_exp
Iniciar o prob de otimisacao
Loop
   Gerar populacao K_i
   Rodar Fluidity --> Output: V_i e S_i
   Gerar Funcao Objetivo
   Criterio de Parada alcancaddo
     Sim --> Armazena K_i, V_i e S_i
     Nao --> Gera novos K_i e retorna o Loop
