import flask
import logging
import psycopg2
import time
import random
import datetime
import jwt
from functools import wraps

from flask import Flask, request, jsonify
import psycopg2
from psycopg2 import sql
import logging

'''
# ------ SENHA PARA O ADMINISTRADOR ------
from werkzeug.security import generate_password_hash
print()
print(generate_password_hash('admin123'))
print()
'''

from werkzeug.security import generate_password_hash, check_password_hash

app = flask.Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'some_jwt_secret_key'

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

StatusCodes = {
    'success': 200,
    'api_error': 400,
    'internal_error': 500,
    'unauthorized': 401,
    'not_found': 404
}

##########################################################
## DATABASE ACCESS
##########################################################

def db_connection():
    db = psycopg2.connect(
        user='userprojeto',
        password='raphaelyoshio25',
        host='127.0.0.1',
        port='5432',
        database='projetoDB'
    )
    return db

##########################################################
## AUTHENTICATION HELPERS
##########################################################

def get_user_role(user_id):
    conn = db_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT role FROM person WHERE person_id = %s", (user_id,))
        result = cur.fetchone()
        return result[0] if result else None
    except Exception as e:
        logger.error(f"Error getting user role: {str(e)}")
        return None
    finally:
        cur.close()
        conn.close()

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = flask.request.headers.get('Authorization')
        logger.info(f'Token: {token}')

        if not token or not token.startswith("Bearer "):
            return flask.jsonify({'status': StatusCodes['unauthorized'], 'errors': 'Token is missing or invalid!', 'results': None})

        token = token.split(" ")[1]

        try:
            data = jwt.decode(token, app.config['JWT_SECRET_KEY'], algorithms=["HS256"])
            user_id = data["id"]
            user_role = get_user_role(user_id)
            
            if not user_role:
                return flask.jsonify({'status': StatusCodes['unauthorized'], 'errors': 'User not found!', 'results': None})
            
            # Add user_id and role to the request context
            flask.g.user_id = user_id
            flask.g.user_role = user_role
            
            logger.info(f'Token válido para utilizador: {user_id} com role: {user_role}')
        except jwt.ExpiredSignatureError:
            return flask.jsonify({'status': StatusCodes['unauthorized'], 'errors': 'Token expirado!', 'results': None})
        except jwt.InvalidTokenError:
            return flask.jsonify({'status': StatusCodes['unauthorized'], 'errors': 'Token inválido!', 'results': None})

        return f(*args, **kwargs)
    return decorated

##########################################################
## ENDPOINTS
##########################################################

# === ENDPOINT PARA LISTAR PESSOAS ===
@app.route('/person', methods=['GET'])
def get_all_person():
    conn = db_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
            SELECT 
                p.person_id, p.email, p.name, p.phone_number, p.address, p.role,
                s.area,
                i.department
            FROM person p
            LEFT JOIN student s ON p.person_id = s.person_person_id
            LEFT JOIN instructor i ON p.person_id = i.employee_person_person_id
        """)
        rows = cur.fetchall()

        results = []
        for row in rows:
            person = {
                'person_id': row[0],
                'email': row[1],
                'name': row[2],
                'phone_number': row[3],
                'address': row[4],
                'role': row[5]
            }
            if row[6]:  # area
                person['area'] = row[6]
            if row[7]:  # department
                person['department'] = row[7]
            results.append(person)

        response = {'status': 'success', 'results': results}
    except Exception as e:
        response = {'status': 'internal_error', 'errors': str(e)}
    finally:
        conn.close()

    return flask.jsonify(response)

# === ENDPOINTS DE REGISTO DE UTILIZADORES ===
def check_staff_permission():
    if not hasattr(flask.g, 'user_role') or flask.g.user_role != 'staff':
        return False
    return True

@app.route('/register/student', methods=['POST'])
@token_required
def register_student():
    if not check_staff_permission():
        return jsonify({'status': 'unauthorized', 'errors': 'Only staff members can register students', 'results': None})

    data = request.get_json()
    required_fields = ['email', 'name', 'phone_number', 'address', 'password', 
                      'date_of_birth', 'area']
    
    if not all(field in data for field in required_fields):
        return jsonify({'status': 'api_error', 'errors': 'Missing required fields', 'results': None})

    conn = db_connection()
    cur = conn.cursor()

    try:
        # Check if email already exists
        cur.execute("SELECT * FROM person WHERE email = %s", (data['email'],))
        if cur.fetchone():
            return jsonify({'status': 'api_error', 'errors': 'Email already registered', 'results': None})

        # Insert into person table
        hashed_password = generate_password_hash(data['password'])
        cur.execute("""
            INSERT INTO person (email, name, phone_number, address, password, role)
            VALUES (%s, %s, %s, %s, %s, 'student')
            RETURNING person_id
        """, (data['email'], data['name'], data['phone_number'], 
              data['address'], hashed_password))
        
        person_id = cur.fetchone()[0]

        # Insert into student table
        cur.execute("""
            INSERT INTO student (person_person_id, date_of_birth, area)
            VALUES (%s, %s, %s)
        """, (person_id, data['date_of_birth'], data['area']))

        conn.commit()
        return jsonify({'status': 'success', 'message': 'Student registered successfully', 'results': None})

    except Exception as e:
        conn.rollback()
        return jsonify({'status': 'internal_error', 'errors': str(e), 'results': None})
    finally:
        cur.close()
        conn.close()

@app.route('/register/staff', methods=['POST'])
@token_required
def register_staff():
    if not check_staff_permission():
        return jsonify({'status': 'unauthorized', 'errors': 'Only staff members can register staff', 'results': None})

    data = request.get_json()
    required_fields = ['email', 'name', 'phone_number', 'address', 'password']
    
    if not all(field in data for field in required_fields):
        return jsonify({'status': 'api_error', 'errors': 'Missing required fields', 'results': None})

    conn = db_connection()
    cur = conn.cursor()

    try:
        # Check if email already exists
        cur.execute("SELECT * FROM person WHERE email = %s", (data['email'],))
        if cur.fetchone():
            return jsonify({'status': 'api_error', 'errors': 'Email already registered', 'results': None})

        # Insert into person table
        hashed_password = generate_password_hash(data['password'])
        cur.execute("""
            INSERT INTO person (email, name, phone_number, address, password, role)
            VALUES (%s, %s, %s, %s, %s, 'staff')
            RETURNING person_id
        """, (data['email'], data['name'], data['phone_number'], 
              data['address'], hashed_password))
        
        person_id = cur.fetchone()[0]

        # Insert into employee table
        cur.execute("""
            INSERT INTO employee (person_person_id, hire_date)
            VALUES (%s,CURRENT_DATE)
        """, (person_id,))

        # Insert into admstaff table
        cur.execute("""
            INSERT INTO admstaff (employee_person_person_id)
            VALUES (%s)
        """, (person_id,))

        conn.commit()
        return jsonify({'status': 'success', 'message': 'Staff registered successfully', 'results': None})

    except Exception as e:
        conn.rollback()
        return jsonify({'status': 'internal_error', 'errors': str(e), 'results': None})
    finally:
        cur.close()
        conn.close()

@app.route('/register/instructor', methods=['POST'])
@token_required
def register_instructor():
    if not check_staff_permission():
        return jsonify({'status': 'unauthorized', 'errors': 'Only staff members can register instructors', 'results': None})

    data = request.get_json()
    required_fields = ['email', 'name', 'phone_number', 'address', 'password', 'department']
    
    if not all(field in data for field in required_fields):
        return jsonify({'status': 'api_error', 'errors': 'Missing required fields', 'results': None})

    conn = db_connection()
    cur = conn.cursor()

    try:
        # Check if email already exists
        cur.execute("SELECT * FROM person WHERE email = %s", (data['email'],))
        if cur.fetchone():
            return jsonify({'status': 'api_error', 'errors': 'Email already registered', 'results': None})

        # Insert into person table
        hashed_password = generate_password_hash(data['password'])
        cur.execute("""
            INSERT INTO person (email, name, phone_number, address, password, role)
            VALUES (%s, %s, %s, %s, %s, 'instructor')
            RETURNING person_id
        """, (data['email'], data['name'], data['phone_number'], 
              data['address'], hashed_password))
        
        person_id = cur.fetchone()[0]

        # Insert into employee table
        cur.execute("""
            INSERT INTO employee (person_person_id, hire_date)
            VALUES (%s, CURRENT_DATE)
        """, (person_id,))

        # Insert into instructor table
        cur.execute("""
            INSERT INTO instructor (employee_person_person_id, department)
            VALUES (%s, %s)
        """, (person_id, data['department']))

        conn.commit()
        return jsonify({'status': 'success', 'message': 'Instructor registered successfully', 'results': None})

    except Exception as e:
        conn.rollback()
        return jsonify({'status': 'internal_error', 'errors': str(e), 'results': None})
    finally:
        cur.close()
        conn.close()

# === ENDPOINT DE LOGIN ===
@app.route('/login', methods=['PUT'])
def login_user():
    data = flask.request.get_json()
    email = data.get('email')  
    password = data.get('password')

    if not email or not password:
        return flask.jsonify({'status': 'api_error', 'errors': 'Email and password are required', 'results': None})

    try:
        conn = db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT person_id, password FROM person WHERE email = %s", (email,))
        user = cursor.fetchone()
        conn.close()

        if not user:
            return flask.jsonify({'status': 'unauthorized', 'errors': 'Invalid credentials', 'results': None})

        user_id, hashed_password = user

        # Verifica se a senha fornecida corresponde ao hash armazenado
        if not check_password_hash(hashed_password, password):
            return flask.jsonify({'status': 'unauthorized', 'errors': 'Invalid credentials', 'results': None})

        # Geração do token com ID da pessoa e tempo de expiração
        token = jwt.encode({'id': user[0]}, app.config['JWT_SECRET_KEY'], algorithm="HS256")

        response = {'status': 'success', 'errors': None, 'results': token}
        return flask.jsonify(response)

    except Exception as e:
        return flask.jsonify({'status': 'internal_error', 'errors': str(e), 'results': None})


# === ENDPOINT PARA REMOVER TODOS OS DADOS DE UM ESTUDANTE ===
@app.route('/delete_student/<int:student_id>', methods=['DELETE'])
@token_required
def delete_student(student_id):
    if not check_staff_permission():
        return jsonify({'status': StatusCodes['unauthorized'], 'errors': 'Only staff can delete student data', 'results': None})

    conn = db_connection()
    cur = conn.cursor()

    try:
        # Verifica se o estudante existe
        cur.execute("SELECT * FROM person WHERE person_id = %s AND role = 'student'", (student_id,))
        student = cur.fetchone()

        if not student:
            return jsonify({
                'status': StatusCodes['not_found'],
                'errors': f'Student with ID {student_id} not found',
                'results': None
            })

        # Remove dados relacionados em outras tabelas
        cur.execute("DELETE FROM student_activity WHERE student_id = %s", (student_id,))
        cur.execute("DELETE FROM student_courseedition WHERE student_id = %s", (student_id,))
        cur.execute("DELETE FROM subject_grade WHERE student_person_person_id = %s", (student_id,))
        # Remove da tabela student e da person
        cur.execute("DELETE FROM student WHERE person_person_id = %s", (student_id,))
        cur.execute("DELETE FROM person WHERE person_id = %s", (student_id,))

        conn.commit()

        return jsonify({
            'status': StatusCodes['success'],
            'errors': None,
            'results': f'All data for student with ID {student_id} deleted successfully'
        })

    except Exception as e:
        conn.rollback()
        return jsonify({
            'status': StatusCodes['internal_error'],
            'errors': str(e),
            'results': None
        })
    finally:
        cur.close()
        conn.close()

# === ENDPOINTS PARA LISTAR USUÁRIOS ===
@app.route('/students', methods=['GET'])
@token_required
def get_students():
    conn = db_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
            SELECT p.person_id, p.email, p.name, p.phone_number, p.address,
                   s.date_of_birth, s.area
            FROM person p
            JOIN student s ON p.person_id = s.person_person_id
            WHERE p.role = 'student'
        """)
        rows = cur.fetchall()

        results = []
        for row in rows:
            results.append({
                'person_id': row[0],
                'email': row[1],
                'name': row[2],
                'phone_number': row[3],
                'address': row[4],
                'date_of_birth': row[5],
                'area': row[6]
            })

        return jsonify({'status': 'success', 'results': results})

    except Exception as e:
        return jsonify({'status': 'internal_error', 'errors': str(e), 'results': None})
    finally:
        cur.close()
        conn.close()

@app.route('/staff', methods=['GET'])
@token_required
def get_staff():
    if not check_staff_permission():
        return jsonify({'status': 'unauthorized', 'errors': 'Only staff members can access this endpoint', 'results': None})

    conn = db_connection()
    cur = conn.cursor()

    try:
        # Get all staff and instructors
        cur.execute("""
            SELECT p.person_id, p.email, p.name, p.phone_number, p.address, p.role,
                   CASE 
                       WHEN p.role = 'instructor' THEN i.department
                       ELSE NULL
                   END as department
            FROM person p
            LEFT JOIN instructor i ON p.person_id = i.employee_person_person_id
            WHERE p.role IN ('staff', 'instructor')
        """)
        rows = cur.fetchall()

        results = []
        for row in rows:
            staff_info = {
                'person_id': row[0],
                'email': row[1],
                'name': row[2],
                'phone_number': row[3],
                'address': row[4],
                'role': row[5]
            }
            if row[6]:  # department (only for instructors)
                staff_info['department'] = row[6]
            
            results.append(staff_info)

        return jsonify({'status': 'success', 'results': results})

    except Exception as e:
        return jsonify({'status': 'internal_error', 'errors': str(e), 'results': None})
    finally:
        cur.close()
        conn.close()

# === ENDPOINT DE LOGOUT ===
@app.route('/logout', methods=['POST'])
def logout():
    return jsonify({
        'status': 'success',
        'message': 'Sessão encerrada com sucesso. Por favor, descarte o token de autenticação.',
        'results': None
    })

# === ENDPOINT PARA LISTAR AS ÁREAS DISPONÍVEIS PARA INSCRIÇÃO ===
@app.route('/list_areas', methods=['GET'])
@token_required
def list_areas():
    if flask.g.user_role != 'student':
        return jsonify({
            'status': StatusCodes['unauthorized'],
            'errors': 'Only students can view available areas',
            'results': None
        })

    conn = db_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
            SELECT type, duration
            FROM degreeprogram
        """)
        rows = cur.fetchall()

        results = [{
            'area': row[0],
            'duration_years': row[1]
        } for row in rows]

        return jsonify({
            'status': StatusCodes['success'],
            'errors': None,
            'results': results
        })

    except Exception as e:
        return jsonify({
            'status': StatusCodes['internal_error'],
            'errors': str(e),
            'results': None
        })
    finally:
        cur.close()
        conn.close()

# === ENDPOINT PARA ASSOCIAR UM ESTUDANTE A UM DEGREEPROGRAM ===
@app.route('/enroll_degree/<string:type>', methods=['POST'])
@token_required
def enroll_degree(type):
    """
    Associa um estudante autenticado ao degreeprogram especificado (type).
    O type é o nome/type do degreeprogram/curso.
    """
    if flask.g.user_role != 'staff':
        return jsonify({
            'status': StatusCodes['unauthorized'],
            'errors': 'Only staff members can enroll a student to a degree program',
            'results': None
        })
    
    data = request.get_json()
    student_id = int(data.get("student_id"))
    conn = db_connection()
    cur = conn.cursor()
    try:
        # Verifica se o estudante existe
        cur.execute("SELECT * FROM student WHERE person_person_id = %s", (student_id,))
        student_row = cur.fetchone()
        if not student_row:
            return jsonify({'status': StatusCodes['not_found'], 'errors': 'Student not found', 'results': None})

        # Considera que o nome do curso do estudante já é o type do degreeprogram
        cur.execute("SELECT area FROM student WHERE person_person_id = %s", (student_id,))
        student_area_row = cur.fetchone()
        if not student_area_row:
            return jsonify({'status': StatusCodes['not_found'], 'errors': 'Student\'s area not found', 'results': None})

        student_area = student_area_row[0]
        if student_area != type:
            return jsonify({'status': StatusCodes['api_error'], 'errors': 'Student was not registered in this degree program', 'results': None})

        # Aqui faria associação do estudante ao degreeprogram, se necessário (pode ser lógica dummy)
        # Exemplo: inserir em uma tabela de associação, se existir
        # No exemplo, apenas retorna sucesso
        return jsonify({'status': StatusCodes['success'], 'message': f'Student {student_id} is associated with degree program {type}', 'results': None})

    except Exception as e:
        return jsonify({'status': StatusCodes['internal_error'], 'errors': str(e), 'results': None})
    finally:
        cur.close()
        conn.close()

@app.route('/activities', methods=['GET'])
def list_activities():
    conn = db_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT activity_id, name, fee FROM activity")
        rows = cur.fetchall()

        results = [{
            'activity_id': r[0],
            'name': r[1],
            'fee': r[2],
        } for r in rows]

        return jsonify({'status': StatusCodes['success'], 'results': results})
    except Exception as e:
        return jsonify({'status': StatusCodes['internal_error'], 'errors': str(e), 'results': None})
    finally:
        cur.close()
        conn.close()

@app.route('/enroll_activity/<int:activity_id>', methods=['POST'])
@token_required
def enroll_activity(activity_id):
    if flask.g.user_role != 'student':
        return jsonify({
            'status': StatusCodes['unauthorized'],
            'errors': 'Only students can enroll in activities',
            'results': None
        })

    student_id = flask.g.user_id
    conn = db_connection()
    cur = conn.cursor()

    try:
        # Verify if activity exists
        cur.execute("SELECT activity_id FROM activity WHERE activity_id = %s", (activity_id,))
        if not cur.fetchone():
            return jsonify({
                'status': StatusCodes['not_found'],
                'errors': 'Activity not found',
                'results': None
            })

        # Insert enrollment
        cur.execute("""
            INSERT INTO student_activity 
            (student_id, activity_id)
            VALUES (%s, %s)
        """, (student_id, activity_id))

        conn.commit()
        return jsonify({
            'status': StatusCodes['success'],
            'errors': None,
            'results': 'Successfully enrolled in activity'
        })

    except Exception as e:
        conn.rollback()
        return jsonify({
            'status': StatusCodes['internal_error'],
            'errors': str(e),
            'results': None
        })
    finally:
        cur.close()
        conn.close()


# === ENDPOINT PARA LISTAR CURSOS/CADEIRAS DISPONÍVEIS AO ESTUDANTE ===
@app.route('/list_courses', methods=['GET'])
@token_required
def list_courses():
    # Apenas estudantes podem consultar
    if flask.g.user_role != 'student':
        return jsonify({
            'status': StatusCodes['unauthorized'],
            'errors': 'Only students can view all courses',
            'results': None
        })

    student_id = flask.g.user_id
    conn = db_connection()
    cur  = conn.cursor()

    try:
        # 1. Obter a área / degree program do estudante
        cur.execute("""
            SELECT area
            FROM student
            WHERE person_person_id = %s
        """, (student_id,))
        row = cur.fetchone()
        if not row:
            return jsonify({'status': StatusCodes['not_found'],
                            'errors': 'Student not found',
                            'results': None})
        student_area = row[0]

        # 2. Listar edições de curso do mesmo programa com vagas
        cur.execute("""
            SELECT
                ce.edition_id,
                ce.edition_year,
                ce.semester,
                ce.capacity,
                c.course_id,
                c.name,
                ce.capacity
                    - COALESCE(
                        (SELECT COUNT(*)
                         FROM student_courseedition sce
                         WHERE sce.course_edition_id = ce.edition_id), 0
                      ) AS remaining_slots
            FROM courseedition ce
            JOIN course c                ON c.course_id = ce.course_course_id
            JOIN course_degreeprogram cd ON cd.course_course_id = c.course_id
            WHERE cd.degreeprogram_type = %s
              AND (ce.capacity
                   - COALESCE(
                       (SELECT COUNT(*)
                        FROM student_courseedition sce
                        WHERE sce.course_edition_id = ce.edition_id), 0)
                  ) > 0
            ORDER BY ce.edition_year DESC, ce.semester, c.name
        """, (student_area,))

        rows = cur.fetchall()
        results = [{
            'course_edition_id': r[0],
            'year'             : r[1],
            'semester'         : r[2],
            'capacity'         : r[3],
            'course_id'        : r[4],
            'course_name'      : r[5],
            'remaining_slots'  : r[6]
        } for r in rows]

        return jsonify({'status': StatusCodes['success'],
                        'errors': None,
                        'results': results})

    except Exception as e:
        return jsonify({'status': StatusCodes['internal_error'],
                        'errors': str(e),
                        'results': None})
    finally:
        cur.close()
        conn.close()

@app.route('/enroll_course_edition/<int:course_edition_id>', methods=['POST'])
@token_required
def enroll_course_edition(course_edition_id):
    if flask.g.user_role != 'student':
        return jsonify({'status': StatusCodes['unauthorized'], 'errors': 'Only students can enroll in course editions', 'results': None})

    student_id = flask.g.user_id
    conn = db_connection()
    cur = conn.cursor()

    try:
        # 1. Obter curso do estudante
        cur.execute("SELECT area FROM student WHERE person_person_id = %s", (student_id,))
        row = cur.fetchone()
        if not row:
            return jsonify({'status': StatusCodes['not_found'], 'errors': 'Student not found', 'results': None})

        student_area = row[0]

        # 2. Obter course_id da edição
        cur.execute("SELECT course_course_id FROM courseedition WHERE edition_id = %s", (course_edition_id,))
        row = cur.fetchone()
        if not row:
            return jsonify({'status': StatusCodes['not_found'], 'errors': 'Course edition not found', 'results': None})

        edition_course_id = row[0]

        # 3. Verificar se essa cadeira faz parte do curso do aluno
        cur.execute("""
            SELECT 1 FROM course_degreeprogram 
            WHERE course_course_id = %s AND degreeprogram_type = %s
        """, (edition_course_id, student_area))
        if not cur.fetchone():
            return jsonify({'status': StatusCodes['unauthorized'], 'errors': 'This course is not part of your program', 'results': None})

        # 4. Registrar inscrição
        cur.execute("""
            INSERT INTO student_courseedition (student_id, course_edition_id)
            VALUES (%s, %s) ON CONFLICT DO NOTHING
        """, (student_id, course_edition_id))

        conn.commit()
        return jsonify({'status': StatusCodes['success'], 'results': f'Student {student_id} enrolled in course edition {course_edition_id}'})

    except Exception as e:
        conn.rollback()
        return jsonify({'status': StatusCodes['internal_error'], 'errors': str(e), 'results': None})
    finally:
        cur.close()
        conn.close()

# === ENDPOINT DE SUBMISSÃO DE NOTAS ===
@app.route('/submit_grades', methods=['POST'])
@token_required
def submit_grades():
    if flask.g.user_role != 'instructor':
        return jsonify({
            'status': 'unauthorized',
            'errors': 'Only instructors can submit grades.',
            'results': None
        })

    data = request.get_json()
    required_fields = ['course_id', 'period', 'grades']
    if not all(field in data for field in required_fields):
        return jsonify({
            'status': 'api_error',
            'errors': 'Missing required fields: course_id, period, grades',
            'results': None
        })

    course_id = data['course_id']
    period = data['period']
    grades = data['grades']  # Expecting list of [student_id, grade]

    conn = db_connection()
    cur = conn.cursor()

    inserted = 0
    skipped = 0

    try:
        # Get the degreeprogram_type(s) this course is part of
        cur.execute("""
            SELECT degreeprogram_type
            FROM course_degreeprogram
            WHERE course_course_id = %s
        """, (course_id,))
        course_programs = cur.fetchall()
        valid_programs = {row[0] for row in course_programs}

        if not valid_programs:
            return jsonify({
                'status': 'not_found',
                'errors': 'Course not associated with any degree program.',
                'results': None
            })

        for student_id, grade in grades:
            # Get student's course area
            cur.execute("""
                SELECT area FROM student WHERE person_person_id = %s
            """, (student_id,))
            student_row = cur.fetchone()

            if not student_row:
                skipped += 1
                continue

            student_area = student_row[0]

            if student_area not in valid_programs:
                skipped += 1
                continue

            # Insert grade
            cur.execute("""
                INSERT INTO subject_grade (
                    grade_grade, grade_evaluation_period, student_person_person_id, course_course_id
                ) VALUES (%s, %s, %s, %s)
            """, (grade, period, student_id, course_id))
            inserted += 1

        conn.commit()
        return jsonify({
            'status': 'success',
            'inserted': inserted,
            'skipped': skipped,
            'results': None
        })

    except Exception as e:
        conn.rollback()
        return jsonify({
            'status': 'internal_error',
            'errors': str(e),
            'results': None
        })
    finally:
        cur.close()
        conn.close()

@app.route('/degree_details/<string:degree_id>', methods=['GET'])
@token_required
def degree_details(degree_id):
    if not check_staff_permission():
        return jsonify({'status': StatusCodes['unauthorized'], 'errors': 'Only staff can access degree details', 'results': None})

    conn = db_connection()
    cur = conn.cursor()

    try:
        query = """
        SELECT
            c.course_id,
            c.name AS course_name,
            ce.edition_id AS course_edition_id,
            ce.edition_year AS course_edition_year,
            ce.capacity,
            ce.instructor_employee_person_person_id AS coordinator_id,
            (
                SELECT COUNT(*)
                FROM student_courseedition sce
                WHERE sce.course_edition_id = ce.edition_id
            ) AS enrolled_count,
            (
                SELECT COUNT(*)
                FROM subject_grade sg
                WHERE sg.course_course_id = c.course_id AND sg.grade_grade >= 10
            ) AS approved_count,
            (
                SELECT ARRAY_AGG(ic.instructor_employee_person_person_id)
                FROM instructor_course ic
                WHERE ic.course_course_id = c.course_id
            ) AS instructors
        FROM
            course c
        JOIN course_degreeprogram cd ON cd.course_course_id = c.course_id
        LEFT JOIN courseedition ce ON ce.course_course_id = c.course_id
        WHERE cd.degreeprogram_type = %s
        ORDER BY ce.edition_year DESC
        """

        cur.execute(query, (degree_id,))
        rows = cur.fetchall()

        results = []
        for row in rows:
            results.append({
                "course_id": row[0],
                "course_name": row[1],
                "course_edition_id": row[2],
                "course_edition_year": row[3],
                "capacity": row[4],
                "coordinator_id": row[5],
                "enrolled_count": row[6],
                "approved_count": row[7],
                "instructors": row[8] if row[8] else []
            })

        return jsonify({
            "status": StatusCodes['success'],
            "errors": None,
            "results": results
        })

    except Exception as e:
        conn.rollback()
        return jsonify({
            "status": StatusCodes['internal_error'],
            "errors": str(e),
            "results": None
        })
    finally:
        cur.close()
        conn.close()
        
@app.route('/top3', methods=['GET'])
@token_required
def top_3_students():
    if not check_staff_permission():
        return jsonify({'status': StatusCodes['unauthorized'], 'errors': 'Only staff can access degree details', 'results': None})

    conn = db_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
            SELECT 
                p.name,
                p.email,
                ROUND(AVG(sg.grade_grade)::numeric, 2) AS average_grade
            FROM subject_grade sg
            JOIN student s ON sg.student_person_person_id = s.person_person_id
            JOIN person p ON s.person_person_id = p.person_id
            GROUP BY p.name, p.email
            ORDER BY average_grade DESC
            LIMIT 3
        """)

        rows = cur.fetchall()
        results = []

        for row in rows:
            results.append({
                'name': row[0],
                'email': row[1],
                'average_grade': float(row[2])
            })

        return jsonify({'status': 'success', 'errors': None, 'results': results})

    except Exception as e:
        return jsonify({'status': 'internal_error', 'errors': str(e), 'results': None})

    finally:
        cur.close()
        conn.close()

'''
@app.route('/report', methods=['GET'])
@token_required
def get_monthly_report():
    if flask.g.user_role != 'staff':
        return jsonify({
            'status': StatusCodes['unauthorized'],
            'errors': 'Only staff members can view monthly reports',
            'results': None
        })

    conn = db_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
            WITH monthly_stats AS (
                SELECT 
                    DATE_TRUNC('month', sg.grade_date) as month,
                    ce.course_edition_id,
                    c.name as course_name,
                    COUNT(DISTINCT CASE WHEN sg.grade >= 10 THEN sg.student_person_person_id END) as approved_count,
                    COUNT(DISTINCT sg.student_person_person_id) as total_count
                FROM subject_grade sg
                JOIN course_edition ce ON ce.course_edition_id = sg.course_edition_course_edition_id
                JOIN course c ON c.course_id = ce.course_course_id
                WHERE sg.grade_date >= CURRENT_DATE - INTERVAL '12 months'
                GROUP BY DATE_TRUNC('month', sg.grade_date), ce.course_edition_id, c.name
            ),
            monthly_best_courses AS (
                SELECT 
                    month,
                    course_edition_id,
                    course_name,
                    approved_count,
                    total_count,
                    ROW_NUMBER() OVER (PARTITION BY month ORDER BY approved_count DESC) as rank
                FROM monthly_stats
            )
            SELECT 
                TO_CHAR(month, 'YYYY-MM') as month,
                course_name,
                approved_count,
                total_count
            FROM monthly_best_courses
            WHERE rank = 1
            ORDER BY month DESC
        """)

        rows = cur.fetchall()
        results = []
        for row in rows:
            results.append({
                'month': row[0],
                'course_name': row[1],
                'approved_count': row[2],
                'total_count': row[3]
            })

        return jsonify({
            'status': StatusCodes['success'],
            'errors': None,
            'results': results
        })

    except Exception as e:
        return jsonify({
            'status': StatusCodes['internal_error'],
            'errors': str(e),
            'results': None
        })
    finally:
        cur.close()
        conn.close()
'''

@app.route('/report', methods=['GET'])
@token_required
def get_monthly_report():
   

    conn = db_connection()
    cur = conn.cursor()

    if not check_staff_permission():
        return jsonify({'status': StatusCodes['unauthorized'], 'errors': 'Only staff can access degree details', 'results': None})

    try:
        cur.execute("""
            WITH monthly_stats AS (
                SELECT 
                    DATE_TRUNC('month', CURRENT_DATE) - (interval '1 month' * generate_series(0, 11)) AS month,
                    ce.edition_id,
                    c.name AS course_name,
                    COUNT(DISTINCT CASE WHEN sg.grade_grade >= 10 THEN sg.student_person_person_id END) AS approved_count,
                    COUNT(DISTINCT sg.student_person_person_id) AS total_count
                FROM subject_grade sg
                JOIN courseedition ce ON ce.course_course_id = sg.course_course_id
                JOIN course c ON c.course_id = sg.course_course_id
                WHERE sg.grade_grade IS NOT NULL
                GROUP BY ce.edition_id, c.name
            ),
            monthly_best_courses AS (
                SELECT 
                    m.month,
                    ms.edition_id,
                    ms.course_name,
                    ms.approved_count,
                    ms.total_count,
                    ROW_NUMBER() OVER (PARTITION BY m.month ORDER BY ms.approved_count DESC) as rank
                FROM (
                    SELECT DATE_TRUNC('month', CURRENT_DATE) - (interval '1 month' * generate_series(0, 11)) AS month
                ) m
                LEFT JOIN monthly_stats ms ON m.month = DATE_TRUNC('month', CURRENT_DATE)
            )
            SELECT 
                TO_CHAR(month, 'YYYY-MM') as month,
                edition_id,
                course_name,
                approved_count,
                total_count
            FROM monthly_best_courses
            WHERE rank = 1
            ORDER BY month DESC
        """)

        rows = cur.fetchall()
        results = []
        for row in rows:
            results.append({
                'month': row[0],
                'course_edition_id': row[1],
                'course_edition_name': row[2],
                'approved': row[3],
                'evaluated': row[4]
            })

        return jsonify({
            'status': StatusCodes['success'],
            'errors': None,
            'results': results
        })

    except Exception as e:
        return jsonify({'status': StatusCodes['internal_error'], 'errors': str(e), 'results': None})
    finally:
        cur.close()
        conn.close()

if __name__ == '__main__':
    # set up logging
    logging.basicConfig(filename='log_file.log')
    logger = logging.getLogger('logger')
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # create formatter
    formatter = logging.Formatter('%(asctime)s [%(levelname)s]:  %(message)s', '%H:%M:%S')
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    host = '127.0.0.1'
    port = 8080
    app.run(host=host, debug=True, threaded=True, port=port)
    logger.info(f'API stubs online: http://{host}:{port}')
