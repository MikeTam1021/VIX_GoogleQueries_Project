from sklearn import linear_model

X = np.array(dataframe_shifts.loc[:,:'UNEMPL']) 
y = np.array(dataframe_shifts.loc[:,'VIX'])

P = np.array(prediction_mat)

tt = -30
features_train = X[:tt]
features_test = X[tt:]

targets_train = y[:tt]
targets_test = y[tt:]

model_line = linear_model.LinearRegression()
model_line.fit(features_train, targets_train)

print 'Coefficients: \n', model_line.coef_

print 'Residual sum of squares: %.2f' % np.mean((model_line.predict(features_test) - targets_test) ** 2)

print 'Variance score: %.2f' % model_line.score(features_test, targets_test)

plt.plot(targets_test)
plt.title('VIX Index')
plt.xlabel('time')
plt.ylabel('index_rating')
plt.show()

plt.plot(model_line.predict(features_test), 'r')
plt.title('VIX Prediction')
plt.xlabel('time')
plt.ylabel('index_rating')
plt.show()

rec_VIX = data.DataReader('^VIX', 'yahoo', futr_dates[0].date(), now)

predicts_line = pd.Series(model_line.predict(P), index=futr_dates[:min(shift_rows)+1])

plt.plot(rec_VIX['Close'], 'b')
plt.plot(predicts_line, 'r')
plt.title('Actual vs. predicted')
plt.show()

with pd.option_context('display.max_rows', 999, 'display.max_columns', 3):
    print pd.concat([rec_VIX['Close'], predicts_line], join= 'outer', axis = 1)
