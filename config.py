# config.py

DB_CONFIG = {
    "dbname": "datawarehouse_test",
    "user": "postgres",
    "password": "root",
    "host": "localhost",
    "port": "5432"
}

TICKERS = ['AI.PA','AIR.PA','ALO.PA','MT.AS','CS.PA','BNP.PA','EN.PA','CAP.PA','CA.PA','ACA.PA',
               'BN.PA','DSY.PA','EDEN.PA','ENGI.PA','EL.PA','ERF.PA','RMS.PA','KER.PA','OR.PA','LR.PA',
               'MC.PA','ML.PA','ORA.PA','RI.PA','PUB.PA','RNO.PA','SAF.PA','SGO.PA',
               'SAN.PA', 'SU.PA', 'GLE.PA', 'STLAP.PA', 'STMPA.PA', 'TEP.PA', 'HO.PA', 'TTE.PA', 'URW.PA', 'VIE.PA',
               'DG.PA', 'WLN.PA'
               ] 
SAVE_DIRECTORY = "./financial_data_lake"
