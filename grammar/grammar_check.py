#calling word's in built spell/ grammar check
import win32com.client, os

wdDoNotSaveChanges = 0
path = os.path.abspath('grammar/input.txt')

snippet = 'Jon Skeet lieks ponies.  I can haz reputashunz?'
snippet += 'This is a correct sentence.'
file = open("input2.txt", 'w')
file.write(snippet)
file.close()

app = win32com.client.gencache.EnsureDispatch('Word.Application')
doc = app.Documents.Open(path)
print ("Grammar: ",doc.GrammaticalErrors.Count,)
print ("Spelling: ",doc.SpellingErrors.Count,)

app.Quit(wdDoNotSaveChanges)
