#!/usr/bin/env python
# coding: utf-8

# # Time series detecting model for queuing problem

# ### Use case: Algerie Poste
# #### DevFest competition 2021 by GDG Algiers
# ##### Team vision
# 
# - Mokeddem Ahmed Abdelaziz
# - Boumendjel Mohamed Islam
# - Bensalma Ibrahim
# - Adjal Zakaria Mehdi
# - Inezarene Abdelghafour

# In[33]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats
import pylab
#desactiver le systeme de warning
import warnings
warnings.filterwarnings("ignore")


# In[34]:


raw_csv_data=pd.read_csv("mockup.csv")
raw_csv_data


# In[35]:


raw_csv_data=pd.read_csv("mockup.csv")
df=raw_csv_data.copy()

df.plot(figsize=(20,6))


# In[36]:


scipy.stats.probplot(df.NbPeople,plot=pylab)
pylab.show()


# In[37]:


df.describe()


# In[38]:


df.head()


# In[39]:


df.Date=pd.to_datetime(df.Date,dayfirst=True)
df.set_index("Date",inplace=True)


# In[40]:


df.sort_values(by='Date')
df


# In[41]:


df.plot(figsize=(20,6))



# In[42]:


df.head()


# In[43]:


df.describe()
df=df.asfreq("b")
df.NbPeople=df.NbPeople.fillna(method="bfill")


# In[44]:


import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 
import statsmodels.graphics.tsaplots as sgt 
import statsmodels.tsa.stattools as sts 
from statsmodels.tsa.seasonal import seasonal_decompose
import seaborn as sns
sns.set()
sts.adfuller(df.NbPeople)


# In[45]:


s_dec_multiplicative=seasonal_decompose(df.NbPeople,model="multiplicative")
s_dec_multiplicative.plot()



# In[46]:


sgt.plot_acf(df.NbPeople,lags=40,zero=False)



# In[47]:


sgt.plot_pacf(df.NbPeople, lags=40, zero=False,method=("ols"))



# In[48]:


get_ipython().system('python -m pip install statsmodels ')


# In[52]:


from statsmodels.tsa.arima.model import ARIMA
model_ar=ARIMA(df.NbPeople,order=(1,0,0))
results_ar=model_ar.fit()
results_ar.summary()


# In[54]:


model_ar_2=ARIMA(df.NbPeople,order=(2,0,0))
results_ar_2=model_ar_2.fit()
results_ar_2.summary()


# In[56]:


# AR(3)
model_ar_3=ARIMA(df.NbPeople,order=(3,0,0))
results_ar_3=model_ar_3.fit()
results_ar_3.summary()


# In[57]:


# AR(4)
model_ar_4=ARIMA(df.NbPeople,order=(4,0,0))
results_ar_4=model_ar_4.fit()
results_ar_4.summary()


# In[58]:


from scipy.stats import chi2
def llr_test(mod_1,mod_2,DF=1):
    L1=mod_1.fit().llf
    L2=mod_2.fit().llf
    LR=(2*(L2-L1))
    p=chi2.sf(LR,DF).round(3)
    return p


# In[59]:


print(llr_test(model_ar,model_ar_2))
print(llr_test(model_ar_2,model_ar_3))
print(llr_test(model_ar_3,model_ar_4))


# In[61]:


# AR(9)
model_ar_9=ARIMA(df.NbPeople,order=(9,0,0))
results_ar_9=model_ar_9.fit()
results_ar_9.summary()
# AR(10)
model_ar_10=ARIMA(df.NbPeople,order=(10,0,0))
results_ar_10=model_ar_10.fit()
results_ar_10.summary()
# AR(11)
model_ar_11=ARIMA(df.NbPeople,order=(11,0,0))
results_ar_11=model_ar_11.fit()
results_ar_11.summary()
# AR(12)
model_ar_12=ARIMA(df.NbPeople,order=(12,0,0))
results_ar_12=model_ar_12.fit()
results_ar_12.summary()
print(llr_test(model_ar_11,model_ar_12))
df_pred_ar=model_ar_12


# In[62]:


size=int(len(df)*0.8)
df_test=df.iloc[size:] #testing set
df=df.iloc[:size] #training set
df_test.describe()


# In[64]:


from statsmodels.tsa.arima.model import ARIMA
model_ar = ARIMA(df.NbPeople, order = (1,0,0))
results_ar = model_ar.fit()


# In[65]:


df.tail()


# In[66]:


start_date = "2021-10-18"
end_date = "2021-10-21"


# In[67]:


from statsmodels.tsa.statespace.sarimax import SARIMAX
model_ret_sarimax = SARIMAX(df.NbPeople[1:], exog = df[["NbPeople"]][1:], 
                            order = (3,0,4), seasonal_order = (3,0,2,5))
results_ret_sarimax = model_ret_sarimax.fit()

df_pred_sarimax = results_ret_sarimax.predict(start = start_date, end = end_date, 
                                              exog = df_test[["NbPeople"]][start_date:end_date]) 

df_pred_sarimax[start_date:end_date].plot(figsize = (25,6), color = "black")
df_test.NbPeople[start_date:end_date].plot(color = "blue")
plt.title("Predictions vs Actual", size = 24)


# In[68]:


df_pred = results_ar.predict(start = start_date, end = end_date)
df_pred[start_date:end_date].plot(figsize = (20,5), color = "red")
df_test.NbPeople[start_date:end_date].plot(color = "blue")
plt.title("Predictions vs Actual", size = 24)


# In[69]:


model_ret_ma = ARIMA(df.NbPeople[1:], order=(0,0,1))
results_ret_ma = model_ret_ma.fit()

df_pred_ma = results_ret_ma.predict(start = start_date, end = end_date) 

df_pred_ma[start_date:end_date].plot(figsize = (20,5), color = "red")   
df_test.NbPeople[start_date:end_date].plot(color = "blue")
plt.title("Predictions vs Actual (Returns)", size = 24)



# In[70]:


model_ret_arma = ARIMA(df.NbPeople[1:], order=(1,0,1))
results_ret_arma = model_ret_arma.fit()

df_pred_arma = results_ret_arma.predict(start = start_date, end = end_date)

df_pred_arma[start_date:end_date].plot(figsize = (20,5), color = "red")   
df_test.NbPeople[start_date:end_date].plot(color = "blue")
plt.title("Predictions vs Actual (Returns)", size = 24)



# In[71]:


model_ret_armax = ARIMA(df.NbPeople[1:], exog = df[["NbPeople"]][1:], order = (1,0,1))
results_ret_armax = model_ret_armax.fit()

df_pred_armax = results_ret_armax.predict(start = start_date, end = end_date, 
                                          exog = df_test[["NbPeople"]][start_date:end_date]) 

df_pred_armax[start_date:end_date].plot(figsize = (20,5), color = "red")
df_test.NbPeople[start_date:end_date].plot(color = "blue")
plt.title("Predictions vs Actual (Returns)", size = 24)


# In[72]:


model_ret_sarma = SARIMAX(df.NbPeople[1:], order = (3,0,4), seasonal_order = (3,0,2,5))
results_ret_sarma = model_ret_sarma.fit()

df_pred_sarma = results_ret_sarma.predict(start = start_date, end = end_date)

df_pred_sarma[start_date:end_date].plot(figsize = (20,5), color = "red")
df_test.NbPeople[start_date:end_date].plot(color = "blue")
plt.title("Predictions vs Actual (SARMA)", size = 24)


# In[73]:


model_ret_sarimax = SARIMAX(df.NbPeople[1:], exog = df[["NbPeople"]][1:], order = (3,0,4), seasonal_order = (3,0,2,5))
results_ret_sarimax = model_ret_sarimax.fit()

df_pred_sarimax = results_ret_sarimax.predict(start = start_date, end = end_date, 
                                              exog = df_test[["NbPeople"]][start_date:end_date]) 

df_pred_sarimax[start_date:end_date].plot(figsize = (20,5), color = "red")
df_test.NbPeople[start_date:end_date].plot(color = "blue")
plt.title("Predictions vs Actual", size = 24)


# In[74]:


#results_ar_12[start_date:end_date].plot(figsize = (20,10), color = "yellow")
df_pred_ma[start_date:end_date].plot(color = "pink")
df_pred_arma[start_date:end_date].plot(color = "cyan")
df_pred_armax[start_date:end_date].plot(color = "green")
df_pred_sarma[start_date:end_date].plot(color = "magenta")
df_pred_sarimax[start_date:end_date].plot(color = "red")
df_test.NbPeople[start_date:end_date].plot(color = "blue")
plt.legend(['AR','MA','ARMA','ARMAX','SARMA','SARIMAX'])
plt.title("All the Models", size = 24)

# In[78]:


from pmdarima.arima import auto_arima


# In[79]:


from arch import arch_model
model_auto = auto_arima(df.NbPeople[1:], exogenous = df[['NbPeople']][1:],m = 5, max_p = 5, max_q = 5, max_P = 5, max_Q = 5)


# In[80]:


df_auto_pred = pd.DataFrame(model_auto.predict(n_periods = len(df_test[start_date:end_date]),
                            exogenous = df_test[['NbPeople']][start_date:end_date]),
                            index = df_test[start_date:end_date].index)


# In[82]:


df_auto_pred.plot(figsize = (20,5), color = "red")
df_test.NbPeople[start_date:end_date].plot(color = "blue")



# In[ ]:




