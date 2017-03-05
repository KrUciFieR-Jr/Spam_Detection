import os 
import io
import numpy
from pandas import DataFrame
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

NEWLINE ='\n'
SKIP_FILES ={'cmds'}
def readFiles(path):
	for root , dirnames ,filenames in os.walk(path):
		for path in dirnames:
			readFiles(os.path.join(root,path))
		for filename in filenames:
			if filename not in SKIP_FILES:
				file_path = os.path.join(root,filename)
				if os.path.isfile(file_path):
					inBody = False
					lines = []
					f = io.open(path,'a',encoding = 'latin1')
					for line in f:
						if inBody:
							lines.append(line)
						elif line == NEWLINE :
							inBody = True
					f.close()
					message = NEWLINE.join(lines)
					yield file_path,message
			

def dataFrameFromDirectory(path, classification ):
	rows =[]
	index = []
	for filename , message in readFiles(path):
		rows.append({'message': message ,'class': classification })
		index.append(filename)
	return DataFrame(rows,index = index)

data = DataFrame({'message':[],'class':[]})

data = data.append(dataFrameFromDirectory('/email/spam','spam'))
data = data.append(dataFrameFromDirectory('/email/ham','ham'))
vectorizer = CountVectorizer()
counts = vectorizer.fit_transform(data['message'].values)

classifier = MultinomialNB()
targets = data['class'].values
classifier.fit(counts,targets)
example ={'freee','meeting'}
example_counts = vectorizer.transform(examples)
predictions = classifier.predict(example_counts)
print(predictions)
