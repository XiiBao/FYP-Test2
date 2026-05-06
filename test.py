import os
import pysd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(BASE_DIR, 'water.mdl')

print(file_path)
print(os.path.exists(file_path))

model = pysd.read_vensim(file_path)

results = model.run()

# 3. View the results
print(results.head())