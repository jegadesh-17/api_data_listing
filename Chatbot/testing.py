from flask import Flask, jsonify,request
from pymongo import MongoClient, errors
from bson.json_util import dumps
from flask_cors import CORS, cross_origin




app = Flask(__name__)
CORS(app)

# MongoDB configuration
try:
    client = MongoClient('mongodb+srv://ssdev:ssdev123@ssdev.us8prjv.mongodb.net/test')
    db = client['job_data']  # Replace with your database name
    collection = db['job']  # Replace with your collection name
    print("Connected to MongoDB successfully")
except errors.ConnectionError as e:
    print(f"Failed to connect to MongoDB: {e}")

# Initial job data
job_data = {
    "job_title": "python",
    "assigned_to": [],
    "status": "Open",
    "no_of_positions": "2",
    "priority": "Low",
    "client": "maersk",
    "job_description": "<p>test java developer</p>",
    "additional_details": "<p></p>",
    "due_date": "2024-06-14T18:30:00.000Z",
    "notice_period": "< 15 Days",
    "minimum_experience": 26,
    "maximum_experience": 39,
    "mode_of_hire": "Permanent",
    "vendor_name": "",
    "poc_vendor": "",
    "job_rr_id": "",
    "skillset": [{"skill": "java", "exp": 53}]
}

# Insert initial data into MongoDB
try:
    collection.insert_one(job_data)
    print("Initial job data inserted successfully")
except errors.PyMongoError as e:
    print(f"Failed to insert initial job data: {e}")

@app.route('/')
def index():
    # Retrieve all job data from MongoDB
    try:
        job_data = list(collection.find({}))
        if job_data:
            # Render the job data as an HTML string
            html_content = '<h1>Job Listings</h1>'
            html_content += '<ul>'
            for job in job_data:
                html_content += '<li>'
                html_content += f'<h2>{job["job_title"]}</h2>'
                html_content += f'<p>Status: {job["status"]}</p>'
                html_content += f'<p>Client: {job["client"]}</p>'
                html_content += f'<p>Priority: {job["priority"]}</p>'
                html_content += f'<p>Description: {job["job_description"]}</p>'
                html_content += f'<p>Due Date: {job["due_date"]}</p>'
                html_content += '</li>'
            html_content += '</ul>'
            return html_content
        else:
            return "<h1>No job data available</h1>"
    except errors.PyMongoError as e:
        return f"<h1>Failed to retrieve job data: {e}</h1>"

@app.route('/api/job', methods=['POST'])
def add_job():
    try:
        data = request.get_json()
        # Insert new job data into MongoDB
        result = collection.insert_one(data)
        return jsonify({"success": True, "message": f"Job added with ID: {result.inserted_id}"}), 201
    except errors.PyMongoError as e:
        return jsonify({"success": False, "message": f"Failed to add job: {e}"}), 500

@app.route('/api/job', methods=['GET'])
def get_jobs():
    try:
        # Retrieve all job data from MongoDB
        job_data = list(collection.find({}))
        if job_data:
            return dumps(job_data), 200
        else:
            return jsonify({"error": "No job data available"}), 404
    except errors.PyMongoError as e:
        return jsonify({"error": f"Failed to retrieve jobs: {e}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
