from distutils.log import debug
from fileinput import filename
import pandas as pd
from flask import Flask, request, render_template, session
import os
from werkzeug.utils import secure_filename
from ydata_profiling import ProfileReport

UPLOAD_FOLDER = os.path.join('staticFiles', 'uploads')

# Define allowed files
ALLOWED_EXTENSIONS = {'csv'}

app = Flask(__name__)

# Configure upload file path flask
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.secret_key = 'abcd'

filename = str()

@app.route('/', methods=['GET', 'POST'])
def uploadFile():
	if request.method == 'POST':
	# upload file flask
		f = request.files.get('file')

		# Extracting uploaded file name
		data_filename = secure_filename(f.filename)

		f.save(os.path.join(app.config['UPLOAD_FOLDER'],
							data_filename))
		global filename
		filename = data_filename
		session['uploaded_data_file_path'] = './staticFiles/uploads/' + data_filename

		return render_template('./upload_ok.html')
	return render_template("./upload.html")


@app.route('/upload_ml', methods=['GET', 'POST'])
def upload_ml_file():
	if request.method == 'POST':
	# upload file flask
		f = request.files.get('file')

		# Extracting uploaded file name
		data_filename = secure_filename(f.filename)

		f.save(os.path.join(app.config['UPLOAD_FOLDER'],
							data_filename))
		global filename
		filename = data_filename
		session['uploaded_data_file_path'] = './staticFiles/uploads/{}'.format(filename)

		# Uploaded File Path
		data_file_path = session['uploaded_data_file_path']
		# read csv
		df = pd.read_csv(data_file_path, encoding='unicode_escape', sep=',', engine='python')
		uploaded_df = pd.read_csv(data_file_path,
								encoding='unicode_escape')
		
		report = ProfileReport(df, title="CSV Advanced AI-Assisted Exploration", html={'style': {'full_width': True}})
		report.to_file('./templates/ml_output.html')


		return render_template('./upload_ok.html')
	return render_template("./upload.html")


@app.route('/show_data')
def showData():
	global filename
	# Uploaded File Path
	data_file_path = './staticFiles/uploads/{}'.format(filename)
	# read csv
	uploaded_df = pd.read_csv(data_file_path,
							encoding='unicode_escape')
	# Converting to html Table
	uploaded_df_html = uploaded_df.to_html()
	return render_template('show_csv.html',
						data_var=uploaded_df_html)


@app.route('/ml_show_data')
def show_ml_data():	
	return render_template('ml_output.html')


if __name__ == '__main__':
	app.run(debug=True)
