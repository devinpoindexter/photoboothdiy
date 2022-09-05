from datetime import datetime

now = datetime.now()
filename = now.strftime('%m-%d-%Y.jpg')

print(filename)