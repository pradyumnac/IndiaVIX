#!/usr/bin/env python
# coding: utf-8

# # Indiavix

# In[1]:


get_ipython().system('pip install html5lib')
get_ipython().system('pip install tabulate')


# In[2]:


import requests
import pandas as pd
from lxml import html
from io import StringIO
from datetime import datetime as dt, timedelta
from IPython.display import Markdown, display
from tabulate import tabulate


# In[3]:


def get_vix(oprn_dt):
    today_str = (oprn_dt).strftime("%d-%b-%Y")
    oneyearago_str = (oprn_dt+timedelta(days=-364)).strftime("%d-%b-%Y")
    url = f"https://www.nseindia.com/products/dynaContent/equities/indices/hist_vix_data.jsp?&fromDate={oneyearago_str}&toDate={today_str}"
    res = requests.get(url)
    print("Operation status: ", url, res.status_code)
    tree = html.fromstring(res.text)
    csvdata = tree.xpath(r'//*[@id="csvContentDiv"]')[0].text
    df = pd.read_csv(StringIO(csvdata), lineterminator =":")
    df.columns = [i.strip() for i  in df.columns]
#     print(df.columns)
    df['Pct Rank']=df['% Change'].rank(pct=True)
    df['Close Rank']=df['Close'].rank(pct=True)
    
    pct_stats = {
        "pct_mean"                : df['% Change'].mean(),
        "pct_median"              : df['% Change'].median(), 
        "pct_std"                 : df['% Change'].std(),
        "pct_q10"                 :df['% Change'].quantile(0.1),
        "pct_q90"                 : df['% Change'].quantile(0.9),
        "pct_lastpercentilescore" : df['Pct Rank'].iloc[-1:].values[0]*100
    }
    
    close_stats = {
        "close_mean"                : df['Close'].mean(),
        "close_median"              : df['Close'].median(), 
        "close_std"                 : df['Close'].std(),
        "close_q10"                 : df['Close'].quantile(0.1),
        "close_q90"                 : df['Close'].quantile(0.9),
        "close_lastpercentilescore" : df['Close Rank'].iloc[-1:].values[0]*100
    }
    
    return df, pct_stats, close_stats


# In[4]:


report_md_str=''
def add_to_report(string):
    global report_md_str
#     display(Markdown(string))
    report_md_str+=string+"  \n"
    
def prepare_report(df, pct_stats, close_stats):
    global report_md_str
    report_md_str = ''
    add_to_report('---  ')
    add_to_report('## Today:  ')
    add_to_report('---  ')
    add_to_report(tabulate(df.iloc[-1:], tablefmt="pipe", headers="keys")+"  \n  \n")
    add_to_report('---  ')
    add_to_report('## History of "Closing Volatility":  ')
    add_to_report('**Mean:** {0:.2f}, **Median:** {1:.2f}, **Standard Deviation:** {2:.2f}, **Quantile 10%:** {3:.2f}, **Quantile 90%:** {4:.2f}'.format(close_stats['close_mean'], close_stats['close_median'], close_stats['close_std'], close_stats['close_q10'], close_stats['close_q90']))
    add_to_report('**Percentile Rank of "Close Vol":** {:.2f}%'.format(close_stats['close_lastpercentilescore']))
    add_to_report('  \n---  ')
    add_to_report('## History of "% Change in Volatility":  ')
    add_to_report('**Mean:** {0:.2f}, **Median:** {1:.2f}, **Standard Deviation:** {2:.2f}, **Quantile 10%:** {3:.2f}, **Quantile 90%:** {4:.2f}'.format(pct_stats['pct_mean'], pct_stats['pct_median'], pct_stats['pct_std'], pct_stats['pct_q10'], pct_stats['pct_q90']))
    add_to_report('**Percentile Rank of "% Change":** {:.2f}%'.format(pct_stats['pct_lastpercentilescore']))
    return report_md_str


# In[6]:


today = dt.now() # Not supported while market is open
yesterday = today+timedelta(days=-1)
df, pct_stats, close_stats = get_vix(yesterday)
report = prepare_report(df, pct_stats, close_stats)
display(Markdown(report))


# In[ ]:




