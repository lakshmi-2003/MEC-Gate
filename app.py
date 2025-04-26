from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__,static_folder='static')

# Database connection function
def get_db_connection():
    conn = sqlite3.connect('MEC.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    if username == "admin" and password == "admin1":
        return redirect(url_for('dashboard'))
    elif username == "so1" and password == "so1":
        return redirect(url_for('user_dashboard'))
    else:
        return "<script>alert('Invalid username or password'); window.location.href='/'</script>"

@app.route('/collegebus')
def user_dashboard():
    return render_template('collegebus.html')

@app.route('/get_bus_logs')
def get_bus_logs():
    conn = get_db_connection()
    date_today = datetime.now().strftime("%Y-%m-%d")

    buses = conn.execute('SELECT * FROM Bus').fetchall()

    bus_logs = []
    for bus in buses:
        # Fetch the latest intime and outtime for this bus from CollegeBus
        log = conn.execute('''
            SELECT intime, outtime 
            FROM CollegeBus 
            WHERE bus_id = ? AND date = ? 
            ORDER BY id DESC LIMIT 1
        ''', (bus["bus_id"], date_today)).fetchone()

        bus_logs.append({
            "bus_id": bus["bus_id"],
            "bus_number": bus["bus_number"],
            "bus_route": bus["bus_route"],
            "date": date_today,
            "intime": log["intime"] if log else "-",   # ✅ Use stored intime if available
            "outtime": log["outtime"] if log else "-"  # ✅ Use stored outtime if available
        })

    conn.close()
    return jsonify(bus_logs)


# Insert In-Time entry in CollegeBus table
# Set In-Time

@app.route('/set_intime/<int:bus_id>', methods=['POST'])
def set_intime(bus_id):
    intime = datetime.now().strftime("%H:%M:%S")  # Get current time
    date_today = datetime.now().strftime("%Y-%m-%d")  # Get today's date

    # Fetch bus details from Bus table
    conn = get_db_connection()
    bus = conn.execute("SELECT bus_number, bus_route FROM Bus WHERE bus_id = ?", (bus_id,)).fetchone()

    if bus is None:
        conn.close()
        return jsonify({"success": False, "error": "Bus not found"}), 404

    bus_number, bus_route = bus

    # Insert a new record every time Set In-Time is clicked
    conn.execute('''
        INSERT INTO CollegeBus (bus_id, bus_number, bus_route, date, intime, outtime)
        VALUES (?, ?, ?, ?, ?, ?);
    ''', (bus_id, bus_number, bus_route, date_today, intime, '-'))

    conn.commit()
    conn.close()
    
    return jsonify({"success": True, "intime": intime})



# Set Out-Time
@app.route('/set_outtime/<int:bus_id>', methods=['POST'])
def set_outtime(bus_id):
    outtime = datetime.now().strftime("%H:%M:%S")  # Get current time
    date_today = datetime.now().strftime("%Y-%m-%d")  # Get today's date

    conn = get_db_connection()

    latest_entry = conn.execute('''
        SELECT id FROM CollegeBus
        WHERE bus_id = ? AND date = ?
        ORDER BY id DESC
        LIMIT 1;
    ''', (bus_id, date_today)).fetchone()

    if latest_entry:
        latest_id = latest_entry['id']
        
        # Update the outtime for the latest entry
        conn.execute('''
            UPDATE CollegeBus
            SET outtime = ?
            WHERE id = ?;
        ''', (outtime, latest_id))

        conn.commit()
        conn.close()

        return jsonify({"success": True, "outtime": outtime})
    else:
        conn.close()
        return jsonify({"success": False, "error": "No matching entry found"}), 404

@app.route('/visitors')
def visitor_page():
    return render_template('visitors.html')

@app.route('/submit_visitor', methods=['POST'])
def submit_visitor():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO Visitors (name, mobile, purpose, vehicle, vehicle_type, vehicle_number, intime)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        data['name'], data['mobile'], data['purpose'], data['vehicle'],
        data['vehicle_type'], data['vehicle_number'], data['intime']
    ))

    conn.commit()
    conn.close()
    return jsonify({"message": "Visitor entry saved successfully!"})

@app.route('/get_visitors', methods=['GET'])
def get_visitors():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, mobile, purpose, vehicle, vehicle_type, vehicle_number, intime, outtime FROM Visitors WHERE outtime IS NULL")
    visitors = cursor.fetchall()
    conn.close()

    visitors_list = []
    for visitor in visitors:
        visitors_list.append({
            "id": visitor[0],
            "name": visitor[1],
            "mobile": visitor[2],
            "purpose": visitor[3],
            "vehicle": visitor[4],
            "vehicle_type": visitor[5],
            "vehicle_number": visitor[6],
            "intime": visitor[7],
            "outtime": visitor[8]
        })

    return jsonify(visitors_list)

@app.route('/update_outtime', methods=['POST'])
def update_outtime():
    data = request.json
    visitor_id = data['id']
    outtime = data['outtime']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE Visitors SET outtime = ? WHERE id = ?", (outtime, visitor_id))
    conn.commit()
    conn.close()

    return jsonify({"message": "Out-Time updated successfully!"})


@app.route('/outpass')
def outpass_page():
    return render_template('outpass.html')

@app.route('/submit_outpass', methods=['POST'])
def submit_outpass():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO Outpass (name, department, hostel, hostel_type, room_number, reason, outtime, date)
        VALUES (?, ?, ?, ?, ?, ?,?, ?)
    ''', (
        data['name'], data['department'], data['hostel'], data['hostel_type'],
        data['room_number'], data['reason'], data['outtime'], data['date']
    ))

    conn.commit()
    conn.close()
    return jsonify({"message": "Outpass entry saved successfully!"})

@app.route('/latecomers')
def latecomers_page():
    return render_template('latecomers.html')

@app.route('/submit_latecomer', methods=['POST'])
def submit_latecomer():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO Latecomers (name, department, intime, reason, date)
        VALUES (?, ?, ?, ?, ?)
    ''', (
        data['name'], data['department'], data['intime'],
        data['reason'], data['date']
    ))

    conn.commit()
    conn.close()
    return jsonify({"message": "Latecomer entry saved successfully!"})

#admin
# Function to fetch counts from the database
def get_counts():
    conn = get_db_connection()
    cursor = conn.cursor()

    today_date = datetime.now().strftime('%Y-%m-%d')

    def fetch_count(query, params=()):
        cursor.execute(query, params)
        result = cursor.fetchone()
        return result[0] if result else 0

    # Fetching counts safely
    collegebus_count = fetch_count("SELECT COUNT(*) FROM CollegeBus WHERE date = ?", (today_date,))
    visitors_count = fetch_count("SELECT COUNT(*) FROM Visitors WHERE date = ?", (today_date,))
    vehicles_count = fetch_count("SELECT COUNT(*) FROM Visitors WHERE date = ? AND vehicle='Yes'", (today_date,))
    hostel_count=fetch_count("SELECT COUNT(*) FROM Outpass WHERE date=? AND hostel='Yes'",(today_date,))
    outpass_count = fetch_count("SELECT COUNT(*) FROM Outpass WHERE date = ?", (today_date,))
    latecomers_count = fetch_count("SELECT COUNT(*) FROM Latecomers WHERE date = ?", (today_date,))

    conn.close()

    return {
        "collegebus_count": collegebus_count,
        "visitors_count": visitors_count,
        "vehicles_count": vehicles_count,
        "hostel_count":hostel_count,
        "outpass_count": outpass_count,
        "latecomers_count": latecomers_count
    }

@app.route("/dashboard")
def dashboard():
    counts = get_counts()
    return render_template("admin.html", **counts)


# Fetch bus summary counts
def get_bus_counts():
    conn = get_db_connection()
    cursor = conn.cursor()

    today_date = datetime.now().strftime("%Y-%m-%d")

    cursor.execute("SELECT COUNT(*) FROM Bus")
    total_bus = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM CollegeBus WHERE intime != '-' AND outtime = '-' AND date = ?", (today_date,))
    in_station = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM CollegeBus WHERE outtime != '-' AND date = ?", (today_date,))
    out_station = cursor.fetchone()[0]

    conn.close()
    return total_bus, in_station, out_station

# Function to fetch buses based on selected date
def get_buses_by_date(selected_date):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT bus_id, bus_number, bus_route, intime, outtime FROM CollegeBus WHERE date = ?", (selected_date,))
    data = cursor.fetchall()

    conn.close()
    return data

@app.route("/collegeBus", methods=["GET", "POST"])
def college_bus_view():
    total_bus, in_station, out_station = get_bus_counts()
    buses = []

    if request.method == "POST":
        selected_date = request.form.get("selected_date")
        buses = get_buses_by_date(selected_date)

    return render_template("college_bus_view.html", total_bus=total_bus, in_station=in_station, out_station=out_station, buses=buses)

@app.route('/add_bus', methods=['POST'])
def add_bus():
    data = request.json
    bus_number = data.get("bus_number")
    bus_route = data.get("bus_route")

    if not bus_number or not bus_route:
        return jsonify({"message": "Bus Number and Route are required!"}), 400

    conn = get_db_connection()
    try:
        conn.execute("INSERT INTO Bus (bus_number, bus_route) VALUES (?, ?)", (bus_number, bus_route))
        conn.commit()
        return jsonify({"message": "Bus added successfully!"})
    except sqlite3.IntegrityError:
        return jsonify({"message": "Bus Number already exists!"}), 400
    finally:
        conn.close()

# Remove Bus API
@app.route('/remove_bus', methods=['POST'])
def remove_bus():
    data = request.json
    bus_number = data.get("bus_number")

    if not bus_number:
        return jsonify({"message": "Bus Number is required!"}), 400

    conn = get_db_connection()
    cursor = conn.execute("DELETE FROM Bus WHERE bus_number = ?", (bus_number,))
    conn.commit()
    conn.close()

    if cursor.rowcount == 0:
        return jsonify({"message": "Bus not found!"}), 404
    return jsonify({"message": "Bus removed successfully!"})

@app.route('/vehicle_view')
def vehicle_view():
    return render_template('vehicles_view.html')

@app.route('/get_vehicle_entries', methods=['POST'])
def get_vehicle_entries():
    date_selected = request.form.get('selected_date')

    if not date_selected:
        return jsonify({'success': False, 'message': 'No date selected'})

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Visitors WHERE vehicle = 'Yes' AND date = ?", (date_selected,))
    vehicle_entries = cursor.fetchall()
    conn.close()

    if not vehicle_entries:
        return jsonify({'success': False, 'message': 'No records found'})

    # Convert rows to dictionary for JSON response
    vehicle_data = [dict(row) for row in vehicle_entries]

    return jsonify({'success': True, 'data': vehicle_data})

@app.route('/visitors_view')
def visitor_view():
    return render_template('visitors_view.html')

@app.route('/get_visitors_entries', methods=['POST'])
def get_visitors_entries():
    date_selected = request.form.get('selected_date')

    if not date_selected:
        return jsonify({'success': False, 'message': 'No date selected'})

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Visitors WHERE vehicle = 'No' AND date = ?", (date_selected,))
    visitor_entries = cursor.fetchall()
    conn.close()

    if not visitor_entries:
        return jsonify({'success': False, 'message': 'No records found'})

    # Convert rows to dictionary for JSON response
    visitor_data = [dict(row) for row in visitor_entries]

    return jsonify({'success': True, 'data': visitor_data})

def get_hostel_counts():
    conn = get_db_connection()
    cursor = conn.cursor()

    today_date = datetime.now().strftime("%Y-%m-%d")

    cursor.execute("SELECT COUNT(*) FROM Outpass WHERE hostel='Yes' AND date=?",(today_date,))
    total_outpass = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM Outpass WHERE hostel_type='Girls' AND date = ?", (today_date,))
    girls_hostel = cursor.fetchone()[0] 

    cursor.execute("SELECT COUNT(*) FROM Outpass WHERE hostel_type='Boys' AND date = ?", (today_date,))
    boys_hostel = cursor.fetchone()[0] 

    conn.close()
    return total_outpass, girls_hostel, boys_hostel

# Function to fetch hostel based on selected date
def get_outpass_by_date(selected_date):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Outpass WHERE hostel='Yes' AND date = ?", (selected_date,))
    data = cursor.fetchall()

    conn.close()
    return data

@app.route("/hostelview", methods=["GET", "POST"])
def hostellers_view():
    total_outpass, girls_hostel, boys_hostel = get_hostel_counts()
    hostel = []

    if request.method == "POST":
        selected_date = request.form.get("selected_date")
        hostel = get_outpass_by_date(selected_date)

    return render_template("hostellers_view.html", total_outpass=total_outpass, girls_hostel=girls_hostel, boys_hostel=boys_hostel, hostel=hostel)

@app.route('/outpass_view')
def outpass_view():
    return render_template('outpass_view.html')

@app.route('/get_outpass_entries', methods=['POST'])
def get_outpass_entries():
    date_selected = request.form.get('selected_date')

    if not date_selected:
        return jsonify({'success': False, 'message': 'No date selected'})

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Outpass WHERE hostel = 'No' AND date = ?", (date_selected,))
    outpass_entries = cursor.fetchall()
    conn.close()

    if not outpass_entries:
        return jsonify({'success': False, 'message': 'No records found'})

    # Convert rows to dictionary for JSON response
    outpass_data = [dict(row) for row in outpass_entries]

    return jsonify({'success': True, 'data': outpass_data})

@app.route('/latecomers_view')
def latecomers_view():
    return render_template('latecomers_view.html')

@app.route('/get_latecomers_entries', methods=['POST'])
def get_latecomers_entries():
    date_selected = request.form.get('selected_date')

    if not date_selected:
        return jsonify({'success': False, 'message': 'No date selected'})

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Latecomers WHERE date = ?", (date_selected,))
    latecomers_entries = cursor.fetchall()
    conn.close()

    if not latecomers_entries:
        return jsonify({'success': False, 'message': 'No records found'})

    # Convert rows to dictionary for JSON response
    latecomers_data = [dict(row) for row in latecomers_entries]

    return jsonify({'success': True, 'data': latecomers_data})

@app.route('/')
def logout():
    return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True,port=7000,host='0.0.0.0')
