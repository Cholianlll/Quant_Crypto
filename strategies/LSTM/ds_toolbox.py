# reference: https://github.com/mscharth/qbus6810/blob/master/statlearning.py
# version 1.0
# Modified by Cholian (Chao Li)


# Imports
import pandas as pd
import numpy as np
from scipy import stats
import statsmodels.api as sm
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt
import itertools



def mae(response, predicted):
    
    y = np.array(np.abs(np.ravel(response)-np.ravel(predicted)))
    mae = np.mean(y)
    se = np.std(y)/np.sqrt(len(y))

    return mae, se


def rmse(response, predicted):
    
    y = np.array((np.ravel(response)-np.ravel(predicted))**2)
    y_sum = np.sum(y)
    n = len(y)

    resample = np.sqrt((y_sum-y)/(n-1))

    rmse = np.sqrt(y_sum/n)
    se = np.sqrt((n-1)*np.var(resample))

    return rmse, se

def r_squared(response, predicted):


    e2 = np.array((np.ravel(response)-np.ravel(predicted))**2)
    y2 = np.array((np.ravel(response)-np.mean(np.ravel(response)))**2)

    rss = np.sum(e2)
    tss = np.sum(y2)
    n = len(e2)

    resample = 1-(rss-e2)/(tss-y2)

    r2 = 1-rss/tss
    se = np.sqrt((n-1)*np.var(resample))

    return r2, se


def forwardselection(X, y):
    """Forward variable selection based on the Scikit learn API
    
    
    Output:
    ----------------------------------------------------------------------------------
    Scikit learn OLS regression object for the best model
    """

    # Functions
    from sklearn.linear_model import LinearRegression
    from sklearn.model_selection import cross_val_score

    # Initialisation
    base = []
    p = X.shape[1]
    candidates = list(np.arange(p))

    # Forward recursion
    i=1
    bestcvscore=-np.inf    
    while i<=p:
        bestscore = 0
        for variable in candidates:
            ols = LinearRegression()
            ols.fit(X[:, base + [variable]], y)
            score = ols.score(X[:, base + [variable]], y)
            if score > bestscore:
                bestscore = score 
                best = ols
                newvariable=variable
        base.append(newvariable)
        candidates.remove(newvariable)
        
        cvscore = cross_val_score(best, X[:, base], y, scoring='neg_mean_squared_error').mean() 
        
        if cvscore > bestcvscore:
            bestcvscore=cvscore
            bestcv = best
            subset = base[:]
        i+=1
    
    #Finalise
    return bestcv, subset


class forward:
    def __init__(self):
        pass

    def fit(self, X, y):
        self.ols, self.subset = forwardselection(X, y)

    def predict(self, X):
        return self.ols.predict(X[:, self.subset])

    def cv_score(self, X, y, cv=5):
        from sklearn.model_selection import cross_val_score
        scores = cross_val_score(self.ols, X[:, self.subset], np.ravel(y), cv=cv, scoring='neg_mean_squared_error')
        return np.sqrt(-1*np.mean(scores))
        

class PCR:
    def __init__(self, M=1):
        self.M=M

    def fit(self, X, y):
        from sklearn.decomposition import PCA
        from sklearn.linear_model import LinearRegression
        
        self.pca=PCA(n_components=self.M)
        Z = self.pca.fit_transform(X)
        self.pcr = LinearRegression().fit(Z, y)

    def predict(self, X):
        return self.pcr.predict(self.pca.transform(X))

    def cv_score(self, X, y, cv=10):
        from sklearn.model_selection import cross_val_score
        Z=self.pca.transform(X)
        scores = cross_val_score(self.pcr, Z, np.ravel(y), cv=cv, scoring='neg_mean_squared_error').mean() 
        return np.sqrt(-1*np.mean(scores))


def pcrCV(X, y):
    from sklearn.model_selection import cross_val_score
    
    p=X.shape[1]
    bestscore= -np.inf
    cv_scores = []
    for m in range(1,p+1):
        model = PCR(M=m)
        model.fit(X, y)
        Z=model.pca.transform(X)
        score = cross_val_score(model.pcr, Z, y, cv=5, scoring='neg_mean_squared_error').mean() 
        cv_scores.append(score)
        if score > bestscore:
            bestscore=score
            best=model

    best.cv_scores = pd.Series(cv_scores, index = np.arange(1,p+1))
    return best


def plsCV(X, y):

    from sklearn.cross_decomposition import PLSRegression
    from sklearn.model_selection import cross_val_score
    
    p=X.shape[1]
    bestscore=-np.inf
    for m in range(1,p): # not fitting with M=p avoids occasional problems
        pls = PLSRegression(n_components=m).fit(X, y)
        score = cross_val_score(pls, X, y, cv=10, scoring='neg_mean_squared_error').mean() 
        if score > bestscore:
            bestscore=score
            best=pls
    return best


from sklearn.linear_model import Lasso, LassoCV, LinearRegression


class AdaLasso:
    def __init__(self, lambda_, gamma=1, weights_estimator=LinearRegression(), fit_intercept=True):
        self.lambda_ = lambda_
        self.gamma = gamma
        self.weights_estimator = weights_estimator
        self.fit_intercept = fit_intercept
    
    def fit(self, X_train, y_train):
        X = np.array(X_train)
        y = np.ravel(y_train)
        n, p = X.shape

        model = self.weights_estimator.fit(X_train, y_train)    
        self.weights = 1/np.abs(model.coef_)**self.gamma
        
        X_transf = X/self.weights.reshape((1,-1))

        self.estimator = Lasso(alpha=self.lambda_, fit_intercept=self.fit_intercept).fit(X_transf, y)
        self.coef_ = self.estimator.coef_/self.weights        
        return self        
           
    def predict(self, X_test): 
        return self.estimator.predict(X_test.reshape((-1, 1))/self.weights.reshape((1,-1)))


class AdaLassoCV:
    def __init__(self, gamma=1, weights_estimator=LinearRegression(), fit_intercept=True, cv=5):
        self.gamma = gamma
        self.weights_estimator = weights_estimator
        self.fit_intercept = fit_intercept
        self.cv = cv
    
    def fit(self, X_train, y_train):
        X = np.array(X_train)
        y = np.ravel(y_train)
        n, p = X.shape

        model = self.weights_estimator.fit(X_train, y_train)    
        self.weights = 1/np.abs(model.coef_)**self.gamma
        
        X_transf = X/self.weights.reshape((1,-1))

        self.estimator = LassoCV(fit_intercept=self.fit_intercept, cv=self.cv).fit(X_transf, y)
        self.coef_ = self.estimator.coef_/self.weights        
        return self        
           
    def predict(self, X_test): 
        return self.estimator.predict(X_test/self.weights.reshape((1,-1)))


from patsy import dmatrix, build_design_matrices



def GAM_design_train(X_train, dfs, degree=3):
    p=X_train.shape[1]
    train_splines = []
   
    for j in range(p):
        if dfs[j] > 0:          
            if dfs[j]==1:
                train_splines.append(X_train[:,j].reshape((-1,1)))
            else:
                a=X_train[:,j].min() # lower bound 
                b=X_train[:,j].max() # upper bound
                if dfs[j]==2:
                    X = dmatrix('bs(x, degree=1, df=2, lower_bound=a, upper_bound=b) - 1',{'x': X_train[:,j]}, 
                        return_type='matrix')
                else:
                    if degree > 1:
                        X = dmatrix('cr(x, df=dfs[j], lower_bound=a, upper_bound=b) - 1', {'x': X_train[:,j]}, 
                            return_type='matrix')
                    else: 
                        X = dmatrix('bs(x, degree=1, df=dfs[j], lower_bound=a, upper_bound=b) - 1', {'x': X_train[:,j]}, 
                            return_type='matrix')
                train_splines.append(X)
    
    if len(train_splines)>1:        
        X_train_gam = np.hstack(train_splines) 
    else:
        X_train_gam=train_splines[0]
    
    return  X_train_gam

def GAM_design_test(X_train, X_test, dfs, degree=3):

    if type(X_test)!=np.ndarray:
        X_test = np.array(X_test)
    
    p=X_train.shape[1]
    train_splines = []
    test_splines = []
   
    for j in range(p):
        
        if dfs[j] > 0:          
            if dfs[j]==1:
                train_splines.append(X_train[:,j].reshape((-1,1)))
                test_splines.append(X_test[:,j].reshape((-1,1)))
            else:
                a=min(np.min(X_train[:,j]), np.min(X_test[:,j])) # lower bound 
                b=max(np.max(X_train[:,j]), np.max(X_test[:,j])) # upper bound 
                if dfs[j]==2:
                    X = dmatrix('bs(x, degree=1, df=2, lower_bound=a, upper_bound=b) - 1',{'x': X_train[:,j]}, 
                        return_type='matrix')
                else:
                    if degree > 1:
                        X = dmatrix('cr(x, df=dfs[j], lower_bound=a, upper_bound=b) - 1', {'x': X_train[:,j]}, 
                            return_type='matrix')
                    else: 
                        X = dmatrix('bs(x, degree=1, df=dfs[j], lower_bound=a, upper_bound=b) - 1', {'x': X_train[:,j]}, 
                            return_type='matrix')
                train_splines.append(X)
                test_splines.append(build_design_matrices([X.design_info], {'x': X_test[:,j]})[0])
               
    X_train_gam = np.hstack(train_splines) 
    X_test_gam = np.hstack(test_splines) 
    
    return  X_train_gam, X_test_gam

from sklearn.linear_model import LinearRegression
from sklearn.model_selection import cross_val_score

def GAM_backward_selection(X_train, y_train, max_dfs, max_params, degree):

    # Initialisation
    p = X_train.shape[1]
    dfs = np.array(max_dfs)    

    # Full model
    X_train_gam = GAM_design_train(X_train, dfs, degree) 
    ols = LinearRegression().fit(X_train_gam, y_train)
    cv_score = np.mean(cross_val_score(ols, X_train_gam, y_train, 
            scoring='neg_mean_squared_error', cv=len(y_train)))

    if np.sum(dfs)<=max_params:
        best_cv_score= cv_score
        best_cv_ols = ols
        best_cv_dfs = np.copy(dfs)
        best_cv_X_train = np.copy(X_train_gam)
    else:
        best_cv_score = -np.inf
    
    # Initialising cross validation information
    cv_scores=pd.Series([-1*best_cv_score], index=[np.sum(dfs)])

    # Backward algorithm
    i=np.sum(dfs)-1
    while i > 0:  
        best_score = -np.inf
        for j in range(p):
            if dfs[j] > 0:
                dfs[j]-= 1
                X_train_gam = GAM_design_train(X_train, dfs, degree) 
                ols = LinearRegression().fit(X_train_gam, y_train)
                score = ols.score(X_train_gam, y_train)
                if score > best_score:
                    best_score = score 
                    best_ols = ols
                    best_X_train = np.copy(X_train_gam)
                    best_dfs = np.copy(dfs) 
                dfs[j]+= 1
        
        # cv_score = np.mean(cross_val_score(best_ols, best_X_train, y_train, 
        #     scoring='neg_mean_squared_error', cv=len(y_train)))
        cv_score = np.mean(cross_val_score(best_ols, best_X_train, y_train, 
            scoring='neg_mean_squared_error', cv=len(y_train)))
        
        if (cv_score > best_cv_score) & (i<=max_params):   
            best_cv_score=cv_score
            best_cv_ols = best_ols
            best_cv_dfs = np.copy(best_dfs)
            best_cv_X_train = np.copy(best_X_train)
            
        dfs=np.copy(best_dfs)
        cv_scores[i]=-1*cv_score
        i-=1
    
    return best_cv_ols, best_cv_dfs, best_cv_X_train, cv_scores.sort_index()


class GAM_splines:
    def __init__(self, degree=3, labels=None):
        self.degree = degree
        self.labels = labels
    
    def fit(self, X, y, max_dfs):
        n, p = X.shape
        self.predictors = list(np.arange(p))
        self.X_train =  np.array(X)
        self.y_train = np.ravel(y)

        dfs=np.array(max_dfs)
        max_dfs_model = np.sum(dfs)

        self.ols, self.dfs, self.X_train_gam,  self.cv_scores  = GAM_backward_selection(self.X_train, self.y_train, dfs, max_dfs_model, self.degree)

    def info(self):
        print('Selected degrees of freedom (backward algorithm): \n')
        if self.labels:
            print(pd.Series(self.dfs, index=self.labels))
        else:
            print(pd.Series(self.dfs, index=self.predictors))

    def plot_cv(self):
        fig, ax = plt.subplots(figsize=(8,5))
        ax.plot(self.cv_scores)
        ax.set_xlabel('Degrees of freedom')
        ax.set_ylabel('Cross validation error')
        sns.despine()
        fig.show()
        return fig, ax  

    def predict(self, X_test):
        self.X_train_gam, X_test_gam =  GAM_design_test(self.X_train, X_test, self.dfs, self.degree)
        self.ols = LinearRegression().fit(self.X_train_gam, self.y_train)
        return self.ols.predict(X_test_gam)

from statsmodels.nonparametric.kernel_regression import KernelReg


class LocalRegression:
    def __init__(self):
        pass
    
    def fit(self, X_train, y_train):
        # By default, this function will do a local linear regression
        self.regression = KernelReg(y_train, X_train, var_type='c')
        return self
        
    def predict(self, X_test):
        return self.regression.fit(X_test)[0]

from sklearn.linear_model import LinearRegression


class GAM_local:
    """
    Generalised additive regression model
    
    Parameters
    ----------
    smoother : 
        One-dimensional smoother object implementing fit and predict methods.
        
    linear : list, optional, default empty list
        List of predictor variables that will enter the model via linear terms.
        The values can be either numerical indexes or strings containing the names
        of the predictors. 
    """
    
    def __init__(self, linear=[]):
        self.smoother = LocalRegression
        self.linear = linear 

    def fit(self, X_train, y_train, tol=0.005, verbose=False):
        
        n, p = X_train.shape
        
        # This section is a detail. It makes the class handle both variable names and numbers in the list
        # of predictors that will form the linear part of the model.
        if len(self.linear) > 0:
            if type(self.linear[0])==str:
                predictors = list(X_train.columns)
                self.linear_indexes_ = [predictors.index(predictor) for predictor in self.linear]
            else:
                self.linear_indexes_ = [predictor for predictor in self.linear]
        self.nonlinear_indexes_ = [i for i in range(p) if i not in self.linear_indexes_]
        
        # It is better to convert the data to NumPy arrays
        y_train = np.ravel(y_train)
        X_train = np.array(X_train)
        
        # Separating the predictors for the linear and nonlinear parts of the model
        X_linear = X_train[:, self.linear_indexes_]
        X_nonlinear = X_train[:, self.nonlinear_indexes_]
        
        self.intercept = np.mean(y_train)
        y_hat = self.intercept
        
        p = len(self.nonlinear_indexes_)
        f_hat = np.zeros((n,p))
        offset = np.zeros(p)
        
        counter = 0
        iterate = True
        while iterate: 
            
            counter+= 1 # this syntax adds one to counter
            if verbose:
                print(f'Iteration {counter}')
            y_hat_0 = np.copy(y_hat) # copying is safer 
            
            
            if len(self.linear) > 0: 
                # If the model has linear components, it is efficient to fit the entire linear
                # part in one block by OLS.
                y_tilde = y_train-self.intercept-np.sum(f_hat, axis=1)
                ols = LinearRegression().fit(X_linear, y_tilde)
                partial_fit = self.intercept + ols.predict(X_linear)
                
            else: 
                partial_fit = self.intercept
            
            # These are the residuals after subtracting the intercept and the linear fit
            partial_resid  = y_train - partial_fit
            
            smoothers = []
            # Iterating over the nonlinear predictors
            for j in range(p):
                # The simplest syntax is to subtract f_hat[:,j] then add it back
                y_tilde = partial_resid-np.sum(f_hat, axis=1) + f_hat[:,j]
                
                # Setting up the smoother for nonlinear predictor j, we fit the residuals
                smoothers.append(self.smoother().fit(X_nonlinear[:,j], y_tilde))
                
                # Applying up the smoother for nonlinear predictor j
                f_hat[:, j] = smoothers[j].predict(X_nonlinear[:,j]) 
                
                # Remember that we need to subtract the average of f_hat[:, j]
                offset[j] = np.mean(f_hat[:, j])
                f_hat[:, j] = f_hat[:, j] - offset[j]       
            
            # Updated fitted value once we cycle through all predictors
            y_hat = partial_fit + np.sum(f_hat, axis=1)
            criterion = max(np.abs(y_hat-y_hat_0)) 
            if verbose:
                print(f'Convergence criterion: {criterion}\n')
            iterate =  criterion  > tol
        
        self.smoothers_ = smoothers
        self.offset_ = offset
        if len(self.linear) > 0:
            self.ols_ = ols
        
        return self
           
    def predict(self, X_test):
        
        if len(self.linear) > 0: 
            X_linear = np.array(X_test)[:,self.linear_indexes_]
            y_pred = self.intercept + self.ols_.predict(X_linear)
        else: 
            y_pred = self.intercept
        
        X_nonlinear = np.array(X_test)[:,self.nonlinear_indexes_]
        p = X_nonlinear.shape[1]
      
        for j in range(p):
            y_pred+= self.smoothers_[j].predict(X_nonlinear[:,j])-self.offset_[j]
    
        return y_pred



def plot_additive_local_fit(X, y, model):

    labels = list(X.columns)

    X = np.array(X)
    y = np.ravel(y)
    
    N, p = X.shape

    rows = int(np.ceil(p/3)) 

    fig, axes = plt.subplots(rows, 3, figsize=(12, rows*(12/4)))

    j = 0  # counter for the linear predictors
    k = 0  # counter for the nonlinear predictors
    for i, ax in enumerate(fig.axes):
        
        if i < p:
            a = np.min(X[:,i])
            b = np.max(X[:,i])
            x = np.linspace(a, b).reshape((-1,1))

            if i in model.linear_indexes_:
                y_pred = x*model.ols_.coef_[j]
                j+=1
            else:
                y_pred = model.smoothers_[k].predict(x)-model.offset_[k]
                k+=1 

            ax.plot(np.ravel(x), np.ravel(y_pred))
            ax.set_ylim(min(y)-model.intercept, max(y)-model.intercept)
            ax.set_xlabel('')
            ax.set_ylabel('')
            ax.set_title(labels[i])
        else:
            fig.delaxes(ax)

    sns.despine()
    plt.tight_layout()
    
    return fig, axes



def plot_dist(series, bins = 10):
    fig, ax= plt.subplots(figsize=(9,6))
    # sns.distplot(series, ax=ax, hist_kws={'alpha': 0.9, 'edgecolor':'black'},  
    #     kde_kws={'color': 'black', 'alpha': 0.7})
    sns.histplot(series, color='#264653', stat='density', ax=ax, bins=bins)
    sns.kdeplot(series, color='#E76F51',ax = ax)
    
    sns.despine()
    return fig, ax

def plot_density(series, num = 30):
    
    fig, ax= plt.subplots(figsize=(9,6))
    s = pd.DataFrame(series.value_counts().sort_values(ascending=False)[:num])
    s.columns = {'Frequency'}
    s = s.reset_index(drop= False)
    
    sns.barplot(y="index", x="Frequency", facecolor=(1, 1, 1, 0), errcolor=".2", edgecolor=".2", data=s)
    ax.set_ylabel('')
    sns.despine()
    return fig, ax

def plot_dists(X, kde=True,plots_in_col = 3,bins = 10):

    labels = list(X.columns)
    
    N, p = X.shape

    rows = int(np.ceil(p/plots_in_col)) 

    fig, axes = plt.subplots(rows, plots_in_col, figsize=(12, rows*(12/4)))

    for i, ax in enumerate(fig.axes):
        if i < p:
            sns.histplot(X.iloc[:,i], color='#264653', stat='density', ax=ax, bins=bins)
            sns.kdeplot(X.iloc[:,i], color='#E76F51',ax = ax)
            # sns.histplot(X.iloc[:,i], ax=ax, kde=kde, thresh=0.9, edgecolor='black', bins = 10)
            ax.set_xlabel('')
            ax.set_ylabel('')
            ax.set_title(labels[i])
            ax.set_yticks([])
        else:
            fig.delaxes(ax)

    sns.despine()
    plt.tight_layout()
    
    return fig,


def plot_boxplots(X, category = None, plots_in_col = 3):

    ## ref https://github.com/mscharth/qbus6810/blob/master/statlearning.py
    labels = list(X.columns)
    
    N, p = X.shape

    rows = int(np.ceil(p/plots_in_col)) 

    fig, axes = plt.subplots(rows, plots_in_col, figsize=(12, rows*(12/4)))

    for i, ax in enumerate(fig.axes):
        if i < p:
            sns.boxplot(y = X.iloc[:,i], x = category,  orient = 'v', ax=ax)
            ax.set_xlabel('')
            ax.set_ylabel('')
            ax.set_title(labels[i])
        else:
            fig.delaxes(ax)

    sns.despine()
    plt.tight_layout()
    
    return fig, axes


def plot_correlation_matrix(X, figsize = (20,15)):

    fig, ax = plt.subplots(figsize = figsize)
    cmap = sns.diverging_palette(220, 10, as_cmap=True)
    sns.heatmap(X.corr(), ax=ax, cmap=cmap)
    ax.set_title('Correlation matrix', fontweight='bold', fontsize=13)
    plt.tight_layout()

    return fig, ax


def plot_regressions(X, y, plots_in_col = 3, lowess=False):

    labels = list(X.columns)
    
    N, p = X.shape

    rows = int(np.ceil(p/plots_in_col)) 

    fig, axes = plt.subplots(rows, plots_in_col, figsize=(12, rows*(12/4)))

    for i, ax in enumerate(fig.axes):
        if i < p:
            sns.regplot(X.iloc[:,i], y,  ci=None, y_jitter=0.05, 
                        scatter_kws={'s': 25, 'alpha':.8}, ax=ax, lowess=lowess,
                        line_kws={"color": "#c02c38"})
            ax.set_xlabel('')
            ax.set_ylabel('')
            ax.set_title(labels[i])
        else:
            fig.delaxes(ax)

    sns.despine()
    plt.tight_layout()
    
    return fig, axes


def plot_logistic_regressions(X, y):
    labels = list(X.columns)
    
    N, p = X.shape

    rows = int(np.ceil(p/3)) 

    fig, axes = plt.subplots(rows, 3, figsize=(12, rows*(11/4)))

    for i, ax in enumerate(fig.axes):
        if i < p:          
            sns.regplot(X.iloc[:,i], y,  ci=None, logistic=True, y_jitter=0.05, 
                        scatter_kws={'s': 25, 'alpha':.5}, ax=ax)
            ax.set_xlabel('')
            ax.set_ylabel('')
            ax.set_yticks([])
            ax.set_xticks([])
            ax.set_title(labels[i])
            ax.set_xlim(X.iloc[:,i].min(),X.iloc[:,i].max())
        else:
            fig.delaxes(ax)

    sns.despine()
    plt.tight_layout()

    return fig, axes


def plot_conditional_distributions(X, y, labels=[None, None]):

    variables = list(X.columns)
    
    N, p = X.shape

    rows = int(np.ceil(p/3)) 

    fig, axes = plt.subplots(rows, 3, figsize=(11, rows*(12/4)))
    
    for i, ax in enumerate(fig.axes):

        if i < p:
            sns.kdeplot(X.loc[y==0, variables[i]], ax=ax, label=labels[0])
            ax.set_ylim(auto=True)
            sns.kdeplot(X.loc[y==1, variables[i]], ax=ax, label=labels[1])
            ax.set_xlabel('')
            ax.set_yticks([])
            ax.set_xticks([])
            ax.set_title(variables[i])
           
        else:
            fig.delaxes(ax)

    sns.despine()
    fig.tight_layout()
    plt.show()
    
    return fig, ax

# This function is from the scikit-learn documentation
# http://scikit-learn.org/stable/auto_examples/model_selection/plot_confusion_matrix.html
def plot_confusion_matrix(cm, classes,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    #print(cm)

    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    fmt = '.3f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], fmt),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')


import seaborn as sns


def plot_coefficients(model, labels):
    coef = model.coef_
    table = pd.Series(coef.ravel(), index = labels).sort_values(ascending=True, inplace=False)
    
    all_ = True
    if len(table) > 20:
        reference = pd.Series(np.abs(coef.ravel()), index = labels).sort_values(ascending=False, inplace=False)
        reference = reference.iloc[:20]
        table = table[reference.index]
        table = table.sort_values(ascending=True, inplace=False)
        all_ = False
        

    fig, ax = fig, ax = plt.subplots()
    table.T.plot(kind='barh', edgecolor='black', width=0.7, linewidth=.8, alpha=0.9, ax=ax)
    ax.tick_params(axis=u'y', length=0) 
    if all_:
        ax.set_title('Estimated coefficients', fontsize=14)
    else: 
        ax.set_title('Estimated coefficients (20 largest in absolute value)', fontsize=14)
    sns.despine()
    return fig, ax


def plot_feature_importance(model, labels, max_features = 20):
    feature_importance = model.feature_importances_*100
    feature_importance = 100*(feature_importance/np.max(feature_importance))
    table = pd.Series(feature_importance, index = labels).sort_values(ascending=True, inplace=False)
    fig, ax = fig, ax = plt.subplots(figsize=(9,6))
    if len(table) > max_features:
        table.iloc[-max_features:].T.plot(kind='barh', edgecolor='black', width=0.7, linewidth=.8, alpha=0.9, ax=ax)
    else:
        table.T.plot(kind='barh', edgecolor='black', width=0.7, linewidth=.8, alpha=0.9, ax=ax)
    ax.tick_params(axis=u'y', length=0) 
    ax.set_title('Variable importance', fontsize=13)
    sns.despine()
    return fig, ax


def plot_feature_importance_xgb(model):
    feature_importance = pd.Series(model.get_fscore())
    feature_importance = 100*(feature_importance/np.max(feature_importance))
    table = feature_importance.sort_values(ascending=True, inplace=False)
    fig, ax = fig, ax = plt.subplots(figsize=(9,6))
    table.T.plot(kind='barh', edgecolor='black', width=0.7, linewidth=.8, alpha=0.9, ax=ax)
    ax.tick_params(axis=u'y', length=0) 
    ax.set_title('Variable importance', fontsize=13)
    sns.despine()
    return fig, ax


from sklearn.metrics import roc_curve
from sklearn.metrics import roc_auc_score

def plot_roc_curves(y_test, y_probs, labels, sample_weight=None):
    
    fig, ax= plt.subplots(figsize=(9,6))

    N, M=  y_probs.shape

    for i in range(M):
        fpr, tpr, _ = roc_curve(y_test, y_probs[:,i], sample_weight=sample_weight)
        auc = roc_auc_score(y_test, y_probs[:,i], sample_weight=sample_weight)
        ax.plot(1-fpr, tpr, label=labels.iloc[i] + ' (AUC = {:.3f})'.format(auc))
    
    ax.plot([0,1],[1,0], linestyle='--', color='black', alpha=0.6)

    ax.set_xlabel('Specificity')
    ax.set_ylabel('Sensitivity')
    ax.set_title('ROC curves', fontsize=14)
    sns.despine()

    plt.legend(fontsize=13, loc ='lower left' )
    
    return fig, ax


def barplots(X):

    labels = list(X.columns)
    
    N, p = X.shape

    rows = int(np.ceil(p/3)) 

    fig, axes = plt.subplots(rows, 3, figsize=(12, rows*(12/4)))

    for i, ax in enumerate(fig.axes):
        if i < p:
            X[labels[i]].value_counts().sort_index().plot(kind='bar', alpha=0.9, ax=ax)
            ax.set_xlabel('')
            ax.set_ylabel('')
            ax.set_title(labels[i])
            ax.set_yticks([])
        else:
            fig.delaxes(ax)

    sns.despine()
    plt.tight_layout()
    
    return fig, axes




def crosstabplots(X, y):
    colors = sns.color_palette() 

    labels = list(X.columns)
    
    N, p = X.shape

    rows = int(np.ceil(p/3)) 

    fig, axes = plt.subplots(rows, 3, figsize=(12, rows*(12/4)))

    for i, ax in enumerate(fig.axes):
        if i < p:
            
            table=pd.crosstab(y, X.iloc[:,i])
            table = (table/table.sum()).iloc[1,:]
            (table.T).sort_index().plot(kind='bar', alpha=0.8, ax=ax, color=colors[i % len(colors)])
            
            ax.set_title(labels[i])
            ax.set_ylabel('')
            ax.set_xlabel('')
        else:
            fig.delaxes(ax)

    sns.despine()
    plt.tight_layout()
    
    return fig, axes


from sklearn.calibration import calibration_curve


def plot_calibration_curves(y_true, y_prob, labels=None):
    
    fig, ax = plt.subplots(figsize=(9,6))
    
    if y_prob.ndim==1:
        prob_true, prob_pred = calibration_curve(y_true, y_prob, n_bins=10)
        if labels:
            ax.plot(prob_pred, prob_true, label=labels)
    else: 
        m = y_prob.shape[1]
        for i in range(m):
            prob_true, prob_pred = calibration_curve(y_true, y_prob[:,i], n_bins=10)
            if labels:
                ax.plot(prob_pred, prob_true, label=labels[i])
            else:
                ax.plot(prob_pred, prob_true)
    
    ax.plot([0,1],[0,1], linestyle='--', color='black', alpha=0.5)

    ax.set_xlabel('Estimated probability')
    ax.set_ylabel('Empirical probability')
    if y_prob.ndim==1:
        ax.set_title('Reliability curve', fontsize=14)
    else:
        ax.set_title('Reliability curves', fontsize=14)
    ax.set_xlim(0,1)
    ax.set_ylim(0,1)
    plt.legend(fontsize=13, frameon=False)
    sns.despine()
  
    return fig, ax

#! #################### Data processing  start ###########################

## outliers
# def dp_outliers(X,skew_threshold = 3,fit_test = False, X_test = None):
    
#     from sklearn.preprocessing import RobustScaler
    
#     skewed_var = X.skew()[abs(X.skew())>skew_threshold].index
#     transformer = RobustScaler()
#     result_train = transformer.fit_transform(X[skewed_var])
#     if fit_test:
#         result_test = transformer.transform(X_test[skewed_var])
        
#         return result_train, result_test, skewed_var
    
#     return result_train, skewed_var

def dp_outliers_IQR(X_train, skew_threshold = 3, fit_test = False, X_test = None):
    
    skewed_var = X_train.skew()[abs(X_train.skew())>skew_threshold].index
    X_train = X_train[skewed_var]
    
    q_low = X_train.quantile(q = 0.05)
    q_high = X_train.quantile(q = 0.95)
    
    for i in range(len(skewed_var)):
    
        df = X_train[skewed_var[i]]
        df = df.mask(df<q_low.iloc[i],q_low.iloc[i])
        df = df.mask(df>q_high.iloc[i],q_high.iloc[i])
        X_train[skewed_var[i]] = df
        
    if fit_test:
        X_test = X_test[skewed_var]
        
        for i in range(len(skewed_var)):
                
            df = X_test[skewed_var[i]]
            df = df.mask(df<q_low.iloc[i],q_low.iloc[i])
            df = df.mask(df>q_high.iloc[i],q_high.iloc[i])
            X_test[skewed_var[i]] = df
                
        return X_train, X_test, skewed_var
    
    return X_train, skewed_var

# variable sparsity
def dp_sparsity2other(X_train, freq_threshold = 10, values = 'Others', fit_test = False, X_test = None):

    vals = X_train.value_counts()[X_train.value_counts()>freq_threshold].index
    # ignore the missing value
    X_train[~(X_train.isin(vals) | X_train.isna())] = values
    
    if fit_test:
        X_test[~(X_test.isin(vals) | X_test.isna())] = values
        return X_train, X_test, vals

    return X_train, vals

# numerical missing value imputation
def dp_mv_imputation(X_train, fit_test = False, X_test = None):
# only for numerical columns
    from sklearn.experimental import enable_iterative_imputer
    from sklearn.impute import IterativeImputer

    imp_mean = IterativeImputer(random_state=0)

    X_train.iloc[:] = imp_mean.fit_transform(X_train)
    if fit_test:
        X_test.iloc[:] = imp_mean.transform(X_test)
        return X_train, X_test
    
    return X_train,

def dp_mv_DropCols(data,alpha:float):
    '''
    data: pd.Dataframe
    alpha: missing level for dropping a columns 
    '''
    # drop columns with high proportion of missing values
    ms_col = data.isna().sum()[data.isna().sum()>data.shape[0]*alpha].index
    data = data.drop(ms_col,axis=1)
    
    return data


#! #################### Data processing end ###########################