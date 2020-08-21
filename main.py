# Import requests package
import requests

# Assign URL to variable: url
url = 'https://www.themealdb.com/api/json/v1/1/random.php/?apikey=1'

# Package the request, send the request and catch the response: r
r = requests.get(url)

# Print the text of the response
print(r.text)
