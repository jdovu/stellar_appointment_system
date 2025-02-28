
"""
 * @file database.py
 * @brief SQLite database operations for managing appointments.
"""

import sqlite3
from datetime import datetime

def init_db():
    """
    @brief Initializes the SQLite database and creates the appointments table if it doesn't exist.

    This function establishes a connection to the SQLite database and ensures that the 'appointments'
    table exists with the necessary schema.
    """
    conn = sqlite3.connect('appointments.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient TEXT NOT NULL,
            date TEXT NOT NULL,
            time TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def schedule_appointment(patient, date, time):
    """
    @brief Schedules a new appointment and saves it in the database.

    @param patient A string containing the name of the patient.
    @param date A string representing the appointment date (YYYY-MM-DD).
    @param time A string representing the appointment time (HH:MM format).

    @return Returns the appointment ID of the newly scheduled appointment.
    """
    conn = sqlite3.connect('appointments.db')
    c = conn.cursor()
    # CALL OUT!!!
    # 04 - Insert a new appointment into the SQLite database
    c.execute('INSERT INTO appointments (patient, date, time) VALUES (?, ?, ?)', (patient, date, time))
    appointment_id = c.lastrowid
    conn.commit()
    conn.close()
    return appointment_id

def cancel_appointment(appointment_id):
    """
    @brief Cancels an existing appointment by its ID.

    @param appointment_id An integer representing the ID of the appointment to be canceled.

    @return True if the appointment was successfully canceled, False otherwise.
    """
    conn = sqlite3.connect('appointments.db')
    c = conn.cursor()
    c.execute('DELETE FROM appointments WHERE id = ?', (appointment_id,))
    rows_deleted = c.rowcount
    conn.commit()
    conn.close()
    return rows_deleted > 0

def get_todays_appointments():
    """
    @brief Retrieves all appointments scheduled for today.

    This function queries the SQLite database for all appointments with today's date.

    @return A list of dictionaries, each containing the appointment ID, patient name, and appointment time.
    """
    today_date = datetime.now().strftime('%Y-%m-%d')
    conn = sqlite3.connect('appointments.db')
    c = conn.cursor()
    c.execute('SELECT id, patient, date, time FROM appointments WHERE date = ?', (today_date,))
    appointments = [{'id': row[0], 'patient': row[1], 'date': row[2], 'time': row[3]} for row in c.fetchall()]
    conn.close()
    return appointments

def get_all_appointments():
    """
    @brief Retrieves all appointments from the database.

    @return A list of all scheduled appointments with their ID, patient name, date, and time.
    """
    conn = sqlite3.connect('appointments.db')
    c = conn.cursor()
    c.execute('SELECT id, patient, date, time FROM appointments')
    appointments = [{'id': row[0], 'patient': row[1], 'date': row[2], 'time': row[3]} for row in c.fetchall()]
    conn.close()
    return appointments


