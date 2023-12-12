import pandas as pd 

results_table = pd.read_csv("results", delimiter=" ", header=None)
results_table.columns = ['qid', 'run','sha','rank','score','what']
mapping_table = pd.read_csv('metadata round1 test.csv',encoding = "utf-8", delimiter=";").dropna()

mapping_table['sha'] = mapping_table['sha'].str.split('; ')
mapping_table = mapping_table.explode('sha')

# Merge the tables based on document_id with a left join
merged_table = pd.merge(results_table, mapping_table, on='sha', how='left')

# Fill NaN values in the 'article_id' column with the original 'document_id' values
merged_table['cord_uid'].fillna(merged_table['sha'], inplace=True)

# Drop the original document_id column and rename the new one
merged_table = merged_table.drop(columns=['sha'])
merged_table = merged_table.rename(columns={'cord_uid': 'sha'})

# Display the updated table
print(merged_table)

desired_column_order = ['qid', 'run', 'sha', 'rank', 'score', 'what']
merged_table = merged_table[desired_column_order]

merged_table.to_csv('new_test', sep=' ', index=False, header=False)