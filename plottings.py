import matplotlib.pyplot as plt


"""plottings of the VIX, query indices, and correlation indices"""


plt.plot(frame_queries_VIX['VIX'])
plt.title('VIX')
plt.xlabel('time')
plt.ylabel('index')
plt.show()

for ind in indices:
    plt.plot(frame_queries_VIX[ind])
    plt.xlabel('time')
    plt.ylabel('index_rating')
    plt.axhline(y=1, linewidth=1, color='r', linestyle='dashed', label='1.0')
    plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
           ncol=2, mode="expand", borderaxespad=0.)
    plt.show()

for ind in indices:
    plt.plot(corr_serieses[ind], color='b', label=ind + ' correlation')
    plt.plot(corr_serieses[ind] - corr_serieses[ind].mean(), color='g', label='mean removed')
    plt.xlabel('days shifted')
    plt.ylabel('Correlations')
    plt.axhline(linewidth=1, color='r', linestyle='dashed')
    plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
           ncol=2, mode="expand", borderaxespad=0.)
    plt.show()

