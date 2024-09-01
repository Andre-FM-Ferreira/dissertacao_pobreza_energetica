SELECT
    DISTINCT 
    ec.distrito
    , ec.municipio
    , ec.freguesia
    , SUBSTR(cc.codigo_completo, 1, 2) AS nuts_2
    , SUBSTR(cc.codigo_completo, 1, 3) AS nuts_3
    , cc.codigo_completo AS codigo_completo_mun
    , ec.codigo_municipio
    , ec.codigo_freguesia
    , consumo_energetico.consumo AS kwh_med_mes
    , cpe.pontos_cons AS pontos_med_mes
    , ce_cpe.consumo AS kwh_cpe_med_mes
    , pdc.poder_de_compra AS ippcc
    , rbm.rendimento_bruto_mediano AS rend_mediano
    , rmm.renda_media_mensal + 0.0 AS renda_med
    , d.desemprego AS desemprego
    , cg.coeficiente_gini AS gini
    , pre.proporcao_residente_estrangeiro AS resid_estr
    , (ensino_concluido.ciclo_1*4.0 + ensino_concluido.ciclo_2*6 + ensino_concluido.ciclo_3*9 + ensino_concluido.ensino_secundario*12 + ensino_concluido.ensino_pos_secundario*13 + ensino_concluido.curso_tec_superior_profissional*14 + ensino_concluido.bacharelato*15 + ensino_concluido.licenciatura*15 + ensino_concluido.mestrado*17 + ensino_concluido.doutoramento*21) / ensino_concluido.total AS esc_med_anos
    , dp.pop_km2 + 0.0 AS dens_pop
    , (ensino_concluido.total + 0.0) / ad.agg_total AS dim_med_agreg
    , (ad.agg_1_pessoa + 0.0) / ad.agg_total * 100 AS agreg_1
    , (ad.agg_2_pessoa + 0.0) / ad.agg_total * 100 AS agreg_2
    , (ad.agg_3_pessoa + 0.0) / ad.agg_total * 100 AS agreg_3
    , (ad.agg_4_pessoa + 0.0) / ad.agg_total * 100 AS agreg_4
    , (ad.agg_5_pessoa + 0.0) / ad.agg_total * 100 AS agreg_5
    , (ad.agg_6_pessoa + 0.0) / ad.agg_total * 100 AS agreg_6
    , (ad.agg_7_pessoa + 0.0) / ad.agg_total * 100 AS agreg_7
    , (ad.agg_8_pessoa + 0.0) / ad.agg_total * 100 AS agreg_8
    , (ad.agg_9_pessoa_ou_mais + 0.0) / ad.agg_total * 100 AS agreg_9_mais
    , tmedar.temperatura_media AS temp_med
    , tmaxar.temperatura_maxima - tminar.temperatura_minima AS temp_amp
    , dr.nec_ligeira_reparacao / dr.total * 100 AS lig_nec_rep
    , dr.nec_media_reparacao / dr.total * 100 AS med_nec_rep
    , dr.nec_profunda_reparacao / dr.total * 100 AS prof_nec_rep
    , dr.sem_nec_reparacao / dr.total * 100 AS sem_nec_rep
    , dr.sem_nec_reparacao / dr.total * 100 * 0 + dr.nec_ligeira_reparacao / dr.total * 100 * 1 + dr.nec_media_reparacao / dr.total * 100 * 2 + dr.nec_profunda_reparacao / dr.total * 100 * 3 AS indice_nec_rep
    , (aac.agg_cons_x_1919 + 0.0) / aac.agg_total * 100.0 AS aloj_x_1919
    , (aac.agg_cons_1919_1945 + 0.0) / aac.agg_total * 100 AS aloj_1919_1945
    , (aac.agg_cons_1946_1960 + 0.0) / aac.agg_total * 100 AS aloj_1946_1960
    , (aac.agg_cons_1961_1980 + 0.0) / aac.agg_total * 100 AS aloj_1961_1980
    , (aac.agg_cons_1981_1990 + 0.0) / aac.agg_total * 100 AS aloj_1981_1990
    , (aac.agg_cons_1991_2000 + 0.0) / aac.agg_total * 100 AS aloj_1991_2000
    , (aac.agg_cons_2001_2005 + 0.0) / aac.agg_total * 100 AS aloj_2001_2005
    , (aac.agg_cons_2006_2010 + 0.0) / aac.agg_total * 100 AS aloj_2006_2010
    , (aac.agg_cons_2011_2015 + 0.0) / aac.agg_total * 100 AS aloj_2011_2015
    , (aac.agg_cons_2016_2021 + 0.0) / aac.agg_total * 100 AS aloj_2016_2021
    , (aac.agg_cons_x_1919*104 + 0.0 + aac.agg_cons_1919_1945*78 + aac.agg_cons_1946_1960*63 + aac.agg_cons_1961_1980*43 + aac.agg_cons_1981_1990*33 + aac.agg_cons_1991_2000*23 + aac.agg_cons_2001_2005*18 + aac.agg_cons_2006_2010*13 + aac.agg_cons_2011_2015*8 + aac.agg_cons_2016_2021*2) / aac.agg_total AS idade_med_aloj
    , (aas.agg_sobrelotado + 0.0) / aac.agg_total * 100 AS sobrelot
    , (apo.aloj_prop_sem_encargos + 0.0) / ad.agg_total * 100 AS propriet_s_enc
    , (apo.aloj_prop_com_encargos + 0.0) / ad.agg_total * 100 AS propriet_c_enc
    , (ad.agg_total - apo.aloj_prop_total + 0.0) / ad.agg_total * 100 AS nao_propriet
    , (apo.aloj_prop_sem_encargos + 0.0) / ad.agg_total * 100 * 0 + (apo.aloj_prop_com_encargos + 0.0) / ad.agg_total * 100 * 1 + (ad.agg_total - apo.aloj_prop_total + 0.0) / ad.agg_total * 100 * 1 AS indice_enc_aloj
    , pv.dummy_direita AS direita
    , pv.dummy_esquerda AS esquerda
    , pv.maiorias_absolutas AS m_absoluta
FROM
    energia_consumo_2023 ec
-- Somar os consumos médios mensais de cada freguesia
INNER JOIN (
        SELECT
            ec2.codigo_freguesia AS codigo_freguesia
            , COUNT(ec2.codigo_freguesia)
            , sum(ec2.energia_ativa / ecpe2.contratos_ativos) / COUNT(ec2.codigo_freguesia) AS consumo
        FROM
            energia_consumo_2023 ec2
        INNER JOIN energia_cpe_2023 ecpe2
            ON
                ec2.codigo_freguesia = ecpe2.codigo_freguesia
                AND ec2.mes = ecpe2.mes
        WHERE
            ec2.voltagem = 'Baixa Tensão'
            AND ecpe2.tipo_consumo = 'Doméstico'
            -- Existe voltagem de Baixa Tensão Normal e Especial
            AND ecpe2.voltagem = 'Baixa Tensão Normal'
        GROUP BY
            ec2.codigo_freguesia
    ) ce_cpe
    ON 
    ce_cpe.codigo_freguesia = ec.codigo_freguesia
INNER JOIN (
        SELECT
            ec2.codigo_freguesia AS codigo_freguesia
            , COUNT(ec2.codigo_freguesia)
            , sum(ec2.energia_ativa) / COUNT(ec2.codigo_freguesia) AS consumo
        FROM
            energia_consumo_2023 ec2
        WHERE
            ec2.voltagem = 'Baixa Tensão'
        GROUP BY
            ec2.codigo_freguesia
    ) consumo_energetico
    ON 
    consumo_energetico.codigo_freguesia = ec.codigo_freguesia
INNER JOIN (
        SELECT
            ec2.codigo_freguesia AS codigo_freguesia
            , COUNT(ec2.codigo_freguesia)
            , sum(ecpe2.contratos_ativos) / COUNT(ec2.codigo_freguesia) AS pontos_cons
        FROM
            energia_consumo_2023 ec2
        INNER JOIN energia_cpe_2023 ecpe2
            ON
                ec2.codigo_freguesia = ecpe2.codigo_freguesia
                AND ec2.mes = ecpe2.mes
        WHERE
            ec2.voltagem = 'Baixa Tensão'
            AND ecpe2.tipo_consumo = 'Doméstico'
            -- Existe voltagem de Baixa Tensão Normal e Especial
            AND ecpe2.voltagem = 'Baixa Tensão Normal'
        GROUP BY
            ec2.codigo_freguesia
    ) cpe
    ON 
    cpe.codigo_freguesia = ec.codigo_freguesia
INNER JOIN codigos_completos cc 
    ON
    SUBSTR(cc.codigo_completo, -4) = ec.codigo_municipio
INNER JOIN desemprego_2021 d 
    ON
    d.codigo = ec.codigo_municipio
INNER JOIN poder_de_compra_2021 pdc
    ON
    SUBSTR(pdc.codigo, -4) = ec.codigo_municipio
INNER JOIN dimensao_reparacao_2021 dr
    ON
    dr.codigo = ec.codigo_municipio
INNER JOIN coeficiente_gini_2021 cg
    ON
    SUBSTR(cg.codigo, -4) = ec.codigo_municipio
INNER JOIN proporcao_residente_estrangeiro_2021 pre 
    ON
    pre.codigo = ec.codigo_municipio
INNER JOIN temperatura_media_ar_2020 tmedar  
    ON
    SUBSTR(tmedar.codigo, -4) = ec.codigo_municipio
INNER JOIN temperatura_maxima_ar_2020 tmaxar
    ON
    SUBSTR(tmaxar.codigo, -4) = ec.codigo_municipio
INNER JOIN temperatura_minima_ar_2020 tminar
    ON
    SUBSTR(tminar.codigo, -4) = ec.codigo_municipio
INNER JOIN rendimento_bruto_mediano_2021 rbm
    ON
    SUBSTR(rbm.codigo, -4) = ec.codigo_municipio
INNER JOIN agregados_alojamentos_construcao_2021 aac
    ON
    aac.codigo = ec.codigo_municipio
INNER JOIN agregados_alojamentos_sobrelotados_2021 aas 
    ON
    aas.codigo = ec.codigo_municipio
INNER JOIN agregados_dimensao_2021 ad 
    ON  
    ad.codigo = ec.codigo_municipio
INNER JOIN alojamentos_propriedade_ocupante_2021 apo 
    ON
    apo.codigo = ec.codigo_municipio
INNER JOIN densidade_populacional_2021 dp
    ON
    dp.codigo = ec.codigo_municipio
INNER JOIN renda_media_mensal_2021 rmm
    ON
    rmm.codigo = ec.codigo_municipio
INNER JOIN ensino_concluido_2021 ensino_concluido
    ON
    ensino_concluido.codigo = ec.codigo_municipio
INNER JOIN partido_vencedor_2021 pv 
    ON
    pv.codigo = ec.codigo_municipio
WHERE
    ec.voltagem = 'Baixa Tensão'
    ;




