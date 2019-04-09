import pandas as pd
import numpy as np

#import db
accounts = pd.read_csv('data/MFG-accounts.csv')
customers = pd.read_csv('data/MFG-customers.csv')
invoices = pd.read_csv('data/MFG-invoices.csv')
industry = pd.read_csv('data/MFG-industry.csv')
press_release = pd.read_csv('data/Press_Release.csv')

#new column quarter 1,2,3,4
quarter=[]
for quarter in invoices['month']:
    if quarter>= 1 or quarter<=3:
        quarter=1
    elif quarter >= 4 or quarter <= 6:
        quarter=2
    elif quarter >= 7 or quarter<=9:
        quarter=3
    else:
        quarter=4
invoices['quarter']= quarter

#cleaning columns
invoices['datetime'] = pd.to_datetime(invoices['Date'])
invoices['account_id'] = invoices['Account_ID'].str.replace('-','').astype(int)
invoices['itemid'] = invoices['Item_ID'].str.replace('-','')
invoices['qty'] = invoices['Qty'].str.replace(',','').astype(float)
invoices['qty'] = invoices['qty'].fillna(0)
invoices ['amount'] = (invoices['Amount'].str.replace(',', '').astype(float)).abs()
invoices ['unit_price'] = invoices['Unit_Price'].str.replace(',','').astype(float)
invoices ['unit_price'] = invoices['unit_price'].fillna(0)
invoices['dayofweek'] = invoices['datetime'].dt.dayofweek

#create new column, customer repeat year
repeat=[]
for invoice in invoices.iterrows():
    repeat.append(((invoice[1]['CustID'] == invoices['CustID']) &
    (invoice[1]['datetime'] < invoices['datetime']) &
    (invoice[1]['datetime']  + pd.Timedelta(365, 'd') > invoices['datetime'])).sum()> 0)
invoices['repeat'] = repeat

invoices['repeat_c']= invoices['repeat'].replace('True','1').astype(int)
invoices['repeat_c']= invoices['repeat'].replace('False','0').astype(int)

#create column with only month and only year
def year(col):
    value = int(str(col)[0:4])
    return value

def month(col):
    value = int(str(col)[8:11])
    return value

invoices['year'] = invoices['datetime'].apply(year)

invoices['month'] = invoices['datetime'].apply(month)

#join industry
invoices_industry = pd.merge(invoices, industry, how='left', on=['CustID'])

##cleaning Press_Release
press_release['release_date'] = pd.to_datetime(press_release['Release Date'])
press_release ['premium'] = press_release['Premium'].str.replace('-', 'free')
press_release['premium'] = press_release['premium'].fillna('premium')
press_release['headline_len'] = press_release['Headline'].str.len()
