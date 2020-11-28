#!/usr/bin/env python
# coding: utf-8

# In[53]:


import pandas as pd


# In[54]:


def get_market_stats():
    years = [2014, 2015, 2016, 2017, 2018, 2019, 2020]

    cboe_df = pd.DataFrame()
    for year in years:
        df = pd.read_csv('data/market_history_%s.csv' % year)
        cboe_df = pd.concat([cboe_df, df])

    cboe_df = cboe_df.rename(columns={"Day": "Date"})
    cboe_df['Date'] = pd.to_datetime(cboe_df['Date'])
    cboe_df['Month'] = cboe_df['Date'].apply(lambda x: x.month)
    cboe_df['Year'] = cboe_df['Date'].apply(lambda x: x.year)
    cboe_df['Day'] = cboe_df['Date'].apply(lambda x: x.day)
    cboe_df['Quarter'] = cboe_df['Date'].apply(lambda x: x.quarter)
    cboe_df = cboe_df.sort_values('Date')
#     display(cboe_df)
    
    return cboe_df   


# In[55]:


def get_tradingdays(df):
    trading_days_df = df.copy()
    trading_days_df = trading_days_df.groupby(['Year', 'Quarter'])['Date'].nunique()
    trading_days_df = pd.DataFrame(trading_days_df).rename(columns={'Date': 'US Trading Days'})
    
    return trading_days_df 


# In[56]:


def group_by_quarter(df , trading_days_df):
    grouped_by_quarter_df = df.copy()
    grouped_by_quarter_df = grouped_by_quarter_df.groupby(['Year', 'Quarter']).sum()


    grouped_by_quarter_df = grouped_by_quarter_df.join(trading_days_df, on=['Year', 'Quarter'])
    return grouped_by_quarter_df


# In[57]:


def get_virtu_data():
    virtu_df = pd.read_excel('data/trading_income_quarterly.xlsx')
    virtu_df = virtu_df.set_index(['Year', 'Quarter'])
    
    virtu_df = virtu_df[['Net Revenue','Virtu Days','NR per day','Flow']]
    return virtu_df


# In[58]:


def get_vix_data():
    vix_df = pd.read_csv('data/vix.csv')
    
    vix_df['Date'] = pd.to_datetime(vix_df['Date'])
    vix_df['Year'] = vix_df['Date'].apply(lambda x: x.year)
    vix_df['Quarter'] = vix_df['Date'].apply(lambda x: x.quarter)
    vix_by_quarter_df = vix_df.groupby(['Year', 'Quarter']).mean()
    
    vix_final = pd.DataFrame(vix_by_quarter_df['Adj Close']).rename(columns={"Adj Close": "VIX"})
    
    return vix_final


# In[59]:


def main():
    
    df = get_market_stats()
    
    trading_days = get_tradingdays(df)
    
    dataset = group_by_quarter(df, trading_days)
    
    virtu_df = get_virtu_data()
    
    dataset = dataset.join(virtu_df, on=['Year', 'Quarter'])
    
    vix_df = get_vix_data()
    
    dataset = dataset.join(vix_df)
    
    dataset = dataset.dropna()
    return dataset


# In[60]:


df = main()

