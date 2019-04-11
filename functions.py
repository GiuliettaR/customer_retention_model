import pandas as pd
import numpy as np
from pandas.tools.plotting import scatter_matrix

%matplotlib inline
import matplotlib.pyplot as plt
plt.style.use('ggplot')
from sklearn.linear_model import LogisticRegression#, LinearRegression

#importing zip_code_database####
accounts = pd.read_csv('data/MFG-accounts.csv')
customers = pd.read_csv('data/MFG-customers.csv')
invoices = pd.read_csv('data/MFG-invoices.csv')
industry = pd.read_csv('data/MFG-industry.csv')
press_release = pd.read_csv('data/Press_Release.csv')
zip_codes = pd.read_csv('data/zip_code_database.csv')
zip_codes = zip_codes[['zip','state']]

######accounts#####
label_df = pd.DataFrame(accounts['Account_Description'].unique())
   ### i write a new list with short names, it'll make more sence than the default long ones
label_df.columns = ['Account_Description']
label_list = [
    'scanning',
    'fdm',
    'carbon',
    'conlas',
    'manufacturing',
    'amermakes',
    'rent_inc_mfg',
    'sla',
    'molding',
    'casting',
    'sls',
    'polyjet',
    'metal',
    'freight',
    'cgb',
    'cgb',
    'misc',
    'asset'
]
label_df['label'] = label_list
accounts_labels = accounts.merge(label_df, left_on = 'Account_Description', right_on = 'Account_Description', how = 'left')
#create dummies columns for models
accounts_dummies = pd.get_dummies(accounts_labels, columns=['label'])


### Customers######
  #column country fixed
customers['Country'] = customers['Country'].replace(['UNITED STATES', 'United States'], ['USA', 'USA',])
customers['Country'] = customers['Country'].fillna('USA')
   ### change name to match other tables
customers['CustID'] = customers['CustomerID']
   ### state clean
customers['State'] = customers['State'].replace('az', 'AZ')
customers['State'] = customers['State'].replace('Te','TX')
customers['State'] = customers['State'].fillna('FO') #FO = not US state, foreign

### removing the end of the zip_codes
def strip_zip(longZip):
    value = str(longZip).split('-')[0]
    return value
customers['zipcode'] = customers['Zip'].apply(strip_zip)
#finish table with the data I care
customer_location = customers[['CustID', 'State','Zip','Country']]
## create dummies columns
customer_state_dummies = pd.get_dummies(customer_location, columns=['State'])
customer_region_dummies = pd.get_dummies(customer_state_dummies, columns=['Country'])


### Invoices########

invoices['datetime'] = pd.to_datetime(invoices['Date'])
invoices['dayofweek'] = invoices['datetime'].dt.dayofweek
invoices ['Amount'] = (invoices['Amount'].str.replace(',', '').astype(float)).abs()
invoices['Qty'] = invoices['Qty'].str.replace(',','').astype(float)
invoices['Qty'] = invoices['Qty'].fillna(0)

invoices['Account_ID'] = invoices['Account_ID'].str.replace('-','').astype(int)
invoices['Item_ID'] = invoices['Item_ID'].str.replace('-','')

invoices ['Unit_Price'] = invoices['Unit_Price'].str.replace(',','').astype(float)
invoices ['Unit_Price'] = invoices['Unit_Price'].fillna(0)



repeat=[]
for invoice in invoices.iterrows():
    repeat.append(((invoice[1]['CustID'] == invoices['CustID']) &
    (invoice[1]['datetime'] < invoices['datetime']) &
    (invoice[1]['datetime']  + pd.Timedelta(365, 'd') > invoices['datetime'])).sum()> 0)
invoices['repeat'] = repeat

def year(col):
    value = int(str(col)[0:4])
    return value

def month(col):
    value = int(str(col)[8:11])
    return value

invoices['year'] = invoices['datetime'].apply(year)
invoices['month'] = invoices['datetime'].apply(month)


def quarters(months):

    quarters=[]
    for month in months:
        if month>= 1 and month<=3:
            quarters.append(1)
        elif month >= 4 and month <= 6:
            quarters.append(2)
        elif month >= 7 and month<=9:
            quarters.append(3)
        elif month >= 10 and month >= 12:
            quarters.append(4)
        else:
            quarters.append(0)
    return quarters

invoices['quarter']= quarters(invoices['month'])

invoices['Item_ID'] = invoices['Item_ID'].fillna('other')
invoices['repeat_c']= invoices['repeat'].replace('True','1').astype(int)
invoices['repeat_c']= invoices['repeat'].replace('False','0').astype(int)

invoices_items_dummies = pd.get_dummies(invoices, columns=['Item_ID'])
invoices_items_year_dummies = pd.get_dummies(invoices_items_dummies, columns=['year'])
invoices_items_year_month_dummies = pd.get_dummies(invoices_items_year_dummies, columns=['month'])
invoices_items_year_month_quarter_dummies = pd.get_dummies(invoices_items_year_month_dummies, columns=['quarter'])

final_invoices = invoices_items_year_month_quarter_dummies


### press_release#####

press_release['release_date'] = pd.to_datetime(press_release['Release Date'])
press_release ['Premium'] = press_release['Premium'].str.replace('-', 'free')
press_release['Premium'] = press_release['Premium'].fillna('Premium')
press_release['headline_len'] = press_release['Headline'].str.len()


####industries###


industry_dummies = pd.get_dummies(industry, columns =['Industry'])


### merge invoices industry
invoices_industry = pd.merge(invoices, industry, how='left', on=['CustID'])
invoices_industry = pd.merge(invoices_industry, customer_location, how='left', on=['CustID'])
