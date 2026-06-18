from flask import Flask, render_template, request, redirect, url_for
from db import get_connection
from datetime import date

app = Flask(__name__)

@app.route('/')
def dashboard():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) AS total FROM equipment")
    total = cur.fetchone()['total']

    cur.execute("""
        SELECT status, COUNT(*) AS count
        FROM equipment
        GROUP BY status
    """)
    status_counts = cur.fetchall()

    cur.execute("""
        SELECT e.equipment_name,
               e.department,
               m.next_due_date
        FROM equipment e
        JOIN maintenance_log m
        ON e.equipment_id = m.equipment_id
        WHERE m.next_due_date < CURDATE()
    """)
    overdue = cur.fetchall()

    conn.close()

    return render_template(
        'dashboard.html',
        total=total,
        status_counts=status_counts,
        overdue=overdue
    )

@app.route('/equipment')
def equipment():

    department = request.args.get('department')
    status = request.args.get('status')

    conn = get_connection()
    cur = conn.cursor()

    query = "SELECT * FROM equipment WHERE 1=1"
    params = []

    if department:
        query += " AND department=%s"
        params.append(department)

    if status:
        query += " AND status=%s"
        params.append(status)

    cur.execute(query, params)

    equipment_list = cur.fetchall()

    conn.close()

    return render_template(
        'equipment_list.html',
        equipment=equipment_list
    )

@app.route('/add_equipment', methods=['GET', 'POST'])
def add_equipment():

    if request.method == 'POST':

        equipment_name = request.form['equipment_name']
        serial_number = request.form['serial_number']
        department = request.form['department']
        purchase_date = request.form['purchase_date']
        status = request.form['status']

        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO equipment
            (
                equipment_name,
                serial_number,
                department,
                purchase_date,
                status
            )
            VALUES (%s,%s,%s,%s,%s)
        """,
        (
            equipment_name,
            serial_number,
            department,
            purchase_date,
            status
        ))

        conn.commit()
        conn.close()

        return redirect('/equipment')

    return render_template('add_equipment.html')

@app.route('/equipment/<int:id>')
def history(id):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM equipment WHERE equipment_id=%s",
        (id,)
    )

    equipment = cur.fetchone()

    cur.execute("""
        SELECT *
        FROM maintenance_log
        WHERE equipment_id=%s
        ORDER BY maintenance_date DESC
    """,(id,))

    logs = cur.fetchall()

    conn.close()

    return render_template(
        'maintenance_history.html',
        equipment=equipment,
        logs=logs
    )

@app.route('/add_maintenance/<int:id>',
methods=['GET','POST'])
def add_maintenance(id):

    if request.method == 'POST':

        maintenance_date = request.form['maintenance_date']
        technician_name = request.form['technician_name']
        issue_reported = request.form['issue_reported']
        resolution_notes = request.form['resolution_notes']
        next_due_date = request.form['next_due_date']

        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO maintenance_log
            (
                equipment_id,
                maintenance_date,
                technician_name,
                issue_reported,
                resolution_notes,
                next_due_date
            )
            VALUES (%s,%s,%s,%s,%s,%s)
        """,
        (
            id,
            maintenance_date,
            technician_name,
            issue_reported,
            resolution_notes,
            next_due_date
        ))

        conn.commit()
        conn.close()

        return redirect(
            url_for('history', id=id)
        )

    return render_template(
        'add_maintenance.html',
        equipment_id=id
    )

@app.route('/update_status/<int:id>',
methods=['POST'])
def update_status(id):

    status = request.form['status']

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "UPDATE equipment SET status=%s WHERE equipment_id=%s",
        (status,id)
    )

    conn.commit()
    conn.close()

    return redirect('/equipment')

@app.route('/api/overdue')
def overdue_json():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT e.equipment_name,
               e.department,
               m.next_due_date
        FROM equipment e
        JOIN maintenance_log m
        ON e.equipment_id=m.equipment_id
        WHERE m.next_due_date<CURDATE()
    """)

    data = cur.fetchall()

    conn.close()

    return data

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)