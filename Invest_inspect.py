
"""This code shows the possibility for some predictive value in the
index invest. It is meant to give people a critical look at the scenario
described by Tobias Preis and colleagues"""


Inv_VIX = frame_queries_VIX[['INVEST', 'VIX']]
idx = Inv_VIX['INVEST'].idxmax()

Inv_shift = deepcopy(Inv_VIX)

Inv_corr_rev_shift = []

for shift_per in range(quarter):
    Inv_shift['VIX'] = Inv_VIX['VIX'].shift(periods=shift_per)
    Inv_mat = Inv_shift.dropna().corr(method = 'pearson')
    Inv_corr_rev_shift += [Inv_mat['INVEST'].loc['VIX']]

plt.plot(Inv_corr_rev_shift, color='y', label='VIX leading')
plt.title('VIX and INVEST shifted')
plt.axhline(linewidth=1, color='r', linestyle='dashed')    
plt.plot(corr_serieses['INVEST'], color='b', label='INVEST leading')
plt.xlabel('days shifted')
plt.ylabel('Correlations')
plt.legend()
plt.show()

plt.plot(Inv_VIX['INVEST'])
plt.title('INVEST')
plt.xlabel('Time')
plt.ylabel('Index')
plt.show()

plt.plot(Inv_VIX['VIX'])
plt.title('VIX index')
plt.xlabel('Time')
plt.ylabel('Index')
plt.show()

print Inv_VIX.loc[idx-10:idx+10:1], '\n'
print Inv_VIX.tail(10)
