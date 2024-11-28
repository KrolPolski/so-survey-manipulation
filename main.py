import pandas
#from StringIO import StringIO
csvFile = pandas.read_csv('survey_results_public.csv')
finland = csvFile[csvFile['Country'] == 'Finland']
finland.to_csv("filtered_data.csv", index=False)
languages = finland['LanguageHaveWorkedWith'].dropna().str.split(';', expand=True).stack()
word_counts = languages.value_counts()
print("Languages I have Worked With:")
print(word_counts)
wantLanguages = finland['LanguageWantToWorkWith'].dropna().str.split(';', expand=True).stack()
wantCount = wantLanguages.value_counts()
print("Languages I want to work with:")
print(wantCount)