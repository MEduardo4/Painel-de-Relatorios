-- Consulta de Estoque em Tempo Real
SELECT M0_FILIAL AS Filial,
    B2_COD AS CodigoProduto,
    B1_DESC AS NomeProduto,
    B1_UM AS UM,
    CASE
        WHEN B1_MSBLQL = 1 THEN '1 - Sim'
        WHEN B1_MSBLQL = 2 THEN '2 - Não'
        ELSE ' '
    END AS Bloq,
    CONCAT(B2_LOCAL, '-', NNR_DESCRI) AS DescArmazem,
    B2_LOCAL AS Armazem,
    B1_TIPO AS Tipo,
    CONCAT(B1_GRUPO, '-', BM_DESC) AS DescGrupo,
    B1_GRUPO AS Grupo,
    CONCAT(B1_TIPO, '-', X5_DESCRI) AS DescTipo,
    B2_CM1 AS ValorUni,
    B2_USAI AS DtUltimaSaida,
    B2_QATU AS SaldoEmEstoque,
    B2_QEMP + B2_QEMPSA + B2_RESERVA AS EmpenhoReqPvReserva,
    CASE
        WHEN B2_QEMP + B2_QEMPSA + B2_RESERVA > 0 THEN B2_QATU - (B2_QEMP + B2_QEMPSA + B2_RESERVA)
        ELSE B2_QATU + (B2_QEMP + B2_QEMPSA + B2_RESERVA)
    END AS EstoqueDisponivel,
    B2_VATU1 AS ValorEmEstoque,
    B2_CM1 * B2_QEMP AS ValorEmpenhado,
    B1_EMIN AS EstoqueMinimo
FROM SB2010
    LEFT JOIN SB1010 ON B2_COD = B1_COD
    AND SB1010.D_E_L_E_T_ <> '*'
    AND SUBSTRING(B2_FILIAL, 1, 2) = B1_FILIAL
    LEFT JOIN SBM010 ON B1_GRUPO = BM_GRUPO
    AND SBM010.D_E_L_E_T_ <> '*'
    AND BM_FILIAL = ' '
    LEFT JOIN SX5010 ON X5_TABELA + X5_CHAVE = '02' + B1_TIPO
    AND B2_FILIAL = X5_FILIAL
    AND SX5010.D_E_L_E_T_ <> '*'
    LEFT JOIN NNR010 ON NNR_CODIGO = B2_LOCAL
    AND NNR010.D_E_L_E_T_ <> '*'
    AND B2_FILIAL = NNR_FILIAL
    LEFT JOIN SYS_COMPANY ON B2_FILIAL = M0_CODFIL
    AND SYS_COMPANY.D_E_L_E_T_ = ''
    AND M0_NOME = 'BRG Geradores'
WHERE SB2010.D_E_L_E_T_ <> '*'
    AND SB1010.D_E_L_E_T_ <> '*'
    AND B2_FILIAL IN ('0101', '0501', '0502', '0503')
ORDER BY B2_COD