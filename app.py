from flask import Flask, request, jsonify, render_template
import mysql.connector
import subprocess
import os

app = Flask(__name__)

def init_db():
    conn = mysql.connector.connect(
        host='localhost',
        user='root',  # Replace with your MySQL username
        password='root',  # Replace with your MySQL password
        database='automated_gate_system'  # Updated database name to automated_gate_system
    )
    c = conn.cursor()
    
    # Create Drivers table
    c.execute('CREATE TABLE IF NOT EXISTS drivers (id_number VARCHAR(255) PRIMARY KEY)')
    
    # Create License Plates table
    c.execute('CREATE TABLE IF NOT EXISTS plates (plate VARCHAR(255) PRIMARY KEY, id_number VARCHAR(255), FOREIGN KEY (id_number) REFERENCES drivers (id_number) ON DELETE CASCADE)')
    
    conn.commit()
    conn.close()

def extract_license_plate(frame):
    """
    Extract license plate text using OpenALPR.
    """
    # Save the frame as an image
    frame_path = 'temp_frame.jpg'
    frame.save(frame_path)

    # Run OpenALPR on the image
    result = subprocess.run(['alpr', '-c', 'us', frame_path], capture_output=True, text=True)

    # Process OpenALPR output and extract plate number
    for line in result.stdout.splitlines():
        if line.startswith(" plate: "):
            return line.split(': ')[1].strip()

    return None

@app.route('/check_plate', methods=['GET'])
def check_plate():
    plate = request.args.get('plate')
    conn = mysql.connector.connect(
        host='localhost',
        user='root',  # Replace with your MySQL username
        password='root',  # Replace with your MySQL password
        database='automated_gate_system'  # Updated database name to automated_gate_system
    )
    c = conn.cursor()
    c.execute('SELECT * FROM plates WHERE plate = %s', (plate,))
    result = c.fetchone()
    conn.close()
    return jsonify({"registered": result is not None})

@app.route('/register_plate', methods=['POST'])
def register_plate():
    id_number = request.form['id_number']
    plate = request.form['plate']
    
    conn = mysql.connector.connect(
        host='localhost',
        user='root',  # Replace with your MySQL username
        password='root',  # Replace with your MySQL password
        database='automated_gate_system'  # Updated database name to automated_gate_system
    )
    c = conn.cursor()

    # Check if the driver exists
    c.execute('SELECT * FROM drivers WHERE id_number = %s', (id_number,))
    driver = c.fetchone()
    
    if driver is None:
        # If the driver does not exist, create a new driver entry
        c.execute('INSERT INTO drivers (id_number) VALUES (%s)', (id_number,))
    
    # Check for existing license plates
    c.execute('SELECT * FROM plates WHERE plate = %s', (plate,))
    if c.fetchone() is not None:
        conn.close()
        return jsonify({"message": "License Plate already registered!"}), 400

    c.execute('INSERT INTO plates (plate, id_number) VALUES (%s, %s)', (plate, id_number))
    conn.commit()
    conn.close()
    return jsonify({"message": "License Plate Registered!"}), 200

@app.route('/update_plate', methods=['POST'])
def update_plate():
    id_number = request.form['update_id']
    old_plate = request.form['old_plate']
    new_plate = request.form['new_plate']

    conn = mysql.connector.connect(
        host='localhost',
        user='root',  # Replace with your MySQL username
        password='root',  # Replace with your MySQL password
        database='automated_gate_system'  # Updated database name to automated_gate_system
    )
    c = conn.cursor()

    # Check if the existing plate belongs to the given ID
    c.execute('SELECT * FROM plates WHERE id_number = %s AND plate = %s', (id_number, old_plate))
    plate = c.fetchone()
    
    if plate is None:
        conn.close()
        return jsonify({"message": "No license plate found for the given ID!"}), 404

    # Update the license plate
    c.execute('UPDATE plates SET plate = %s WHERE id_number = %s AND plate = %s', (new_plate, id_number, old_plate))
    conn.commit()
    conn.close()
    return jsonify({"message": "License Plate Updated!"}), 200

@app.route('/delete_plate', methods=['POST'])
def delete_plate():
    id_number = request.form['delete_id']
    plate = request.form['delete_plate']

    conn = mysql.connector.connect(
        host='localhost',
        user='root',  # Replace with your MySQL username
        password='root',  # Replace with your MySQL password
        database='automated_gate_system'  # Updated database name to automated_gate_system
    )
    c = conn.cursor()

    # Check if the existing plate belongs to the given ID
    c.execute('SELECT * FROM plates WHERE id_number = %s AND plate = %s', (id_number, plate))
    existing_plate = c.fetchone()
    
    if existing_plate is None:
        conn.close()
        return jsonify({"message": "No license plate found for the given ID!"}), 404

    # Delete the license plate
    c.execute('DELETE FROM plates WHERE id_number = %s AND plate = %s', (id_number, plate))
    conn.commit()
    conn.close()
    return jsonify({"message": "License Plate Deleted!"}), 200

@app.route('/delete_driver', methods=['POST'])
def delete_driver():
    id_number = request.form['delete_driver_id']

    conn = mysql.connector.connect(
        host='localhost',
        user='root',  # Replace with your MySQL username
        password='root',  # Replace with your MySQL password
        database='automated_gate_system'  # Updated database name to automated_gate_system
    )
    c = conn.cursor()

    # Check if the driver exists
    c.execute('SELECT * FROM drivers WHERE id_number = %s', (id_number,))
    driver = c.fetchone()

    if driver is None:
        conn.close()
        return jsonify({"message": "No driver found with the given ID!"}), 404

    # Delete the driver, which will also delete associated license plates
    c.execute('DELETE FROM drivers WHERE id_number = %s', (id_number,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Driver and associated license plates deleted!"}), 200

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)
