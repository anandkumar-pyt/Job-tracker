

from flask import Flask,render_template,request,url_for,redirect
from config import get_db_connection

app = Flask(__name__)

# jobs = [
#     {
#         "id": 1,
#         "company": "Amazon",
#         "role": "Backend Developer",
#         "status": "Applied"
#     },
#     {
#         "id": 2,
#         "company": "Google",
#         "role": "Python Developer",
#         "status": "Interview"
#     }
# ]

@app.route("/")
def home():
    connection = get_db_connection()
    jobs=connection.execute("Select * from jobs ORDER BY id DESC").fetchall()
    # cursor = connection.cursor()
    # cursor.execute("SELECT DATABASE()")
    # database = cursor.fetchone()
    # cursor.close()
    connection.close()
    return render_template("index.html",jobs=jobs)

@app.route("/addjob" , methods=['POST'])
def addjob():
   company=request.form.get("company")
   role=request.form.get("role")
   connection=get_db_connection()
   connection.execute("INSERT INTO jobs (company,role,status) VALUES (?,?,?)",(company,role,'Applied'))
   connection.commit()
   connection.close()
   return redirect(url_for("home"))

@app.route("/update-job/<int:job_id>",methods=["POST"])
def update_job(job_id):
    new_status=request.form.get("status","").strip()
    allowed_status= ["Applied", "Interview", "Rejected", "Selected"]
    if not new_status in allowed_status:
        return "invalid status",400
    connection=get_db_connection()
    connection.execute("UPDATE jobs SET status = ? WHERE id = ?", (new_status,job_id))
    connection.commit()
    connection.close()
    return redirect(url_for("home"))

@app.route("/delete-job/<int:job_id>", methods=["POST"])
def delete_job(job_id):
    connection=get_db_connection()
    connection.execute("DELETE FROM jobs where id = ? ", (job_id,))
    connection.commit()
    connection.close()
    return redirect(url_for("home"))

#@app.route("/about/<fname>/<lname>")
#def about(fname, lname):
#    return f"This is about {fname} {lname}"
#@app.route("/files/<path:file_path>")
#def paths(file_path):
#    return f"Your file is in {file_path}"
# @app.route("/search")
# def search():
#     name=request.args.get("name")
#     return f"Hello {name}"
if __name__ == "__main__":
    app.run(debug=True)