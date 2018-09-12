import os
import pandas as pd
import numpy as np
from unidecode import unidecode
from pymongo import MongoClient
from sqlalchemy import create_engine
import unicodedata as uni
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, jsonify

app = Flask(__name__) # create the application instance :)
app.config.from_object(__name__) # load config from this file , flaskr.py

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'flaskr.db'),
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('dash.html')

@app.route('/download', methods=['GET', 'POST'])
def download():
    return render_template('download.html')

@app.route('/_reqUF')
def reqUF():
    #staticPath = url_for('static', filename='')
    staticPath = r"C:\\Users\\fsiles\\Desktop\\ATLAS\\flaskr\\static"

    conn = create_engine("postgres+psycopg2://postgres:know@2014@10.129.33.217:5432/ATLAS")
    select = request.args.get('a', 0, type=str)
    table = pd.read_sql('SELECT * FROM "Cities" d WHERE d."Estado" = ' + "'{}'".format(select), conn)

    citiesSel = sorted(list(table["Municipio"]))
    return jsonify(siteInformation=citiesSel)


@app.route('/_req')
def req():

    META = [
        98.5,       #3G_ACC_CS
        98.5,       #3G_ACC_PS
        99.0,       #3G_ACC_HSDPA
        99.0,       #3G_ACC_HSUPA
        1.0,        #3G_DROP_CS
        1.5,        #3G_DROP_PS
        3.0,        #3G_MIGRA
        98.5,       #4G_ACC_ERRC
        98.5,       #4G_ACC_ERAB
        01.0,       #4G_DROP_ERAB
        98.0, ]     #4G_HO_INTRA

    staticPath = r"C:\\Users\\fsiles\\Desktop\\ATLAS\\flaskr\\static"

    #   ---  Postgres  ---
    conn = create_engine("postgres+psycopg2://postgres:1611@10.133.106.213:5432/ATLAS")
    table3G = pd.read_sql('SELECT * FROM celulas_umts', conn)
    table4G = pd.read_sql('SELECT * FROM celulas_lte', conn)

    kpis3G = pd.read_sql('SELECT * FROM cidades_umts', conn)
    kpis4G = pd.read_sql('SELECT * FROM cidades_lte', conn)
    
    freqs = [700, 850, 900, 1800, 2100, 2600]
    freqLTE = {
        '700':[0,0],
        '850':[0,0],
        '900':[0,0],
        '1800':[0,0],
        '2100':[0,0],
        '2600':[0,0] }
    freqUMTS = {
        '700':[0,0],
        '850':[0,0],
        '900':[0,0],
        '1800':[0,0],
        '2100':[0,0],
        '2600':[0,0] }
    freqGSM = {
        '700':[0,0],
        '850':[0,0],
        '900':[0,0],
        '1800':[0,0],
        '2100':[0,0],
        '2600':[0,0] }

    city = request.args.get('a', 0, type=str)
    state = request.args.get('b', 0, type=str)
    totalLTECells = 0
    totalUMTSCells = 0
    totalGSMCells = 0
    
    kpis3G = pd.DataFrame(list(kpis3G[kpis3G['Município'] == city][kpis3G['Estado'] == state]))
    kpis4G = pd.DataFrame(list(kpis4G[kpis3G['Município'] == city][kpis4G['Estado'] == state]))
    
    #cityDF = pd.DataFrame(list(table.find({"MUNICIPIO":city, 'UF':state}, {"_id":0, "Regional":1,'UF':1, "FREQUENCIA":1, "SITE":1, "Vendor_x":1, "TECH":1, "Célula":1, 'earfcnDL':1, 'UARFCN':1, 'BCCH':1, "LTE 700 on air":1, 'Prioridade':1, 'Cluster Name':1, 'Cluster Netchart':1})))
    
    cityDF["Site"] = cityDF['Célula'].str[:-1]
    for k in freqs:
        freqLTE[str(k)][0] = cityDF[cityDF.FREQUENCIA == k][cityDF.TECH == "LTE"]['FREQUENCIA'].count()
        totalLTECells += freqLTE[str(k)][0]
        try:
            freqLTE[str(k)][1] = cityDF[cityDF.FREQUENCIA == k][cityDF.TECH == "LTE"]['Vendor_x'].iloc[0]
        except:
            pass
        freqUMTS[str(k)][0] = cityDF[cityDF.FREQUENCIA == k][cityDF.TECH == "UMTS"]['FREQUENCIA'].count()
        totalUMTSCells += freqUMTS[str(k)][0]
        freqGSM[str(k)][0] = cityDF[cityDF.FREQUENCIA == k][cityDF.TECH == "GSM"]['FREQUENCIA'].count()
        totalGSMCells += freqGSM[str(k)][0]
    if totalGSMCells == 0: totalGSMCells = 1
    if totalLTECells == 0: totalLTECells = 1
    if totalUMTSCells == 0: totalUMTSCells = 1

    # ---------------
    # -- Site Info --

    siteInfo = list()
    try:
        siteInfo.append(cityDF.Prioridade.iloc[0])
    except:
        siteInfo.append('0')

    siteInfo.append('Sim' if freqLTE['700'][0] else 'Não')

    try:
        siteInfo.append(cityDF['Cluster Name'].iloc[0])
        siteInfo.append(cityDF['Cluster Netchart'].iloc[0])
    except:
        siteInfo.append('-')
        siteInfo.append('-')

    cells2g = list()
    sites2g = list()
    liBCCH = [[],[],[],[],[],[]]
    cells3g = list()
    sites3g = list()
    liUARFCN = [[],[],[],[],[],[]]
    cells4g = list()
    sites4g = list()
    liearfcnDL = [[],[],[],[],[],[]]
    k = 0
    for i in freqs:
        cells2g.append(str(cityDF[(cityDF.FREQUENCIA == i) & (cityDF.TECH == "GSM")].count().iloc[2]))
        sites2g.append(str(cityDF[(cityDF.FREQUENCIA == i) & (cityDF.TECH == "GSM")].drop_duplicates(["SITE"]).count().iloc[2]))
        try:
            for l in cityDF[(cityDF.FREQUENCIA == i) & (cityDF.TECH == "GSM")]['BCCH']:
                for j in l.split(', '):
                    if (' ' + str(int(j))) not in liBCCH[k]: liBCCH[k].append(' ' + str(int(j)))
        except:
            liBCCH[k].append('')
        try:
            for l in cityDF[(cityDF.FREQUENCIA == i) & (cityDF.TECH == "UMTS")]['UARFCN']:
                if (' ' + str(int(l))) not in liUARFCN[k]: liUARFCN[k].append(' ' + str(int(l)))
        except:
            liBCCH[k].append('')
        try:
            for l in cityDF[(cityDF.FREQUENCIA == i) & (cityDF.TECH == "LTE")]['earfcnDL']:
                if (' ' + str(int(l))) not in liearfcnDL[k]: liearfcnDL[k].append(' ' + str(int(l)))
        except:
            liBCCH[k].append('')
        cells3g.append(str(cityDF[(cityDF.FREQUENCIA == i) & (cityDF.TECH == "UMTS")].count().iloc[2]))
        sites3g.append(str(cityDF[(cityDF.FREQUENCIA == i) & (cityDF.TECH == "UMTS")].drop_duplicates(["SITE"]).count().iloc[2]))
        cells4g.append(str(cityDF[(cityDF.FREQUENCIA == i) & (cityDF.TECH == "LTE")].count().iloc[2]))
        sites4g.append(str(cityDF[(cityDF.FREQUENCIA == i) & (cityDF.TECH == "LTE")].drop_duplicates(["SITE"]).count().iloc[2]))
        liBCCH[k] = sorted(liBCCH[k])
        k+=1
    # ---------------
    # ---- IBGE ----
    ibge = pd.read_csv(staticPath + "\\database\\CidadesDF.csv", encoding="Latin", sep=";")
    ibge.Cidade = ibge.Cidade.apply(lambda x: unidecode(x).upper())
    findC = ibge[(ibge.Cidade == city) & (ibge.Estado == state)]
    # ---------------
    # ---- FLAG? ----
    
    #weekL = pd.DataFrame(list(kpis.find({'Município':'RIO BRANCO', 'Estado':'AC'}, {'_id':0,'3G.acc_cs':1})))
    #weekL = weekL['3G'].iloc[0]
    #weeks = list(weekL['acc_cs'].keys())[-4:]
    

    kpisLTE = [[],[],[],[]]
    kpisUMTS =[[],[],[],[],[],[],[]]
    kpisLTE = [
    [[str(round(float(x)*100, 2))+'%' for x in kpis4G['acc_errc'].values()][-4:], []],
    [[str(round(float(x)*100, 2))+'%' for x in kpis4G['acc_erab'].values()][-4:], []],
    [[str(round(float(x)*100, 2))+'%' for x in kpis4G['drop_erab'].values()][-4:], []],
    [[str(round(float(x)*100, 2))+'%' for x in kpis4G['intra_freq_ho_succ_out'].values()][-4:], []] ]
    kpisUMTS=[
    [[str(round(float(x)*100, 2))+'%' for x in kpis3G['acc_cs'].values()][-4:], []],
    [[str(round(float(x)*100, 2))+'%' for x in kpis3G['acc_ps'].values()][-4:], []],
    [[str(round(float(x)*100, 2))+'%' for x in kpis3G['acc_hsdpa'].values()][-4:], []],
    [[str(round(float(x)*100, 2))+'%' for x in kpis3G['acc_hsupa'].values()][-4:], []],
    [[str(round(float(x)*100, 2))+'%' for x in kpis3G['drop_cs'].values()][-4:], []],
    [[str(round(float(x)*100, 2))+'%' for x in kpis3G['drop_ps'].values()][-4:], []],
    [[str(round(float(x)*100, 7))+'%' for x in kpis3G['migra_irat_cs'].values()][-4:], []] ]
    flagKPI = [0]

    for k in range(0,7):
        for i in kpisUMTS[k][0]:
            if k in [4,5,6]:
                if float(i[:-1]) > META[k]:
                    kpisUMTS[k][1].append(1)
                    flagKPI[0] = 1
                else:
                    kpisUMTS[k][1].append(0)
            else:
                if float(i[:-1]) < META[k]:
                    kpisUMTS[k][1].append(1)
                    flagKPI[0] = 1
                else:
                    kpisUMTS[k][1].append(0)


    for k in range(0,4):
        for i in kpisLTE[k][0]:
            if k == 2:
                if float(i[:-1]) > META[k+7]:
                    kpisLTE[k][1].append(1)
                    flagKPI[0] = 1
                else:
                    kpisLTE[k][1].append(0)
            else:
                if float(i[:-1]) < META[k+7]:
                    kpisLTE[k][1].append(1)
                    flagKPI[0] = 1
                else:
                    kpisLTE[k][1].append(0)
    # ---------------

    return jsonify(
        weeks=["weeks","weeks","weeks","weeks"],
        flagKPI=flagKPI,
        site2gFreqsInfo=[sites2g,cells2g,liBCCH],
        site3gFreqsInfo=[sites3g,cells3g,liUARFCN],
        site4gFreqsInfo=[sites4g,cells4g,liearfcnDL],
        kpisLTE=kpisLTE,
        kpisUMTS=kpisUMTS,
        ibge=[
            str(findC.População.iloc[0]),
            str(findC["Dens.(km²)"].iloc[0]),
            str(int(findC.Área.iloc[0])) + " Km²",
            str(len(cityDF.drop_duplicates(["Site"]))/findC.Área.iloc[0]) ],
        siteInfo=[
            str(int(siteInfo[0])),
            str(siteInfo[1]),
            str(siteInfo[2]),
            str(siteInfo[3]) ],
        freq4g=[
            str(int(freqLTE["700"][0])), 
            str(int(freqLTE["850"][0])), 
            str(int(freqLTE["900"][0])), 
            str(int(freqLTE["1800"][0])), 
            str(int(freqLTE["2100"][0])), 
            str(int(freqLTE["2600"][0])) ], 
        freq3g=[
            str(int(freqUMTS["700"][0])), 
            str(int(freqUMTS["850"][0])), 
            str(int(freqUMTS["900"][0])), 
            str(int(freqUMTS["1800"][0])), 
            str(int(freqUMTS["2100"][0])), 
            str(int(freqUMTS["2600"][0])) ],
        freq2g=[
            str(int(freqGSM["700"][0])), 
            str(int(freqGSM["850"][0])), 
            str(int(freqGSM["900"][0])), 
            str(int(freqGSM["1800"][0])), 
            str(int(freqGSM["2100"][0])), 
            str(int(freqGSM["2600"][0])) ],
        freq4gP=[
            [str(int((freqLTE["700"][0]/totalLTECells)*100)), str(freqLTE["700"][1]).upper()], 
            [str(int((freqLTE["850"][0]/totalLTECells)*100)), str(freqLTE["850"][1]).upper()], 
            [str(int((freqLTE["900"][0]/totalLTECells)*100)), str(freqLTE["900"][1]).upper()], 
            [str(int((freqLTE["1800"][0]/totalLTECells)*100)), str(freqLTE["1800"][1]).upper()], 
            [str(int((freqLTE["2100"][0]/totalLTECells)*100)), str(freqLTE["2100"][1]).upper()], 
            [str(int((freqLTE["2600"][0]/totalLTECells)*100)), str(freqLTE["2600"][1]).upper()] ], 
        freq3gP=[
            [str(int((freqUMTS["700"][0]/totalUMTSCells)*100)),"TIM"], 
            [str(int((freqUMTS["850"][0]/totalUMTSCells)*100)), "TIM"], 
            [str(int((freqUMTS["900"][0]/totalUMTSCells)*100)), "TIM"], 
            [str(int((freqUMTS["1800"][0]/totalUMTSCells)*100)), "TIM"], 
            [str(int((freqUMTS["2100"][0]/totalUMTSCells)*100)), "TIM"], 
            [str(int((freqUMTS["2600"][0]/totalUMTSCells)*100)), "TIM"] ],
        freq2gP=[
            [str(int((freqGSM["700"][0]/totalGSMCells)*100)),"TIM"], 
            [str(int((freqGSM["850"][0]/totalGSMCells)*100)), "TIM"], 
            [str(int((freqGSM["900"][0]/totalGSMCells)*100)), "TIM"], 
            [str(int((freqGSM["1800"][0]/totalGSMCells)*100)), "TIM"], 
            [str(int((freqGSM["2100"][0]/totalGSMCells)*100)), "TIM"], 
            [str(int((freqGSM["2600"][0]/totalGSMCells)*100)), "TIM"] ]
    )

if __name__ == "__main__":
    app.run(host="10.129.33.217", port=8000)