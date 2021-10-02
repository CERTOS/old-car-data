import numpy as np
import pandas as pd
import traceback
from flask import Flask, request, jsonify, render_template
import pickle
app = Flask(__name__)
model = pickle.load(open("model.pkl", "rb"))
modelcol = pickle.load(open("modelcol.pkl", "rb"))
@app.route('/')
def home():
    return render_template('home.html')
@app.route('/predict', methods = ["POST"])
def predict():
    if request.method=="POST":
        maker= request.form["maker"]
        Type = request.form["type"]
        origin = request.form["origin"]
        drivetrain = request.form["drivetrain"]
        EngineSize = request.form["EngineSize"]
        Cylinders = request.form["Cylinders"]
        Horsepower = request.form["Horsepower"]
        MPG_City = request.form["MPG_City"]
        MPG_Highway = request.form["MPG_Highway"]
        Weight = request.form["Weight"]
        Wheelbase = request.form["Wheelbase"]
        Length = request.form["Length"]
        import csv
        with open('test.csv','w') as f:
            thewriterx = csv.writer(f)
            thewriterx.writerow(["Make","Type","Origin","DriveTrain","EngineSize","Cylinders","Horsepower","MPG_City","MPG_Highway","Weight","Wheelbase","Length"])
            thewriterx.writerow([maker,Type,origin,drivetrain,EngineSize,Cylinders,Horsepower,MPG_City,MPG_Highway,Weight,Wheelbase,Length])

        excelfile=pd.read_csv("test.csv")
        dumy=pd.get_dummies(excelfile,columns=["Make","Type","Origin","DriveTrain"])
        dumy = dumy.reindex(columns=modelcol, fill_value=0)
        dumy=np.array(dumy)
        output = model.predict(dumy)
        output_r=np.round(output,2)
        output_list=output_r.tolist()
        inrs = output_list[0] * 73.25
        final_inrs = round(inrs,2)
        return render_template('home.html', prediction_text='Predicted Price of your Car should be ₹ {}'.format(final_inrs))
 
if __name__ == "__main__":
    app.run(debug=True)
