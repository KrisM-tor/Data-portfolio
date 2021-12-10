# Data Manipulation with Pandas: Part I

## Student Takeaways

By the end of this lesson, the student should know:

* How to access indices and columns of a dataframe
* How to access specific rows and columns using `loc` and `iloc`
* How to access data meeting specific criteria
* How to work with missing values

Here, we introduce some methods for cleaning data using pandas. We'll work with the `adult.data` file we saw in the previous lesson once again. Let's start up Python and load it like we did previously:

```python
import pandas as pd

df = pd.read_csv('./assets/adult_census/adult.data', header=None)
```

In the `read_csv()` call we've provided a value of `None` for the keyword argument `header`, `header=None`, to say that the `csv` file being read doesn't contain column names. This results in pandas identifying our columns as numbers. However, as this isn't very descriptive, it's considered bad practice. Our column names should always reflect what is contained in our data. But how do we know what each column contains? Often, datasets come with _metadata_ — data about data (in our case, data about what the dataset contains). Let's read through the `adult.names` metadata file available in the course module repository. 

The first few lines of the file tell us where the data came from, as well as some information about the distribution of the `income` field and some information about using it as a predictive task. At the very bottom, we are given the column names. Let's use these names as the columns for our dataframe.

## Accessing indices and columns

Every dataframe has two key components: the index, which is how any row in a dataframe can be accessed (and as such, an index should be unique, otherwise it is more expensive to access data); and the columns, which label every field in a row. When pandas cannot detect an index, it just creates an index starting from 0 to <img src="https://render.githubusercontent.com/render/math?math=\color{grey}n_{\text{rows}} - 1" alt="num rows minus one">. We can look at the index of our dataframe as follows:

```python
df.index
```

```
RangeIndex(start=0, stop=32561, step=1)
```

We should see that pandas has created a *RangeIndex* object for us — just the row count described above. The command to access columns is similar:

```python
df.columns
```

```
Int64Index([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14], dtype='int64')
```

In this case, our columns aren't very interesting, since pandas has just labelled them numerically for us. We can also use this command to set the columns of a dataframe, by passing in a list of new column names (this list must contain names for all columns). 

```python
df.columns = ['age', 'workclass', 'fnlwgt', 'education', 'education-num', 'marital-status', 'occupation', 'relationship', 'race', 'sex', 'capital-gain', 'capital-loss', 'hours-per-week', 'native-country', 'income']
```

Now when we use the `df.head()` command, we should see better columns:

```
Index(['age', 'workclass', 'fnlwgt', 'education', 'education-num',
       'marital-status', 'occupation', 'relationship', 'race', 'sex',
       'capital-gain', 'capital-loss', 'hours-per-week', 'native-country',
       'income'],
      dtype='object')
```

Notice that the index and columns give us a good idea of what our dataframe looks like: the index tells us how many rows, and from the column names, we can count the number of columns. This information is also encapsulated in the `shape` method:

```python
df.shape
```

```
(32561, 15)
```

The shape is always reported as <img src="https://render.githubusercontent.com/render/math?math=\color{grey}(n_{\text{rows}},n_{\text{columns}})" alt="number of rows, number of columns">; however, since this just returns a tuple, we can grab either the number of rows or number of columns specifically if we like (for instance, `df.shape[0]`).

## Accessing specific rows, columns, and values

Often, we'll want to single out a column, a few rows, or some specific values for further computation. Once again, pandas makes this easy for us. 

Let's do some investigation on the dataframe we've currently loaded into memory. One of our columns was `hours-per-week`; using this data, let's investigate the work habits of Americans a few decades ago. 

Most of our commands will look like this: `df['column name'].method(optional_args)`

First, let's check what the average number of hours worked per week is. A quick Google search tells us the average in America now is 34.4. 

```python
df['hours-per-week'].mean()
```

```
40.437455852092995
```

It looks like the number of work hours per week has gone down! However, can we think of any reasons why this might not be the case? For example, our data comes from census data, where employees self-report the hours they work. If the 34.4 hours per week is reported by employers, they might factor in breaks; where employees might not. This is a simple example, but it's very important to consider where your data comes from, and any key differences that might exist, when making comparisons!

Next, let's look at the minimum and maximum values for hours worked per week. 

```python
df['hours-per-week'].min()
```

```
1
```

```python
df['hours-per-week'].max()
```

```
99
```

There's a very big spread between these values! Just knowing the minimum, maximum, and average doesn't help us all that much. Let's use a very useful pandas function called `value_counts`. This function is like the `count + groupby` combination in SQL.

```python
hour_counts = pd.value_counts(df['hours-per-week'])
print(hour_counts)
```

```
40    15217
50     2819
45     1824
60     1475
35     1297
 
92        1
94        1
87        1
74        1
82        1
Name: hours-per-week, Length: 94, dtype: int64
```

This function returns a _series_ — essentially a dataframe but with only one column. For the most part, they work like dataframes, but they can't be used in all places dataframes can be. These places are best treated case-by-case, and when you run into such an issue, there is a very good chance that someone else has as well, so don't be afraid to do some investigation with the help of Google. Another workaround is that any series can be converted to a dataframe via `series.to_frame()`.

Let's convert our series to a dataframe with the above command: `hour_counts = hour_counts.to_frame()`. Now, we have a count associated with each number of hours worked per week, but we really can't see all that much, since Python won't print 94 rows (and even if it did, we wouldn't be able to glean all that much information from it). We still might be curious about a few rows, specifically those not too far off from the average. 

### Using `loc` and `iloc`

`loc` and `iloc` are built-in methods for accessing specific data in a dataframe. `loc` works via labels, while `iloc` works via integer indexing. Let's take a closer look, using the `hour_counts` object we created above. 

```python
hour_counts.head(10)
```

```
40    15217
50     2819
45     1824
60     1475
35     1297
20     1224
30     1149
55      694
25      674
48      517
Name: hours-per-week, dtype: int64
```

Notice the index of `hour_counts` is the number of hours worked per week, while the first (and only) column is the number of responders who worked that amount of hours. Since it is sorted by the number of responders, the index itself looks unordered. We can use `loc` to select some hours that are of interest to us.

`loc` is an attribute, so its usage will always look like `df.loc[some arguments]`. `loc` finds the given labels in the index and returns all the columns (or just the specified ones) matching those labels. The labels can be given as a single label, a list, or a slice (**NOTE:** be careful with using slices here, since contrary to almost every other slice in Python, they contain the endpoint). More information about `loc` can be found in its [documentation](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.loc.html).

#### Example: Slicing data with `loc`

Let's look at the distribution of responders around 40 hours worked per week. We'll grab every row in `hour_counts` corresponding to 35–45 hours worked per week. 

```python
hour_counts.loc[range(35, 46)]
```

```
35     1297
36      220
37      149
38      476
39       38
40    15217
41       36
42      219
43      151
44      212
45     1824
Name: hours-per-week, dtype: int64
```

We can also work with the dataframe from earlier, and specify some columns we want to be returned by `loc`. Let's suppose we want to look at rows 10–15 (because our index is just an ascending integer list, `loc` works fine here) and we want to see the columns `age`, `workclass`, `native-country`, `income`. We can achieve this with `loc` by first specifying the indices we are interested in, and then giving a list of columns to return. 

```python
df.loc[10:15, ['age', 'workclass', 'native-country', 'income']]
```

```
    age   workclass  native-country  income
10   37     Private   United-States    >50K
11   30   State-gov           India    >50K
12   23     Private   United-States   <=50K
13   32     Private   United-States   <=50K
14   40     Private               ?    >50K
15   34     Private          Mexico   <=50K
```

We can try using a slice to grab the 35–45 hours per week responders again, but we'd run into some interesting behaviour:

```python
hour_counts.loc[35:45]
```

```
Series([], Name: hours-per-week, dtype: int64)
```

We were returned an empty dataframe! Why is this? From the above, we know that there are people who worked between 35 and 45 hours per week. Here, it's crucial to remember that **`loc` works with labels, not values**. The slice above communicates to `loc` that we want every row in between the row with index label 35, and the row with index label 45. However, with some inspection, we see that 45 was the third most common answer, and 35 the fifth most common, so 45 appears before 35 in `hour_counts`; and therefore, there is no data to return. This is a good case for the sibling function to `loc`, `iloc`.

`iloc` works just like `loc`, except instead of using labels, it uses numeric indexing. That is, if we want to see the fifth through tenth rows, and only the first four columns for these rows, we would call

```python
df.iloc[5:11, :4]
```

```
    age          workclass  fnlwgt      education
5    37            Private  284582        Masters
6    49            Private  160187            9th
7    52   Self-emp-not-inc  209642        HS-grad
8    31            Private   45781        Masters
9    42            Private  159449      Bachelors
10   37            Private  280464   Some-college
```


**NOTE:** 

Unlike `loc`, `iloc` works with slices as we would expect — including the first element, but not including the last element. 

#### Example: Slicing data with `iloc`

Let's use `iloc` to grab every value included in the range 35–45. To do this, we should first sort `hour_counts` by its index, so that we grab everything in between 35 and 45 by using `iloc`.

```python 
hour_counts.sort_index(inplace=True)
```

The `inplace=True` keyword argument just tells Python to replace `hour_counts` by the `hour_counts` with sorted index object we just created (using `inplace=True` can both save memory and run faster than assigning the result to another variable). With some testing with `iloc`, we see that the 34th row corresponds to 35 hours worked, so let's grab the next 10 rows:

```python
hour_counts.iloc[34:45]
```

```
35     1297
36      220
37      149
38      476
39       38
40    15217
41       36
42      219
43      151
44      212
45     1824
Name: hours-per-week, dtype: int64
```

`loc` and `iloc` are useful, but a more natural question that might arise as part of an analysis is "do people whose native country is the United States more consistently make over 50K, compared to those from other countries?" We wouldn't be able to select suitable data using `loc` and `iloc`, unless we knew every row in the dataframe. Next, we'll look at one last (and very useful) way to select a subset of data from a dataframe. 

**NOTE:** 

Pandas has optimized operations based on indices. Therefore, when it is possible to use `loc` or `iloc`, we should opt for that!

### Selecting data via comparisons

The most general way to select data from a dataframe is by passing it an array of `True` or `False` values with the same length as the number of rows in the dataframe. This says precisely which rows we want to keep or dismiss. This may seem like a silly idea, but we can **leverage logical expressions to create these arrays**! Let's see what happens when we create a comparison using a column from a dataframe. 

```python
df['native-country'] == ' Peru'
```

```
0        False
1        False
2        False
3        False
4        False
 
32556    False
32557    False
32558    False
32559    False
32560    False
Name: native-country, Length: 32561, dtype: bool
```

Here, we ask whether each element in the `native-country` column is equal to Peru. We are returned a NumPy array of `True`/`False` values, which is exactly what we want! We can use this to select every row in the dataframe where `native-country` is equal to Peru:

```python
df[df['native-country'] == ' Peru']
```

```
       age          workclass  fnlwgt  ... hours-per-week  native-country  income
1430    49            Private  147322  ...             40            Peru   <=50K
3260    34            Private  223212  ...             40            Peru    >50K
4085    37            Private  243425  ...             50            Peru   <=50K
6794    20            Private  339588  ...             40            Peru   <=50K
6795    22            Private  206815  ...             40            Peru   <=50K
8110    41            Private  202980  ...              4            Peru   <=50K
9665    41            Private  162189  ...             40            Peru   <=50K
10312   48            Private  280422  ...             25            Peru   <=50K
10360   41   Self-emp-not-inc  254818  ...             40            Peru   <=50K
11374   44            Private  155701  ...             38            Peru   <=50K
13017   27            Private  506436  ...             40            Peru   <=50K
13129   49            Private  200949  ...             38            Peru   <=50K
13227   69            Private  174474  ...             28            Peru   <=50K
13699   24            Private  333505  ...             40            Peru   <=50K
14129   48   Self-emp-not-inc  247294  ...             30            Peru   <=50K
18154   29            Private  439263  ...             35            Peru   <=50K
19253   17                  ?  198797  ...             20            Peru   <=50K
21823   33            Private  319422  ...             60            Peru   <=50K
24531   46            Private  551962  ...             50            Peru   <=50K
24637   23            Private  481175  ...             24            Peru   <=50K
24739   17            Private  165918  ...             20            Peru   <=50K
24827   26          Local-gov  273399  ...             40            Peru   <=50K
24853   18            Private  173585  ...             15            Peru   <=50K
26372   41            Private  176452  ...             40            Peru   <=50K
27344   30            Private  437825  ...             20            Peru   <=50K
28357   35            Private  244803  ...             40            Peru   <=50K
28634   41            Private  176452  ...             40            Peru   <=50K
28895   33            Private  405913  ...             40            Peru    >50K
30189   64            Private  153894  ...             40            Peru   <=50K
30520   21            Private  502837  ...             40            Peru   <=50K
31948   25            Private  130513  ...             40            Peru   <=50K

[31 rows x 15 columns]
```

Let's break down the call above. We use the logical expression we created above to pass in an array of `True`/`False` values to the dataframe within the square brackets: `df[right here]`. Based on this array, pandas knows which rows to return: exactly those with the `native-country` field equalling Peru. Recall that we can also use this syntax to select columns from a dataframe: `df[column name or list of column names]`. We can combine selecting rows and columns to grab exactly what we want from a dataframe. Let's look at education level, income, and work hours per week for those people whose native country is Peru: 

```python
peru_data = df[df['native-country'] == ' Peru'][['education', 'income', 'hours-per-week']]
print(peru_data)
```

```
           education  income  hours-per-week
1430       Assoc-voc   <=50K              40
3260       Bachelors    >50K              40
4085         HS-grad   <=50K              50
6794         HS-grad   <=50K              40
6795         HS-grad   <=50K              40
8110         HS-grad   <=50K               4
9665         HS-grad   <=50K              40
10312   Some-college   <=50K              25
10360        Masters   <=50K              40
11374        7th-8th   <=50K              38
13017   Some-college   <=50K              40
13129           10th   <=50K              38
13227           10th   <=50K              28
13699        HS-grad   <=50K              40
14129        HS-grad   <=50K              30
18154        HS-grad   <=50K              35
19253           11th   <=50K              20
21823   Some-college   <=50K              60
24531        HS-grad   <=50K              50
24637   Some-college   <=50K              24
24739           11th   <=50K              20
24827   Some-college   <=50K              40
24853           11th   <=50K              15
26372        HS-grad   <=50K              40
27344      Bachelors   <=50K              20
28357        HS-grad   <=50K              40
28634        HS-grad   <=50K              40
28895   Some-college    >50K              40
30189      Bachelors   <=50K              40
30520        HS-grad   <=50K              40
31948     Assoc-acdm   <=50K              40
```

It looks like a lot of people who come from Peru do not make more than 50000 per year. We'll do a more thorough analysis on this later, but as an exercise, let's consider how we can use data to instigate meaningful change.

We can create other logical statements depending on the type of data with which we're working. For instance, we can select those individuals with capital gain as follows:

```python
df[df['capital-gain'] > 0]
```

```
       age          workclass  fnlwgt  ... hours-per-week  native-country  income
0       39          State-gov   77516  ...             40   United-States   <=50K
8       31            Private   45781  ...             50   United-States    >50K
9       42            Private  159449  ...             40   United-States    >50K
59      30            Private  188146  ...             40   United-States   <=50K
60      30            Private   59496  ...             40   United-States   <=50K
   ...                ...     ...  ...            ...             ...     ...
32515   66        Federal-gov   47358  ...             40   United-States   <=50K
32518   57          Local-gov  110417  ...             40   United-States    >50K
32538   38            Private  139180  ...             45   United-States    >50K
32548   65   Self-emp-not-inc   99359  ...             60   United-States   <=50K
32560   52       Self-emp-inc  287927  ...             40   United-States    >50K

[2712 rows x 15 columns]
```

We can also use membership operations using the dataframe method `isin` (think of this as the `IN` command in SQL), where we check if elements in a column are in an array we specify. Let's count the number of government workers in our data. 

```python
df[df['workclass'].isin([' State-gov', ' Local-gov', ' Federal-gov'])].shape[0]
```

```
4351
```

We can also negate logical expressions with the tilde character, `~` (<code>SHIFT+\`</code>, typically located to the left of the 1 key on US-layout keyboards), to grab exactly the opposite of the expression. Above, we counted the number of government workers. Although we could count those who don't work in government by taking all the rows in the dataframe and subtracting the above, let's negate the expression above to get this number directly.

```python
df[~df['workclass'].isin([' State-gov', ' Local-gov', ' Federal-gov'])].shape[0]
```

```
28210
```

## Working with missing values

A missing value arises when there is no data in a place where we would expect there to be data. For instance, in a comma-separated value file, most rows may look like

```csv
customer_id,age,continent,price,order_id
```

but a certain row might contain

```csv
customer_id,age,continent,,order_id
```

In this case, there would be an `NA`,`NaN`, or `null` value where we would expect to see a price (`NA` simply stands for 'not available', which is more general than `NaN`, which stands for 'not a number'). This can lead to many problems. Suppose we wanted to know the average order value (a common metric in the ecommerce domain). Usually, we would just need to select the *price* column and then compute the mean or median — we might do something like this `st.mean(df['price'])` (more on this later) — but that would return `NaN`.

Some methods deal with `NaN`s or `NA`s intelligently, but **unless we know precisely how `NaN` values will be handled**, it is better to deal with them ourselves. Unfortunately, there is no best way to deal with `NaN` values — it all comes down to the situation at hand. Let's open the [code-along](./code_alongs/Missing_Values_Code_Along_(Student).ipynb?raw=true) and investigate how to deal with data with missing values. 
