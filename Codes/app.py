from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict_price', methods=['POST'])
def predict():
    if request.method == 'POST':
        latitude = request.form['latitude']
        longitude = request.form['longitude']
        baths = request.form['baths']
        bedrooms = request.form['bedrooms']
        total_area = request.form['total_area']
        property_type = request.form['property_type']
        predicted_price = latitude+longitude+baths+bedrooms+total_area+property_type  
        return render_template('index.html', predicted_price=predicted_price)
    else:
        return render_template('index.html', predicted_price=None)

if __name__ == '__main__':
    app.run(debug=True)
