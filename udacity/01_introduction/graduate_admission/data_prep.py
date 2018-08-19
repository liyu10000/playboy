import random
import pandas as pd

csv_name = "./binary.csv"
df = pd.read_csv(csv_name)

# make dummy variables for rank
data = pd.concat([df, pd.get_dummies(df["rank"], prefix="rank")], axis=1)
data = data.drop("rank", axis=1)

# standardize gre and gpa
for field in ("gre", "gpa"):
	mean, std = data[field].mean(), data[field].std()
	data.loc[:,field] = (data[field]-mean)/std

# split off random 10% of the data for testing
random.seed(2018)
sample = random.sample(data.index, k=int(len(data)*0.9))
data, test_data = data.iloc[sample], data.drop(sample)
print("# train: {}, # test: {}".format(len(data), len(test_data)))

# split into features and targets
features, targets = data.drop("admit", axis=1), data["admit"]
features_test, targets_test = test_data.drop("admit", axis=1), test_data["admit"]
