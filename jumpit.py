from flask import Flask, make_response, request
import io
import csv
import pandas as pd
import numpy as np
import scipy.integrate as integrate

app = Flask(__name__)

def integrate2( A , dt  ,x0 = 0.0 ,v0 = 0.0 ,gamma = 0.1  ):
          ###########################################################################
          # arrays are allocated and filled with zeros
          N = A.size 
          print(N)

          x = np.zeros(N)
          v = np.zeros(N)
     

          ###########################################################################    
          # initial conditions
          x[0] = x0
          v[0] = v0

          ###########################################################################
          # integration
          fac1 = 1.0 - 0.5*gamma*dt
          fac2 = 1.0/(1.0 + 0.5*gamma*dt)

          for i in range( N -1 ):
	            #print(i)
	            v[i + 1] = fac1*fac2*v[i] - fac2*dt*x[i] + fac2*dt*A[i]
	            x[i + 1] = x[i] + dt*v[i + 1]
	            #E[i] += 0.5*(x[i]**2 + ((v[i] + v[i+1])/2.0)**2)

          print( "x" , x )
          print( "v" , v )
          ###########################################################################
          # return solution
          return x,v

def calculate( df ):

	df.columns = ["relative_time" , "acc" ]
	A = df["acc"].values - 9.8
	t = df["relative_time"].values/1000 #segs 
	dt = t.max() - t.min()
	vel = integrate.cumtrapz( A , dx = dt/A.size  )
	pos = integrate.cumtrapz( vel , dx = dt/A.size  )

	print( vel.max() )
	print( pos.max() )
	#print( A , dt )
	#integrate ( A , dt  )

	return "Done"


@app.route('/hello')
def hello_world():
    return 'Hello, World!'

@app.route('/')
def form():
    return """
        <html>
            <body>
                <h1>Experimento! </h1>

                <form action="/transform" method="post" enctype="multipart/form-data">
                    <input type="file" name="data_file" />
                    <input type="submit" />
                </form>
            </body>
        </html>
    """

@app.route('/transform', methods=["POST"])
def transform_view():
    f = request.files['data_file']
    if not f:
        return "No file"

    stream = io.StringIO(f.stream.read().decode("UTF8"), newline=None)
    df = pd.read_csv( stream )
    csv_input = csv.reader(stream)
    #print("file contents: ", file_contents)
    #print(type(file_contents))
    print(csv_input)
    for row in csv_input:
        print(row)

    stream.seek(0)
    result = calculate( df )

    response = make_response(result)
    response.headers["Content-Disposition"] = "attachment; filename=result.csv"


    return result