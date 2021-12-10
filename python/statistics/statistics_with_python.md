# Statistics and regression with Python

## Learning objectives

 * How to compute measures of central tendency and dispersion in Python
 * How to calculate single- and two-sample tests in Python
 * Correlation and how to calculate it in Python
 * How to create a regression model
 * How to interpret the output of a regression model
 * How to interpret the coefficients of a regression model
 * How to test hypotheses with a regression model

## Summary statistics in Python

We talked previously about measures of central tendency and dispersion, as well as about single- and two-sample hypothesis testing [here](../../sheets/lessonstats/stats.md). Now, we'll look at how to calculate these in Python, and then dive once more into some statistics content, with a focus on _data modelling_. 

Let's open up Python (via Jupyter notebook, Spyder, or just a console window) and load the [automobile data](./assets/auto-mpg.data?raw=true). This data comes in an archaic format called a _fixed width file_, where every column has the same width, and is padded by spaces where necessary. Fortunately, pandas has a `read_fwf` function that is well-suited to open this type of file (the other functions we've seen don't support fixed width files). Looking at the [documentation](https://pandas.pydata.org/docs/reference/api/pandas.read_fwf.html), we just need to specify the width of each column. We can also take a quick look at the metadata [here](./assets/auto-mpg.names) to see the column names. Based on the above, let's use the following code to load this data:

```python
import numpy as np
import pandas as pd

widths = [7, 4, 10, 10, 11, 7, 4, 4, 30]
df = pd.read_fwf('./assets/auto-mpg.data', widths=widths, header=None)
df.columns = ['mpg', 'cylinders', 'displacement', 'horsepower', 'weight', 'acceleration', 'model year', 'origin', 'car name']

df.head()
```

```
    mpg  cylinders  ...  origin                     car name
0  18.0          8  ...       1  "chevrolet chevelle malibu"
1  15.0          8  ...       1          "buick skylark 320"
2  18.0          8  ...       1         "plymouth satellite"
3  16.0          8  ...       1              "amc rebel sst"
4  17.0          8  ...       1                "ford torino"
```

Besides column names, the metadata also tells us that `horsepower` has six missing values. We can use, for instance, `pd.unique` to find that the missing values are represented by `?`. Let's replace this with the `np.nan` to better represent our missing values, and convert every value to be numeric.

```python
df['horsepower'].replace('?', np.nan, inplace=True)
df['horsepower'] = pd.to_numeric(df['horsepower'])
```

Calculating some summary statistics can often be a good first step in an exploratory analysis. With this in mind, we'll take a look at two ways we can do this: using the `statistics` library, or using built-in dataframe methods. We'll cover the strengths and weaknesses of both of these shortly, but for now, let's import the statistics library with an alias. Using an alias will make the library easier to reference, and our code will be a bit more legible:

```python
import statistics as st
```

The statistics library gives us access to common statistics functions, such as those for calculating averages and variance. Reading through the documentation [here](https://docs.python.org/3/library/statistics.html), we see that most functions work on sequences or iterables. Let's investigate the `mpg` of the vehicles in our dataframe. 

```python
print(f"Mean of mpg: {st.mean(df['mpg'])}\nMedian of mpg: {st.median(df['mpg'])}\nMode of mpg: {st.mode(df['mpg'])}")
print(f"Standard Deviation of mpg: {st.stdev(df['mpg'])}")
```

```
Mean of mpg: 23.514572864321607
Median of mpg: 23.0
Mode of mpg: 13.0
Standard Deviation of mpg: 7.8159843125657815
```

**Question:** Which average do you think best represents the cars in this dataset?

Let's continue to look at averages, but this time for the `horsepower` column. 

```python
st.mean(df['horsepower'])
```

```
nan
```

Wait a second — what just happened? Remember that we replaced our missing values with `np.nan`. The `statistics` library is general; that is, it is designed to calculate statistical measures for a wide variety of data types (not just dataframes or NumPy arrays), but this also means it isn't well-equipped to deal with `NaN` values. Fortunately, our data is in a dataframe, which means pandas probably makes these calculations easy for us! In fact, every dataframe or series comes with built-in methods to calculate basic summary statistics. Recall the syntax for calling methods: `my_object.method(arguments)`. Let's see how these methods deal with missing values.

```python
df['horsepower'].median()
```

```
93.5
```

We get an actual value out! The built-in pandas methods ignore missing values, so as long as the missing values appear randomly (without any bias), then these are fine to use. These methods are also built on top of NumPy methods, so they are more efficient and should be used whenever possible. Alternatively, the NumPy library itself makes several statistical functions available — the documentation can be found [here](https://numpy.org/doc/stable/reference/routines.statistics.html). Let's look at the standard deviation of `horsepower`, this time using NumPy:

```python
np.std(df['horsepower'])
```

```
38.442032714425984
```

Let's try again using the built-in pandas method:

```python
df['horsepower'].std()
```

```
38.49115993282855
```

Wait a second — these numbers aren't quite the same. What's going on? It's important to be aware of the slight differences in the functions we use, especially when it comes to functions that are mathematical in nature. The built-in pandas methods assume we're calculating the _sample standard deviation_. Because we calculate the sample mean to do this, we lose a degree of freedom. This is represented in how we normalize our data, by dividing by the number of data points we have **minus one** (because of the lost degree of freedom). By default, NumPy calculates the _population standard deviation_ — since we aren't estimating the population mean (we can calculate it directly), we don't lose a degree of freedom, so when we normalize, we divide by the number of data points we have. If this is all a bit hazy, don't worry — you can refer back to our previous statistics content [here](../../sheets/lessonstats/stats.md). 

Since we almost never have data for the full population, it makes sense to use the sample standard deviation (the statistics library standard deviation function, `st.stdev()`, also calculates sample standard deviation). In other words, use the built-in pandas method for calculating standard deviation, or use the the NumPy function and set `ddof=1`, to specify that we need to subtract one degree of freedom when normalizing. 

## Hypothesis testing in Python

Here, we'll go over hypothesis testing in Python. If the principles of hypothesis testing are a bit hazy, refer back to [this lesson](../../sheets/lessonstats/stats.md). The main idea behind hypothesis testing is that we are comparing one group against an expected value, or one group against another. When we perform a hypothesis test, we are returned a p-value, which we compare to a threshold we've set before carrying out the test. If the p-value is less than our threshold, we reject the null hypothesis. 

In sheets, we calculated the p-values for a single sample z-test, and a two-sample t-test. Here, we'll focus on using single- and two-sample t-tests. Why? The t-test is more generally applicable than a z-test. For a t-test, we don't need to know the population standard deviation, and for large samples, the t-test and z-test produce nearly identical results. Since most of the data we'll be working with in Python will be very large, it suffices to know only the t-test.

We'll use the [SciPy package](https://www.scipy.org) for our statistical testing. If you don't have it installed already, run `pip install scipy` in a terminal. Let's import the two functions we'll be using:

```python
from scipy.stats import ttest_1samp, ttest_ind
```

### Single-Sample T-Test

To perform a single-sample t-test, we need some data, and the (population) mean we want to compare it against. The documentation for `ttest_1samp` can be found [here](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.ttest_1samp.html). There are two important keyword-arguments to which we should pay attention. First, `nan_policy` gives options on how to handle missing values in data: return `NaN`, raise an error, or ignore. Second, `alternative` lets us specify whether the alternative hypothesis is `two-sided`, `less` (that is the alternative claims that the data mean is less than the assumed population mean), or `greater`. 

A report on automobiles in 1980 claims that the average vehicular horsepower is 100. Let's examine this claim more closely using our data. Since we have `NaN` values in the horsepower data, we should set `nan_policy='omit'`. Let's set our type I error rate threshold to 0.05. Looking at the documentation, this function returns a _t-statistic_ and a p-value. We don't have to worry about the t-statistic, but we'll focus, as always, on the p-value. 

```python
ttest_1samp(df['horsepower'], 100, nan_policy='omit', alternative='two-sided')
```

```
Ttest_1sampResult(statistic=2.298952877938673, pvalue=0.022034213588036713)
```

Our p-value is less than our rejection threshold, so we reject the null hypothesis, and conclude that the mean vehicular horsepower is not 100. 

### Two-Sample T-Test

To perform a two-sample t-test, we need two distinct samples of data. We'll use `ttest_ind`, with documentation [here](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.ttest_ind.html). `ttest_ind` has the `nan_policy` and `alternative` keyword arguments, like `ttest_1samp`, but we also have one more important keyword-argument here: `equal_var`, which can be `True` or `False`. If `True`, we assume that both samples have equal variance. We often don't know whether this is the case or not, in which case it's safer to set it to `False`. Like `ttest_1samp`, `ttest_ind` returns a test statistic (which we can ignore) and a p-value. 

Let's find out whether we can fool the t-test or not. We'll separate our `displacement` column into two random samples and compare them against each other using `ttest_ind`. 

```python
sample1 = df['displacement'].sample(frac=0.5)
sample2 = df[~df.index.isin(sample1.index)]['displacement']

ttest_ind(sample1, sample2)
```

```
Ttest_indResult(statistic=-0.7011737198138793, pvalue=0.4836064290819272)
```

Your output will differ since we are taking a random sample without a specified seed. Our p-value is very high, as we would hope — a low p-value would mean that we were close to tricking the t-test! But let's think about how unrealistic that is for a moment. If our type I error rate threshold is 0.05, this means that if we took an infinite number of samples, we would reject the null hypothesis (in this case, that the groups are the same) 5% of the time, or one in twenty tests. Did anyone get a p-value of less than 0.05? 

We reiterate that the type I error rate threshold specifies how much trust we can associate with a test when we reject the null hypothesis. For an extremely important claim, we will then set a much lower threshold. For example, if we were testing whether drug B is more effective than the traditionally prescribed drug A for arrhythmias, and drug B was significantly more expensive to manufacture, we might want be very, very sure that B is indeed more effective. Thus, we might require a p-value of 0.001 instead of the typical 0.05. 

## Correlation and causation

Smoking **causes** lung cancer. A **link** has been established between lack of sleep and Alzheimer's disease. What's the difference between these two statements? The first statement implies _causality_, while the second implies _correlation_. _Causation_ or causality means that B is a direct result of A by some observed or provable mechanism. _Correlation_, on the other hand, is just a claim that A and B tend to relate in a predictable, linear fashion. For example, chewing gum sales might be correlated with cigarette sales, since smokers often use gum to freshen their breath. However, it would be absurd to claim that buying gum causes smoking, or buying cigarettes causes one to buy gum. 

Using statistics, we cannot show or prove relationships of a causal nature (this is why we reject the null hypothesis, instead of accepting the alternative hypothesis). We can, however, quantify the correlation between two continuous variables. Let's suppose we have pairs <img src="https://render.githubusercontent.com/render/math?math=\color{grey}{(x_i, y_i)}" alt="(x_i, y_i)">. Then, denoting the means of each sample with bars, we state the (Pearson) correlation between *X* and *Y* as

![pearson correlation formula](./assets/correlation.png)

This formula returns a value between -1 and 1, which measures how much the pairs <img src="https://render.githubusercontent.com/render/math?math=\color{grey}{(x_i, y_i)}" alt="(x_i, y_i)"> tend to vary with each other (linearly). For example, if the correlation is close to 1, then if <img src="https://render.githubusercontent.com/render/math?math=\color{grey}{x_i}" alt="x_i"> is high, then <img src="https://render.githubusercontent.com/render/math?math=\color{grey}{y_i}" alt="y_i"> is likely high as well. Conversely, if the correlation is close to -1, then if <img src="https://render.githubusercontent.com/render/math?math=\color{grey}{x_i}" alt="x_i"> is high, then <img src="https://render.githubusercontent.com/render/math?math=\color{grey}{y_i}" alt="y_i"> is likely low. In this case, we say that <img src="https://render.githubusercontent.com/render/math?math=\color{grey}{X, Y}" alt="X, Y"> are inversely (or negatively) correlated.

Correlation with an absolute value between 0.3–0.5 is considered weak correlation; values between 0.5–0.8 is considered medium correlation; and values higher than that are considered strong correlation. However, correlation, no matter how strong, is never as strong as causation. In fact, there is a term for correlations between variables that are not causally related: _spurious_. Here's a great example of a spurious correlation, despite an extremely strong correlation:

![per capita consumption of mozzarella cheese correlates with civil engineering doctorates awarded, r=0.96](./assets/spurious_correlation.png)

This figure comes from [this website](https://www.tylervigen.com/spurious-correlations), which contains 30,000 more examples of (very amusing) spurious correlations. 

## Linear regression

Despite variables not being causally related, we can still use correlated variables to predict the value of another variable. We mentioned that if variable *X* was correlated with variable *Y*, then if *X* is high, it is likely *Y* will be high as well. Let's think about this more visually. If variables are positively correlated, they tend to increase (linearly) together. See the following figure:

![example of linear regression in two dimensions](./assets/regression.png)

As the *x* values increase, the *y* values of the points in the figure do as well. If you were asked to draw the best fitting line through this point cloud, hopefully you'd draw the red line in the figure. Intuitively, it makes sense to us that this line fits the best, but how do we quantify this mathematically?

![regression with distance of points to regression line](./assets/regression_errors.jpg)

The regression line produces a "best guess" for where a point will be on the y-axis, based on where it is on the x-axis. In our first regression figure, if we look at <img src="https://render.githubusercontent.com/render/math?math=\color{grey}{x%3D20}" alt="x equals twenty">, we see our regression line would produce a "guess" <img src="https://render.githubusercontent.com/render/math?math=\color{grey}{y%3D8}" alt="y equals eight">. If we look at the distance on the y-axis from any point to the regression line, we see how far the regression "guess" is from the actual data. This gives us the notion of _error_. The error associated with a regression line is high if it is far from all the data points. Given an <img src="https://render.githubusercontent.com/render/math?math=\color{grey}{x_i}" alt="x_i">, our regression line *L* gives us a prediction <img src="https://render.githubusercontent.com/render/math?math=\color{grey}{L(x_i)%3D\hat{y_i}}" alt="L(x_i)%3D hat(y_i)">. We can then define the error between a single point and its prediction from the regression line as <img src="https://render.githubusercontent.com/render/math?math=\color{grey}{E_i%3D(y_i - \hat{y_i})^2}" alt="squared difference between y_i and y_i hat">. The total error associated with points of data and a regression line is simply the sum of all these individual errors, <img src="https://render.githubusercontent.com/render/math?math=\color{grey}{E%3D\sum_i E_i}" alt="E%3D sum of E_i">. 

Why do we square the difference between the actual value and the regression prediction? We want all error terms to have the same sign, and squaring achieves this (the square of a negative number is positive). Also, it means points very far from the regression line will contribute even larger error terms, enforcing that the regression line should fit well between all points (versus fitting extremely well to some at the cost of poorly fitting to others). 

With all this in mind, what is the "best fitting" regression line through some points? Well, it is the line with the least error! Fortunately, we don't have to calculate this manually, since regression is a well-studied problem with many implementations. However, the interested student can find more information on how to optimize a linear regression model, along with some great visuals, [here](https://www.cs.cmu.edu/~mgormley/courses/10601-s17/slides/lecture7-opt.pdf). Note that technically, there are two ways in which a linear regression model can be optimized, but the linked method is more general. The other method is [ordinary least squares](https://en.wikipedia.org/wiki/Ordinary_least_squares), but can run into some numerical issues. 

We aren't limited to regression with two variables. We can probably imagine fitting a line in three dimensions, but the beautiful thing about math is that we aren't limited to our geometric intuition! We can fit a regression line in *N* dimensions, to predict a value in the *(N+1)*st dimension. This might seem a bit weird at first, but let's look at an example! 

### Using Regression to Predict `mpg`

We'll use the dataset we currently have loaded. One column of interest is `mpg`, which summarizes how fuel-efficient a vehicle is. Let's fit a regression model to predict `mpg`, by using the columns `cylinders`, `displacement`, `horsepower`, `weight`, `acceleration`, `model year`. But first, let's make sure that it makes sense to create a regression model. Pandas has a built-in method to calculate correlations between sets of variables. Let's isolate a few of the above columns and see how they correlate to `mpg`:

```python
regression_data = df[['mpg', 'cylinders', 'displacement', 'horsepower', 'weight', 'acceleration', 'model year']]
regression_data[['mpg', 'cylinders', 'displacement']].corr()
```

```
                   mpg  cylinders  displacement
mpg           1.000000  -0.775396     -0.804203
cylinders    -0.775396   1.000000      0.950721
displacement -0.804203   0.950721      1.000000
```

Let's break down this output a little. Each entry in the matrix corresponds to the correlation between the labelled row and the labelled column. For example, the entry in the first row and second column is the correlation between `mpg` and `cylinders`. Correlation is symmetric, so the correlation between *X* and *Y* is the same as the correlation between *Y* and *X*. Therefore, we only need to look at the top or bottom half of the values in the matrix above. Also, variables have perfect correlation with themselves. The most relevant information for us is the correlation between `mpg` and `cylinders`, and `mpg` and `displacement`. Notice that both of these are moderately or highly negatively correlated. This makes sense to us, since more powerful cars tend to have worse fuel-efficiency. These high correlations also tell us that a linear regression model could be useful here. Let's go ahead and create one. To do so, we need to specify the _dependent variable_ (the variable that defines the error, otherwise known as the variable we want to predict) and the _independent variables_ (the data we use to make our predictions). 

We'll use the linear regression class available from `statsmodels`, with documentation [here](https://www.statsmodels.org/stable/regression.html). This model is a _class_, which means it must be instantiated before we can take advantage of its built-in methods. Most of the modelling tools we'll see in the future are also built as classes, so it would be best to remember the general flow of creating the linear regression model. 

```python
import statsmodels.api as sm

#for now, we remove all missing values
regression_data = regression_data[~regression_data['horsepower'].isna()]

dependent_vars = regression_data['mpg']
independent_vars = regression_data[['cylinders', 'displacement', 'horsepower', 'weight', 'acceleration', 'model year']]
independent_vars['constant'] = np.ones((independent_vars.shape[0],)) #add a constant column for the regression, more on this later

#make sure all our data is numeric
dependent_vars = dependent_vars.apply(float)
independent_vars = independent_vars.applymap(float)

#create our linear regression class, with our data
lin_reg = sm.OLS(dependent_vars, independent_vars)
reg_results = lin_reg.fit() #fit the model to the data using the fit method
print(reg_results.summary())
```

```
                            OLS Regression Results                            
==============================================================================
Dep. Variable:                    mpg   R-squared:                       0.809
Model:                            OLS   Adj. R-squared:                  0.806
Method:                 Least Squares   F-statistic:                     272.2
Date:                Fri, 20 Aug 2021   Prob (F-statistic):          3.79e-135
Time:                        09:38:36   Log-Likelihood:                -1036.5
No. Observations:                 392   AIC:                             2087.
Df Residuals:                     385   BIC:                             2115.
Df Model:                           6                                         
Covariance Type:            nonrobust                                         
================================================================================
                   coef    std err          t      P>|t|      [0.025      0.975]
——————————————————————————–
cylinders       -0.3299      0.332     -0.993      0.321      -0.983       0.323
displacement     0.0077      0.007      1.044      0.297      -0.007       0.022
horsepower      -0.0004      0.014     -0.028      0.977      -0.028       0.027
weight          -0.0068      0.001    -10.141      0.000      -0.008      -0.005
acceleration     0.0853      0.102      0.836      0.404      -0.115       0.286
model year       0.7534      0.053     14.318      0.000       0.650       0.857
constant       -14.5353      4.764     -3.051      0.002     -23.902      -5.169
==============================================================================
Omnibus:                       37.865   Durbin-Watson:                   1.232
Prob(Omnibus):                  0.000   Jarque-Bera (JB):               60.248
Skew:                           0.630   Prob(JB):                     8.26e-14
Kurtosis:                       4.449   Cond. No.                     8.53e+04
==============================================================================

Warnings:
[1] Standard Errors assume that the covariance matrix of the errors is correctly specified.
[2] The condition number is large, 8.53e+04. This might indicate that there are
strong multicollinearity or other numerical problems.
```

Wow, this is a lot of information! Let's take it in stride. The first line tells us the dependent variable is `mpg` — this is good, since we wanted to produce "guesses" for `mpg` based on the other variables. The second column in the first line tells us about something called _R-squared_. The R-squared, or R2, score tells us how much variance in the dependent variable our model captures based on the independent variables we've given. It ranges from 0 to 1, and a higher R2 score is (usually) better. When we use a lot of variables, we should instead pay attention to the adjusted R2 score (the second row, second column in our table) — this better represents how well the model is doing. In our case, the two are still very similar, and it looks like we have a strong model. We care about one more value, labelled `Prob (F-statistic)`. This is the p-value for _significance of regression_ — whether our model is legitimately capturing information about `mpg` or not. Since it's incredibly small, we know that we're capturing something of interest in the model. The rest of the sections in the first part of the table aren't that important to us.

Let's look at the second part of the table. We see the independent variables that we've fed into the model: `cylinders`, `displacement`, `horsepower`, `weight`, `acceleration`, `model year`, `constant`. These are the rows in the second part of the table, with columns `coef`, `std err`, `t`, `P>|t|`, `[0.025`, `0.975]`. To understand this part of the table, we have to more fully understand what a regression line is. 

Remember that the equation of a line in two dimensions is <img src="https://render.githubusercontent.com/render/math?math=\color{grey}{y%3Dmx%2Bb}" alt="y equals mx plus b">. In the regression figures we saw above, the regression line is given by this equation. *m* is the _slope_ of the line — in other words, if *x* increases by one unit, *y* will increase by *m* units. *b* is the _intercept_, which tells us the "default" value for *y* when *x* is zero. To get *b*, we needed to add the `constant` column. We aren't working in two dimensions, but the two-dimensional case gives us some good intuition for the multi-dimensional case! 

The equation for a line looks similar in multiple dimensions: <img src="https://render.githubusercontent.com/render/math?math=\color{grey}{y%3Dm_1x_1%2Bm_2x_2%2B%5Ccdots%2Bm_Nx_N%2Bb}" alt="y equals m_1x_1 plus m_2x_2 plus dots plus m_Nx_N plus b">. Instead of just one slope, we have one _coefficient_ attached to each of our independent variables (the *x*s). The interpretation of these coefficients is slightly different in this case. Assuming **all other variables stay the same**, if <img src="https://render.githubusercontent.com/render/math?math=\color{grey}{x_i}" alt="x_i"> increases by one unit, then *y* will increase by <img src="https://render.githubusercontent.com/render/math?math=\color{grey}{m_i}" alt="m_i"> units. We still have just one *b*, but this time, it represents the default value of *y* when each of our independent variables are zero. 

The first column of the table above gives us the value of each <img src="https://render.githubusercontent.com/render/math?math=\color{grey}{m_i}" alt="m_i">, in the `coef` column. For example, the coefficient for weight is -0.0064. In other words, assuming all other attributes of a vehicle remained the same, if it went up one pound in weight, we would estimate the miles per gallon to decrease by 0.0064.

We'll ignore all other columns of the output, except for the `P>|t|` column. This is just a fancy name for something we're familiar with already: a p-value! But why would we want p-values for each coefficient in a regression model? We are implicitly running a hypothesis test with the null hypothesis "this coefficient equals zero." If the coefficient is equal to zero, then it can be removed from the model! Otherwise, we reject the null hypothesis, and conclude that the coefficient does not equal zero. If the coefficient doesn't equal zero, then it is contributing meaningful information to the model (based on the other coefficients present in the model). Technically, this is a _marginal_ test, since the test result depends in part upon the other coefficients in the model. That means we should be careful when we decide on what variables to remove from the model. Looking at the above, and deciding to use a threshold of 0.05, we can definitely keep the variables `weight`, `model year`, `constant`. But should we remove all the other variables? Probably not — since, for example, `displacement` and `horsepower` are related, it's likely that removing one will make the other more significant. Since `horsepower` seems pretty unhelpful, we'll remove it, as well as `cylinders` and `displacement` (since it is related to acceleration). 

```python
indep2 = independent_vars[['weight', 'acceleration', 'model year', 'constant']]

lin_reg2 = sm.OLS(dependent_vars, indep2)
regression2 = lin_reg2.fit()

print(regression2.summary())
```

```
                            OLS Regression Results                            
==============================================================================
Dep. Variable:                    mpg   R-squared:                       0.809
Model:                            OLS   Adj. R-squared:                  0.807
Method:                 Least Squares   F-statistic:                     546.5
Date:                Fri, 20 Aug 2021   Prob (F-statistic):          6.91e-139
Time:                        09:55:10   Log-Likelihood:                -1037.1
No. Observations:                 392   AIC:                             2082.
Df Residuals:                     388   BIC:                             2098.
Df Model:                           3                                         
Covariance Type:            nonrobust                                         
================================================================================
                   coef    std err          t      P>|t|      [0.025      0.975]
——————————————————————————–
weight          -0.0066      0.000    -28.502      0.000      -0.007      -0.006
acceleration     0.0664      0.070      0.943      0.346      -0.072       0.205
model year       0.7484      0.050     14.860      0.000       0.649       0.847
constant       -14.9366      4.056     -3.683      0.000     -22.910      -6.963
==============================================================================
Omnibus:                       38.841   Durbin-Watson:                   1.222
Prob(Omnibus):                  0.000   Jarque-Bera (JB):               61.678
Skew:                           0.645   Prob(JB):                     4.04e-14
Kurtosis:                       4.454   Cond. No.                     7.26e+04
==============================================================================

Warnings:
[1] Standard Errors assume that the covariance matrix of the errors is correctly specified.
[2] The condition number is large, 7.26e+04. This might indicate that there are
strong multicollinearity or other numerical problems.
```

Looking at p-values again, it seems like we could remove acceleration from the model as well! However, it doesn't quite make sense that only `model year`, `weight`, and a constant value are good predictors for `mpg`. In this case, we might think about what else we could include in this data to improve our predictive power. 

Let's use this model to predict the `mpg` of a pretty average vehicle. To do so, we need to feed in values for `weight`, `acceleration`, `model year`, and a 1 for `constant`. We'll use the mean values for `weight`, `acceleration`, and `model year`, and the built-in method `predict`.

```python
regression2.predict([2970, 16, 76, 1])
```

```
array([21.912132])
```

Our estimated value is in a believable range (for example, the actual mean of `mpg` in our data is 23.5). That's a good sanity check! This data is pretty old, though, and we're pretty advanced. Cars are lighter and faster, and the years have gone by. Let's try predicting `mpg` values for more updated vehicles. 

```python
regression2.predict([1000, 25, 120, 1])
```

```
array([66.17587711])
```

Hang on — 66 miles per gallon seems like a car manufacturer's dream claim. What's going on? When we're modelling data and making predictions, we need to be very careful about how we _extrapolate_ — make predictions on ranges of data outside our original dataset. Of course, if we limited ourselves to _interpolating_ (making predictions on data strictly inside the range of our original dataset), data modelling wouldn't be very useful. So where does extrapolation break down? Well, in this case, looking at the `model year` column in our dataset, all the cars are designed between 1970 and 1982. Furthermore, the weights range from about 1600 to 5100 pounds. Based on this information, we're predicting with drastically different data. There's no universal rule on when extrapolation falls apart, but in general, the closer we stay to our original data, the more accurate our predictions will be. 

### Exercises

Concrete is one of the most important materials in civil engineering. Of particular interest is its _compressive strength_, which is known to be highly nonlinear. Technically, this means that linear regression is not a good candidate for modelling, but let's test the limits of linear regression in this exercise.

1. Load this [`concrete.data`](./assets/concrete.data?raw=true) file into Python. The metadata for the file is [here](./assets/concrete.names?raw=true). You may want to replace the columns: `df.columns = ['kg/mixture', 'slag', 'fly ash', 'water', 'superelasticizer', 'coarse aggregate', 'fine aggregate', 'age', 'compressive strength']`.
1. Try to get an idea of what each column in the data looks like, by using the statistical functions we covered above. We are trying to predict the compressive strength.
1. Investigate whether variables are correlated with each other. Based on correlation, does this dataset look like a good candidate for regression modelling?
1. Separate the data into dependent and independent variables. Add a `constant` column to the independet variables. Fit a regression model to the data and print out the summary.
1. Is the regression model significant? Are each of the coefficients significant? Remove the least significant coefficient and re-fit the model.
1. Are the new coefficients all significant? 
1. Use the fitted model to predict compressive strength for different values of the independent variables. Use both values that make sense based on those in the data, and values that don't. How does prediction quality break down?
