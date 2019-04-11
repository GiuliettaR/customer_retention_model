
### Logistic regretios
y = invoices_industry['repeat_c'] == True
X = invoices_industry[['year', 'month', 'unit_price', 'qty', 'account_id', 'amount', 'repeat_c','industry1']]

model1 = LogisticRegression()
model1.fit(X, y)
model1.coef_

### Random Fores

from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor, DecisionTreeClassifier
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier

from sklearn.model_selection import cross_val_score, train_test_split, GridSearchCV


y = pd.Series(invoices_industry.repeat_c)

X = invoices_industry [['year', 'month', 'unit_price', 'qty', 'account_id', 'amount', 'industry1']]

X_train, X_test, y_train, y_test = train_test_split(X, y,
                                                    test_size=.33,
                                                    random_state=2)



# Parameter Search
model = DecisionTreeClassifier(max_depth=5)

model.fit(X_train,y_train)
print(model.score(X_test, y_test))


# Parameter Search
model = DecisionTreeClassifier()
depth_parm = np.arange(1, 12, 1)
num_samples_parm = np.arange(5,95,10)
parameters = {'max_depth' : depth_parm,
             'min_samples_leaf' : num_samples_parm}
clf = GridSearchCV(model, parameters, cv=10, n_jobs=-1)
clf.fit(X_train,y_train)
print(clf.score(X_test, y_test))

y_train.mean()

clf.best_estimator_

clf.best_params_

# Train and fit model
rf = RandomForestClassifier(n_estimators=1000,
                           max_features='auto',
                           random_state=0, n_jobs=-1)
rf.fit(X_train, y_train)

# Test Prediction
pred = rf.predict(X_test)
print(rf.score(X_test, y_test))
