#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sept 21 05:32:11 2022

@author: Josiele, Matheus and Jeff
"""

import sys
import os, math
import numpy as np
import ExtractFields as EF
import TestMat as TM
import shutil
import fileinput

""" ============================================================
                       Funcao CALCNORMROW
    ============================================================ """
def CalcNormRow(CC):
    """ This function calculates the norm of each row of the matrix. """
    norm = np.zeros(len(CC))
    for irow in range(len(CC)):
        nm = 0.
        for icol in range(len(CC[0])):
            nm = nm + CC[irow][icol]**2
        norm[irow] = math.sqrt(nm)
    return norm

""" Functions to replace lines within a file """
def ReplaceFloatString(K_Float):
    """ This function replaces an array by an string of the same array """
    n = len(K_Float)
    K_String = '['
    for i in range(n):
        if i == 0:
            K_String = K_String + str(round(K_Float[i], 18)) 
        else:
            K_String = K_String + ', ' + str(round(K_Float[i], 18)) 
    K_String = K_String + ']'
    return K_String

def ReplaceString(filename, K):
    OldString = 'K = np.zeros(n); K = '
    NewString = ReplaceFloatString(K)
    for line in fileinput.input([filename], inplace=True):
        if line.strip().startswith('K = '):
            NewString = '    K = np.zeros(n); K = ' + NewString + '\n'
            line = NewString
        sys.stdout.write(line)

    fileinput.close()

    return

""" ============================================================
                       Funcao FOPT
    ============================================================ """
def fobj( ValuesPermK,  Dados_Exp):
    """        Funcao objetivo que sera otimisada        """

    """ Hard-coding to ensure that ValuesPermK is not equal to zero. For the time being 
          let's consider teh same 'bounds' values as in the 'OptimisationCall' function """
    n = len(ValuesPermK);
    for i in range(n):
        if ValuesPermK[i] < TM.MinVal:
            ValuesPermK[i] = TM.MinVal
        elif ValuesPermK[i] > TM.MaxVal:
            ValuesPermK[i] = TM.MaxVal
            
    """ Escrevendo os valores de permeabilidade no arquivo texto 'outdata.txt'
         que eh copiado (apenas por seguranca) para o arquivo 'Kdata.txt'. """
    filename = 'PermFcn.py';
    ReplaceString(filename, ValuesPermK)
          
    """ Chamando a funcao 'LinkFldty'. Esta funcao retorna as seguintes variaveis
          na regiao de contorno de interesse (producao):
            - Coord: numpy 2d array contendo coordenadas (X,Y,Z);
            - Sat: numpy array contendo valores de saturacao nas coordenadas 'Coord';
            - Vel: numpy 2d array contendo components (X,Y,Z) da velocidade de 
               Darcy nas coordenadas 'Coord'.
          """          
    Coord, Sat, Vel = EF.LinkFldty_OptFcn()
    Vvr = CalcNormRow(Vel) # calculando (magnitude) da velocidade

    """ Calculando a soma dos residuos quadraticos ponderados pelo dado experimental  """
    Fobj = 0
    for j in range(len(Vvr)):
        Fobj = Fobj + ((Vvr[j] - Dados_Exp[j])**2)/(Dados_Exp[j]**2)

    return Fobj

""" ====================================================================================
                            Funcao ERRO_PARAMETROS
      Funcao que calcula a tolerancia erro entre os parametros a serem estimados. Essa 
        funcao retorna '0' caso todas as condicoes da tolerancia do erro sejam satisfeitas 
        e retorna '1' caso alguma dessas condicoes ainda nao tenham sido satisfeitas.
          - ValuesPermK -> Vetor contendo as permeabilidades;
          - tolerancia  -> Vetor que contem as tolerancias desejadas para o erro relativo
                           a cada parametro.
      NOTA: Quando for generalizar para mais parametros esse vetor de valores exatos
                        [K1_exato, K2_exato, K3_exato, K4_exato] 
            (valores usados como referencia para calcular os dados experimentais) devera 
            ser passado como parametro da funcao ou devera ser lido de um arquivo 
            externo. 
    ==================================================================================== """
def erro_parametros(ValuesPermK, ValuesPermK_Old, tolerancia):
        
    dim = len(ValuesPermK); erro = np.zeros(dim); indicador = np.zeros(dim, dtype=int)
    
    for i in range(dim):
        erro[i] = np.fabs(ValuesPermK_Old[i] - ValuesPermK[i])
        if (erro[i] < tolerancia[i]):
          indicador[i] = 1
        else:
          indicador[i] = 0
    
    p = np.prod(indicador)
    
    return p, erro


""" ====================================================================================
                            Funcao DE (Differential Evolution)
    ==================================================================================== """
def de_alg(bounds, mut, crossp, popsize, its, Dados_Exp):
    """
       1. Dados_Exp -> Estes sao os dados experimentais que serao utilizados na funcao objetivo
       2. fobj      -> Essa é a função Objetivo ==> fobj(vet_Per, Dados_Exp)
       3. bounds    -> Intervalo de busca de cada parametro
       4. mut       -> Fator de mutação
       5. crossp    -> Fator de cruzamento
       6. popsize   -> Tamanho da população
       7. its       -> Numero de gerações
    """
    
    dimensions = len(bounds)                                                     # Quantidade de parametros a serem estimados (a principio serao 4 parametros)
    pop = np.random.rand(popsize, dimensions)                                    # Vetor da ordem de popsize(linhas) por dimensão do problema(colunas)
    min_b, max_b = np.asarray(bounds).T                                          # Decomposição do vetor(bounds) contendo o limite inferior e superior do espaço de busca de cada parametro
    diff = np.fabs(min_b - max_b)                                                # Comprimento dos intervalos de busca para cada parametro
    pop_denorm = min_b + pop * diff                                              # População inicial
    print('pop_denorm:', len(pop_denorm), pop_denorm)
    fitness = np.asarray([fobj(ind, Dados_Exp) for ind in pop_denorm])           # Valor da função objetivo pra cada elemento da população
    best_idx = np.argmin(fitness)                                                # Indice do menor(melhor) valor da função objetivo 
    best = pop_denorm[best_idx]                                                  # Menor(melhor) valor da função objetivo                                                 
    inter_ = 0
    Tol = [1.e-8, 1.e-8, 1.e-8, 1.e-8]                                           # Vetor contendo as respectivas tolerancias para os erros de cada parametro de interesse, podendo ser diferentes entre si

    """ Inicializacao do problema gerando dois arrays """
    K = np.ones(dimensions)
    Old = [np.random.uniform(TM.MinVal,TM.MaxVal) for _ in range(dimensions)]
   
    [p, E] = erro_parametros(K, Old, Tol)
    inter_fix = its                                                               # Numero de interações maxima
    L_inf = TM.MinVal ; L_sup = TM.MaxVal                                         # Limites inferior/superior do intervalo 
    L_sup = TM.MaxVal                                                             #     de busca dos parâmetros de interesse
  
    f = np.zeros(popsize); Erro = []
    cont = 0                                                                     # Contador de avaliacoes da funcao objetivo
    print('======> AVALIACOES init:', inter_, '<======')
    while (  (p == 0) and (inter_ < inter_fix) ):                                # Percorre gerações                                                     
         Old = best                                                             # Guarda o melhor valor da iteracao anterior
         print('======> AVALIACOES:', inter_, '<======')
         for j in range(popsize):                                               # Percorre população
             idxs = [idx for idx in range(popsize) if idx != j]
             a, b, c = pop[np.random.choice(idxs, 3, replace = False)]
             mutant = np.clip(a + mut * (b - c), L_inf, L_sup)
             cross_points = np.random.rand(dimensions) < crossp
             if not np.any(cross_points):
                  cross_points[np.random.randint(0, dimensions)] = True
             trial = np.where(cross_points, mutant, pop[j])
             trial_denorm = min_b + trial * diff
             f[j] = fobj(trial_denorm, Dados_Exp)                              # Calling FOBJ
             cont = cont + 1
             if f[j] < fitness[j]:
                 fitness[j] = f[j]
                 pop[j] = trial[j]                                             # @Josiele ... could you check here  
                 if f[j] < fitness[best_idx]:
                      best_idx = j
                      best = trial_denorm
                      K = best
   
         [p, E] = erro_parametros(K, Old, Tol)
         Erro.append(E) 
         inter_ = inter_ + 1

    # plotar erro, valor da Fobj e numero de avaliacoes
    #yield best, fitness[best_idx], cont, f
    print('best:', best)
    print('best_idx, fitness:', best_idx,  fitness[best_idx])
    print('cont:', cont)
    print('f:', f)
    return Erro


""" ============================================================
                       Funcao OPTMISATIONCALL
    ============================================================ """
def OptimisationCall():
    # Loading global variables
    TM.GlobalVar()

    """ Obter os valores experimentais de um arquivo de dados"""
    CoordFM, SatFM, VelFM = EF.ReadFineResolMeshFile()
    #print('Coord:', CoordFM); print('Velocity:', VelFM)
    Dados_Exp = CalcNormRow(VelFM)

    """  Definindo os intervalos de busca dos parametros de interesse   """
    #dim = len(ValuesPermK)
    dim = TM.nd
    L_inf = TM.MinVal; L_sup = TM.MaxVal
    bounds= [(L_inf, L_sup)] * 4   # bounds tem dimensao 4linhas x 2 colunas
    

    if TM.AlgOptimisation == 'DE' or TM.AlgOptimisation == 'de':
        # Definindo os parametros do algoritmo
        mut = TM.FMutacao; crossp = TM.FCruzamento; popsize = TM.DimPopulacao; its = TM.NGeracoes
        # Chamando a funcao 'Differential Evolution'
        #de(fobj, bounds, mut, crossp, popsize, its, Dados_Exp)
        print('just b4')
        Er = de_alg(bounds, mut, crossp, popsize, its, Dados_Exp)
        print('just after', Er)
    else:
        sys.exit('Algoritmo de otimisacao nao encontrado')
