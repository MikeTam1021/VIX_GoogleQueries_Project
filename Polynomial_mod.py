from sklearn import linear_model, preprocessing, pipeline

X = np.array(dataframe_shifts.loc[:,:'UNEMPL']) 
y = np.array(dataframe_shifts.loc[:,'VIX'])

P = np.array(prediction_mat)

tt = -30
features_train = X[:tt]
features_test = X[tt:]

targets_train = y[:tt]
targets_test = y[tt:]

model_poly = pipeline.Pipeline([('poly', preprocessing.PolynomialFeatures(degree=2)),
                     ('linear', linear_model.LinearRegression(fit_intercept=False))])

model_poly.fit(features_train, targets_train)

print 'Residual sum of squares: %.2f' % np.mean((model_poly.predict(features_test) - targets_test) ** 2)

print 'Variance score: %.2f' % model_poly.score(features_test, targets_test)

plt.plot(targets_test)
plt.title('VIX Index')
plt.xlabel('time')
plt.ylabel('index_rating')
plt.show()

plt.plot(model_poly.predict(features_test), 'r')
plt.title('VIX Prediction')
plt.xlabel('time')
plt.ylabel('index_rating')
plt.show()

predicts_poly = pd.Series(model_poly.predict(P), index=futr_dates[:min(shift_rows)+1])

plt.plot(rec_VIX['Close'], 'b')
plt.plot(predicts_poly, 'r')
plt.title('Actual vs. predicted')
plt.show()

with pd.option_context('display.max_rows', 999, 'display.max_columns', 3):
    print pd.concat([rec_VIX['Close'], predicts_ridge], join= 'outer', axis = 1)
