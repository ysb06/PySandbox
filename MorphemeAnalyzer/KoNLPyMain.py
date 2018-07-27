import konlpy
import csv

kkma = konlpy.tag.Kkma()

data = open('Data/SentancesData/AC Data.csv', 'r')
dataLines = csv.reader(data)

result = open('Data/SentancesData/Result.csv', 'w', newline='')
csvWriter = csv.writer(result)

result_set = open('Data/SentancesData/Result Set.csv', 'w', newline='')
csvWriter_set = csv.writer(result_set)
wordSet = set()

print('-' * 50)
for line in dataLines:
    if line[0] != 'C0':
        code = line[0] + '.' + line[1] + '.' + line[2] + '.' + line[3] + '.' + line[4]
        morphemes = kkma.morphs(line[5])

        print(code + '\t\t|', end='\t')
        print(morphemes)
        print('-' * 50)

        row = [code] + morphemes
        csvWriter.writerow(row)

        wordSet.update(morphemes)

while len(wordSet) > 0:
    word = wordSet.pop()
    csvWriter_set.writerow([word])
    if len(wordSet) % 10 == 0:
        print(word)
    else:
        print(word, end=', ')

data.close()
result.close()
