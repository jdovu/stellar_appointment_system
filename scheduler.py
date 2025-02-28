
"""
 * @file scheduler.py
 * @brief Main microservice handling appointment requests using ZeroMQ.
"""

import zmq
import json
import database
import datetime

# Setup ZeroMQ server for handling appointment requests
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

# Initialize the SQLite database
database.init_db()

# Microservice loop to handle incoming appointment-related requests
while True:
    # Receive a request from the client
    message = socket.recv_string()
    request = json.loads(message)
    response = {}

    # Handle different actions based on the request data
    action = request.get("action")
    if action == "schedule":
        """
        @brief Handles scheduling of an appointment.

        Extracts patient name, date, and time from the request and schedules an appointment.

        @param patient A string containing the patient's name.
        @param date A string representing the appointment date (YYYY-MM-DD).
        @param time A string representing the appointment time (HH:MM format).

        @return JSON response with a success status and newly created appointment ID.
        """
        patient = request.get("patient")
        date = request.get("date")
        time = request.get("time")
        # CALL OUT!!!
        # 03 - Call the database function to schedule a new appointment
        appointment_id = database.schedule_appointment(patient, date, time)
        response = {"status": "success", "appointment_id": appointment_id}
    elif action == "cancel":
        """
        @brief Handles appointment cancellation.

        Cancels an existing appointment using the provided appointment ID.

        @param appointment_id An integer representing the ID of the appointment to cancel.

        @return JSON response indicating whether the cancellation was successful.
        """
        appointment_id = request.get("appointment_id")
        success = database.cancel_appointment(appointment_id)
        response = {
            "status": "success",
            "message": f"Appointment {appointment_id} canceled."
        } if success else {
            "status": "error",
            "message": "Appointment not found."
        }
    elif action == "view_today":
        """
        @brief Retrieves all of today's appointments.

        @return JSON response containing a list of appointments scheduled for today.
        """
        appointments = database.get_todays_appointments()
        response = {"appointments": appointments}
    elif action == "view_all":
        """
        @brief Retrieves all scheduled appointments.

        @return JSON response containing a list of all appointments.
        """
        appointments = database.get_all_appointments()
        response = {"appointments": appointments}
    else:
        """
        @brief Handles invalid requests.

        @return JSON response indicating an invalid action was requested.
        """
        response = {"status": "error", "message": "Invalid action."}

    # CALL OUT!!!
    # 05 - Send the processed response back to api.py through ZeroMQ
    socket.send_string(json.dumps(response))
