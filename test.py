from flask import Flask, request, jsonify
import pyodbc
 
app = Flask(__name__)
 

server = 'IN-BWF3NX3'
database = 'EmployeeDatabase'
username = 'sa'
password = 'sa'
driver = '{ODBC Driver 17 for SQL Server}'
 
def create_connection():
   
    connection = pyodbc.connect(
        f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'
)
    return connection
 
class EmployeeAPI:
    @staticmethod
    @app.route('/employees', methods=['GET'])
    def get_employees():
       
        connection = create_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT ID, Name, Salary FROM Employee")
        rows = cursor.fetchall()
        connection.close()
        employees = [{"ID": row[0], "Name": row[1], "Salary": float(row[2])} for row in rows]
        return jsonify(employees)
 
    @staticmethod
    @app.route('/employees', methods=['POST'])
    def add_employee():
       
        data = request.get_json()
        name = data.get('Name')
        salary = data.get('Salary')
 
        if not name or not salary:
            return jsonify({"error": "Name and Salary are required"}), 400
 
        connection = create_connection()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO Employee (Name, Salary) VALUES (?, ?)", (name, salary))
        connection.commit()
        connection.close()
        return jsonify({"message": "Employee added successfully"}), 201
 
    @staticmethod
    @app.route('/employees/<int:id>', methods=['PUT'])
    def update_employee(id):
       
        data = request.get_json()
        name = data.get('Name')
        salary = data.get('Salary')
 
        if not name or not salary:
            return jsonify({"error": "Name and Salary are required"}), 400
 
        connection = create_connection()
        cursor = connection.cursor()
        cursor.execute(
            "UPDATE Employee SET Name = ?, Salary = ? WHERE ID = ?", (name, salary, id)
        )
        connection.commit()
        rows_affected = cursor.rowcount
        connection.close()
 
        if rows_affected == 0:
            return jsonify({"error": "Employee not found"}), 404
 
        return jsonify({"message": "Employee updated successfully"}), 200
 
if __name__ == '__main__':
    app.run(debug=True)
