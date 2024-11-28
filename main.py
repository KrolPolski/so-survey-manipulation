import pandas
#from StringIO import StringIO
csvFile = pandas.read_csv('survey_results_public.csv')
finland = csvFile[csvFile['Country'] == 'Finland']
finland.to_csv("filtered_data.csv", index=False)
print(finland)
