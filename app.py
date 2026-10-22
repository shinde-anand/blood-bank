from flask import Flask, render_template, request, redirect, url_for, session, flash
from database import get_db_connection
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.secret_key = "blood_bank_management_secret"


# =========================================================
# HOME
# =========================================================
@app.route("/")
def home():

    if "user_id" in session:
        return redirect(url_for("dashboard"))

    return redirect(url_for("login"))


# =========================================================
# REGISTER
# =========================================================
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        role = request.form["role"]

        hashed_password = generate_password_hash(password)

        try:

            db = get_db_connection()
            cursor = db.cursor()

            cursor.execute(
                """
                INSERT INTO users
                (name, email, password, role)
                VALUES (%s, %s, %s, %s)
                """,
                (
                    name,
                    email,
                    hashed_password,
                    role
                )
            )

            db.commit()

            cursor.close()
            db.close()

            flash(
                "Registration successful! Please login.",
                "success"
            )

            return redirect(url_for("login"))

        except Exception as e:

            flash(
                f"Registration failed: {e}",
                "danger"
            )

    return render_template("register.html")


# =========================================================
# LOGIN
# =========================================================
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        db = get_db_connection()
        cursor = db.cursor(dictionary=True)

        cursor.execute(
            "SELECT * FROM users WHERE email = %s",
            (email,)
        )

        user = cursor.fetchone()

        cursor.close()
        db.close()

        if user and check_password_hash(
            user["password"],
            password
        ):

            session["user_id"] = user["id"]
            session["user_name"] = user["name"]
            session["role"] = user["role"]

            return redirect(url_for("dashboard"))

        else:

            flash(
                "Invalid email or password.",
                "danger"
            )

    return render_template("login.html")


# =========================================================
# DASHBOARD
# =========================================================
@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect(url_for("login"))

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    # Total Donors
    cursor.execute(
        "SELECT COUNT(*) AS total FROM donors"
    )

    total_donors = cursor.fetchone()["total"]

    # Total Blood Units
    cursor.execute(
        """
        SELECT COALESCE(SUM(units), 0) AS total
        FROM blood_stock
        """
    )

    total_blood_units = cursor.fetchone()["total"]

    # Total Patients
    cursor.execute(
        "SELECT COUNT(*) AS total FROM patients"
    )

    total_patients = cursor.fetchone()["total"]

    # Pending Requests
    cursor.execute(
        """
        SELECT COUNT(*) AS total
        FROM blood_requests
        WHERE status = 'Pending'
        """
    )

    pending_requests = cursor.fetchone()["total"]

    # Blood Stock
    cursor.execute(
        """
        SELECT blood_group, units
        FROM blood_stock
        ORDER BY
            FIELD(
                blood_group,
                'A+', 'A-',
                'B+', 'B-',
                'AB+', 'AB-',
                'O+', 'O-'
            )
        """
    )

    blood_stock = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template(
        "dashboard.html",
        name=session["user_name"],
        role=session["role"],
        total_donors=total_donors,
        total_blood_units=total_blood_units,
        total_patients=total_patients,
        pending_requests=pending_requests,
        blood_stock=blood_stock
    )


# =========================================================
# DONOR LIST
# =========================================================
@app.route("/donors")
def donors():

    if "user_id" not in session:
        return redirect(url_for("login"))

    search = request.args.get("search", "")

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    if search:

        cursor.execute(
            """
            SELECT *
            FROM donors
            WHERE name LIKE %s
               OR blood_group LIKE %s
               OR phone LIKE %s
            ORDER BY id DESC
            """,
            (
                f"%{search}%",
                f"%{search}%",
                f"%{search}%"
            )
        )

    else:

        cursor.execute(
            """
            SELECT *
            FROM donors
            ORDER BY id DESC
            """
        )

    donor_list = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template(
        "donors.html",
        donors=donor_list,
        search=search
    )


# =========================================================
# ADD DONOR
# =========================================================
@app.route("/add-donor", methods=["GET", "POST"])
def add_donor():

    if "user_id" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":

        name = request.form["name"]
        age = request.form["age"]
        gender = request.form["gender"]
        blood_group = request.form["blood_group"]
        phone = request.form["phone"]
        email = request.form["email"]
        address = request.form["address"]
        last_donation_date = request.form["last_donation_date"]

        db = get_db_connection()
        cursor = db.cursor()

        cursor.execute(
            """
            INSERT INTO donors
            (
                name,
                age,
                gender,
                blood_group,
                phone,
                email,
                address,
                last_donation_date
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                name,
                age,
                gender,
                blood_group,
                phone,
                email,
                address,
                last_donation_date
                if last_donation_date
                else None
            )
        )

        db.commit()

        cursor.close()
        db.close()

        flash(
            "Donor added successfully!",
            "success"
        )

        return redirect(url_for("donors"))

    return render_template("add_donor.html")


# =========================================================
# EDIT DONOR
# =========================================================
@app.route(
    "/edit-donor/<int:donor_id>",
    methods=["GET", "POST"]
)
def edit_donor(donor_id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    if request.method == "POST":

        name = request.form["name"]
        age = request.form["age"]
        gender = request.form["gender"]
        blood_group = request.form["blood_group"]
        phone = request.form["phone"]
        email = request.form["email"]
        address = request.form["address"]
        last_donation_date = request.form[
            "last_donation_date"
        ]

        cursor.execute(
            """
            UPDATE donors
            SET
                name=%s,
                age=%s,
                gender=%s,
                blood_group=%s,
                phone=%s,
                email=%s,
                address=%s,
                last_donation_date=%s
            WHERE id=%s
            """,
            (
                name,
                age,
                gender,
                blood_group,
                phone,
                email,
                address,
                last_donation_date
                if last_donation_date
                else None,
                donor_id
            )
        )

        db.commit()

        cursor.close()
        db.close()

        flash(
            "Donor updated successfully!",
            "success"
        )

        return redirect(url_for("donors"))

    cursor.execute(
        "SELECT * FROM donors WHERE id=%s",
        (donor_id,)
    )

    donor = cursor.fetchone()

    cursor.close()
    db.close()

    return render_template(
        "edit_donor.html",
        donor=donor
    )


# =========================================================
# DELETE DONOR
# =========================================================
@app.route("/delete-donor/<int:donor_id>")
def delete_donor(donor_id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    db = get_db_connection()
    cursor = db.cursor()

    cursor.execute(
        "DELETE FROM donors WHERE id=%s",
        (donor_id,)
    )

    db.commit()

    cursor.close()
    db.close()

    flash(
        "Donor deleted successfully!",
        "success"
    )

    return redirect(url_for("donors"))


# =========================================================
# BLOOD STOCK
# =========================================================
@app.route("/blood-stock")
def blood_stock():

    if "user_id" not in session:
        return redirect(url_for("login"))

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT *
        FROM blood_stock
        ORDER BY
            FIELD(
                blood_group,
                'A+', 'A-',
                'B+', 'B-',
                'AB+', 'AB-',
                'O+', 'O-'
            )
        """
    )

    stock = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template(
        "blood_stock.html",
        stock=stock
    )


# =========================================================
# UPDATE BLOOD STOCK
# =========================================================
@app.route("/update-stock", methods=["POST"])
def update_stock():

    if "user_id" not in session:
        return redirect(url_for("login"))

    blood_group = request.form["blood_group"]
    units = int(request.form["units"])
    action = request.form["action"]

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT units
        FROM blood_stock
        WHERE blood_group=%s
        """,
        (blood_group,)
    )

    current = cursor.fetchone()

    if not current:

        cursor.close()
        db.close()

        flash(
            "Blood group not found.",
            "danger"
        )

        return redirect(url_for("blood_stock"))

    current_units = current["units"]

    if action == "add":

        new_units = current_units + units

    elif action == "remove":

        if units > current_units:

            cursor.close()
            db.close()

            flash(
                "Cannot remove more units than available stock.",
                "danger"
            )

            return redirect(url_for("blood_stock"))

        new_units = current_units - units

    else:

        cursor.close()
        db.close()

        flash(
            "Invalid action.",
            "danger"
        )

        return redirect(url_for("blood_stock"))

    cursor.execute(
        """
        UPDATE blood_stock
        SET units=%s
        WHERE blood_group=%s
        """,
        (
            new_units,
            blood_group
        )
    )

    db.commit()

    cursor.close()
    db.close()

    flash(
        f"{blood_group} blood stock updated successfully!",
        "success"
    )

    return redirect(url_for("blood_stock"))


# =========================================================
# PATIENT LIST
# =========================================================
@app.route("/patients")
def patients():

    if "user_id" not in session:
        return redirect(url_for("login"))

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT *
        FROM patients
        ORDER BY id DESC
        """
    )

    patient_list = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template(
        "patients.html",
        patients=patient_list
    )


# =========================================================
# ADD PATIENT
# =========================================================
@app.route("/add-patient", methods=["GET", "POST"])
def add_patient():

    if "user_id" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":

        name = request.form["name"]
        age = request.form["age"]
        gender = request.form["gender"]
        blood_group = request.form["blood_group"]
        phone = request.form["phone"]
        hospital = request.form["hospital"]
        address = request.form["address"]

        db = get_db_connection()
        cursor = db.cursor()

        cursor.execute(
            """
            INSERT INTO patients
            (
                name,
                age,
                gender,
                blood_group,
                phone,
                hospital,
                address
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (
                name,
                age,
                gender,
                blood_group,
                phone,
                hospital,
                address
            )
        )

        db.commit()

        cursor.close()
        db.close()

        flash(
            "Patient added successfully!",
            "success"
        )

        return redirect(url_for("patients"))

    return render_template(
        "add_patient.html"
    )


# =========================================================
# BLOOD REQUEST LIST
# =========================================================
@app.route("/blood-requests")
def blood_requests():

    if "user_id" not in session:
        return redirect(url_for("login"))

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT
            br.id,
            br.blood_group,
            br.units_required,
            br.hospital,
            br.request_date,
            br.status,
            p.name AS patient_name,
            p.phone AS patient_phone
        FROM blood_requests br
        JOIN patients p
            ON br.patient_id = p.id
        ORDER BY br.id DESC
        """
    )

    requests_list = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template(
        "blood_requests.html",
        requests=requests_list
    )


# =========================================================
# ADD BLOOD REQUEST
# =========================================================
@app.route("/add-request", methods=["GET", "POST"])
def add_request():

    if "user_id" not in session:
        return redirect(url_for("login"))

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    if request.method == "POST":

        patient_id = request.form["patient_id"]
        blood_group = request.form["blood_group"]
        units_required = int(
            request.form["units_required"]
        )
        hospital = request.form["hospital"]

        cursor.execute(
            """
            INSERT INTO blood_requests
            (
                patient_id,
                blood_group,
                units_required,
                hospital
            )
            VALUES (%s, %s, %s, %s)
            """,
            (
                patient_id,
                blood_group,
                units_required,
                hospital
            )
        )

        db.commit()

        cursor.close()
        db.close()

        flash(
            "Blood request submitted successfully!",
            "success"
        )

        return redirect(
            url_for("blood_requests")
        )

    cursor.execute(
        """
        SELECT id, name, blood_group
        FROM patients
        ORDER BY name
        """
    )

    patient_list = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template(
        "add_request.html",
        patients=patient_list
    )


# =========================================================
# LOGOUT
# =========================================================
@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("login"))


# =========================================================
# RUN APPLICATION
# =========================================================
if __name__ == "__main__":
    app.run(debug=True)
