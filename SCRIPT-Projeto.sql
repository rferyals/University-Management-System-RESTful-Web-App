/* - INÍCIO - VERIFICAR TABELAS */
SELECT * FROM activity
SELECT * FROM admstaff
SELECT * FROM course
SELECT * FROM course_degreeprogram
SELECT * FROM courseedition
SELECT * FROM degreeprogram
SELECT * FROM employee
SELECT * FROM instructor
SELECT * FROM person
SELECT * FROM student
SELECT * FROM student_courseedition
SELECT * FROM student_activity
SELECT * FROM subject_grade
/* - FIM - VERIFICAR TABELAS */


/* - INÍCIO - COMANDO PARA DAR PERMISSÕES */
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE
	person,
	person_person_id,
	employee,
	admstaff,
	student,
	instructor,
    degreeprogram,
    course,
    courseedition,
    course_degreeprogram,
    enrolment_activity_financialtr,
    enrolment_activity_financialtr_student,
    subject_grade,
    classroom_class,
    instructor_course,
    course_course,
	activity,
	student_activity,
	student_courseedition
	subject_grade_subject_id_seq
	subject_grade_grade_grade_id_seq
TO userprojeto;
/* - FIM - COMANDO PARA DAR PERMISSÕES */


/* - INÍCIO - ADICIONAR CADEIRAS AOS CURSOS */

CREATE TABLE student_courseedition (
    student_id INTEGER NOT NULL,
    course_edition_id INTEGER NOT NULL,
    PRIMARY KEY (student_id, course_edition_id),
    FOREIGN KEY (student_id) REFERENCES student(person_person_id),
    FOREIGN KEY (course_edition_id) REFERENCES courseedition(edition_id)
);
-- CADEIRAS ENGENHARIA INFORMATICA
INSERT INTO course (course_id, name, description, credits) VALUES
(101, 'C1EI', 'Cadeira 1 - EI', 6),
(102, 'C2EI', 'Cadeira 2 - EI', 6),
(103, 'C3EI', 'Cadeira 3 - EI', 6),
(104, 'C4EI', 'Cadeira 4 - EI', 6),
(105, 'C5EI', 'Cadeira 5 - EI', 6),
(106, 'C6EI', 'Cadeira 6 - EI', 6),
(107, 'C7EI', 'Cadeira 7 - EI', 6),
(108, 'C8EI', 'Cadeira 8 - EI', 6),
(109, 'C9EI', 'Cadeira 9 - EI', 6),
(110, 'C10EI', 'Cadeira 10 - EI', 6),
(111, 'C11EI', 'Cadeira 11 - EI', 6),
(112, 'C12EI', 'Cadeira 12 - EI', 6);
-- CADEIRAS MEDICINA
INSERT INTO course (course_id, name, description, credits) VALUES
(201, 'C1M', 'Cadeira 1 - M', 6),
(202, 'C2M', 'Cadeira 2 - M', 6),
(203, 'C3M', 'Cadeira 3 - M', 6),
(204, 'C4M', 'Cadeira 4 - M', 6),
(205, 'C5M', 'Cadeira 5 - M', 6),
(206, 'C6M', 'Cadeira 6 - M', 6),
(207, 'C7M', 'Cadeira 7 - M', 6),
(208, 'C8M', 'Cadeira 8 - M', 6),
(209, 'C9M', 'Cadeira 9 - M', 6),
(210, 'C10M', 'Cadeira 10 - M', 6),
(211, 'C11M', 'Cadeira 11 - M', 6),
(212, 'C12M', 'Cadeira 12 - M', 6),
(213, 'C13M', 'Cadeira 13 - M', 6),
(214, 'C14M', 'Cadeira 14 - M', 6),
(215, 'C15M', 'Cadeira 15 - M', 6),
(216, 'C16M', 'Cadeira 16 - M', 6),
(217, 'C17M', 'Cadeira 17 - M', 6),
(218, 'C18M', 'Cadeira 18 - M', 6),
(219, 'C19M', 'Cadeira 19 - M', 6),
(220, 'C20M', 'Cadeira 20 - M', 6);
-- CADEIRAS DIREITO
INSERT INTO course (course_id, name, description, credits) VALUES
(301, 'C1D', 'Cadeira 1 - D', 6),
(302, 'C2D', 'Cadeira 2 - D', 6),
(303, 'C3D', 'Cadeira 3 - D', 6),
(304, 'C4D', 'Cadeira 4 - D', 6),
(305, 'C5D', 'Cadeira 5 - D', 6),
(306, 'C6D', 'Cadeira 6 - D', 6),
(307, 'C7D', 'Cadeira 7 - D', 6),
(308, 'C8D', 'Cadeira 8 - D', 6),
(309, 'C9D', 'Cadeira 9 - D', 6),
(310, 'C10D', 'Cadeira 10 - D', 6),
(311, 'C11D', 'Cadeira 11 - D', 6),
(312, 'C12D', 'Cadeira 12 - D', 6);
-- CADEIRAS CRIMINOLOGIA
INSERT INTO course (course_id, name, description, credits) VALUES
(401, 'C1C', 'Cadeira 1 - C', 6),
(402, 'C2C', 'Cadeira 2 - C', 6),
(403, 'C3C', 'Cadeira 3 - C', 6),
(404, 'C4C', 'Cadeira 4 - C', 6),
(405, 'C5C', 'Cadeira 5 - C', 6),
(406, 'C6C', 'Cadeira 6 - C', 6),
(407, 'C7C', 'Cadeira 7 - C', 6),
(408, 'C8C', 'Cadeira 8 - C', 6),
(409, 'C9C', 'Cadeira 9 - C', 6),
(410, 'C10C', 'Cadeira 10 - C', 6),
(411, 'C11C', 'Cadeira 11 - C', 6),
(412, 'C12C', 'Cadeira 12 - C', 6);
-- CADEIRAS ECONOMIA
INSERT INTO course (course_id, name, description, credits) VALUES
(501, 'C1E', 'Cadeira 1 - E', 6),
(502, 'C2E', 'Cadeira 2 - E', 6),
(503, 'C3E', 'Cadeira 3 - E', 6),
(504, 'C4E', 'Cadeira 4 - E', 6),
(505, 'C5E', 'Cadeira 5 - E', 6),
(506, 'C6E', 'Cadeira 6 - E', 6),
(507, 'C7E', 'Cadeira 7 - E', 6),
(508, 'C8E', 'Cadeira 8 - E', 6),
(509, 'C9E', 'Cadeira 9 - E', 6),
(510, 'C10E', 'Cadeira 10 - E', 6),
(511, 'C11E', 'Cadeira 11 - E', 6),
(512, 'C12E', 'Cadeira 12 - E', 6);

-- Engenharia Informática
INSERT INTO course_degreeprogram (course_course_id, degreeprogram_type) VALUES
(101, 'Engenharia Informática'), (102, 'Engenharia Informática'), (103, 'Engenharia Informática'), (104, 'Engenharia Informática'),
(105, 'Engenharia Informática'), (106, 'Engenharia Informática'), (107, 'Engenharia Informática'), (108, 'Engenharia Informática'),
(109, 'Engenharia Informática'), (110, 'Engenharia Informática'), (111, 'Engenharia Informática'), (112, 'Engenharia Informática');
-- Medicina
INSERT INTO course_degreeprogram (course_course_id, degreeprogram_type) VALUES
(201, 'Medicina'), (202, 'Medicina'), (203, 'Medicina'), (204, 'Medicina'), (205, 'Medicina'), (206, 'Medicina'),
(207, 'Medicina'), (208, 'Medicina'), (209, 'Medicina'), (210, 'Medicina'), (211, 'Medicina'), (212, 'Medicina'),
(213, 'Medicina'), (214, 'Medicina'), (215, 'Medicina'), (216, 'Medicina'), (217, 'Medicina'), (218, 'Medicina'),
(219, 'Medicina'), (220, 'Medicina');
-- Direito
INSERT INTO course_degreeprogram (course_course_id, degreeprogram_type) VALUES
(301, 'Direito'), (302, 'Direito'), (303, 'Direito'), (304, 'Direito'),
(305, 'Direito'), (306, 'Direito'), (307, 'Direito'), (308, 'Direito'),
(309, 'Direito'), (310, 'Direito'), (311, 'Direito'), (312, 'Direito');
-- Criminologia
INSERT INTO course_degreeprogram (course_course_id, degreeprogram_type) VALUES
(401, 'Criminologia'), (402, 'Criminologia'), (403, 'Criminologia'), (404, 'Criminologia'),
(405, 'Criminologia'), (406, 'Criminologia'), (407, 'Criminologia'), (408, 'Criminologia'),
(409, 'Criminologia'), (410, 'Criminologia'), (411, 'Criminologia'), (412, 'Criminologia');
-- Economia
INSERT INTO course_degreeprogram (course_course_id, degreeprogram_type) VALUES
(501, 'Economia'), (502, 'Economia'), (503, 'Economia'), (504, 'Economia'),
(505, 'Economia'), (506, 'Economia'), (507, 'Economia'), (508, 'Economia'),
(509, 'Economia'), (510, 'Economia'), (511, 'Economia'), (512, 'Economia');

-- Inserir edições para algumas cadeiras do curso (course_id de 101 a 112)
INSERT INTO courseedition (edition_id, edition_year, semester, capacity, course_course_id, instructor_employee_person_person_id) VALUES
-- ID's cadeiras Eng. Informática
(1, 2025, '1', 200, 101, 13),
(2, 2025, '1', 200, 102, 15),
(3, 2025, '1', 200, 103, 19),
(4, 2025, '1', 200, 104, 29),
(5, 2025, '1', 200, 105, 30),
(6, 2025, '1', 200, 106, 13),
(7, 2025, '2', 200, 107, 15),
(8, 2025, '2', 200, 108, 19),
(9, 2025, '2', 200, 109, 29),
(10, 2025, '2', 200, 110, 30),
(11, 2025, '2', 200, 111, 13),
(12, 2025, '2', 200, 112, 15),
-- ID's cadeiras Medicina
(13, 2025, '1', 200, 201, 13),
(14, 2025, '1', 200, 202, 15),
(15, 2025, '1', 200, 203, 19),
(16, 2025, '1', 200, 204, 29),
(17, 2025, '1', 200, 205, 30),
(18, 2025, '1', 200, 206, 13),
(19, 2025, '1', 200, 207, 15),
(20, 2025, '1', 200, 208, 19),
(21, 2025, '1', 200, 209, 29),
(22, 2025, '1', 200, 210, 30),
(23, 2025, '2', 200, 211, 13),
(24, 2025, '2', 200, 212, 15),
(25, 2025, '2', 200, 213, 13),
(26, 2025, '2', 200, 214, 15),
(27, 2025, '2', 200, 215, 19),
(28, 2025, '2', 200, 216, 29),
(29, 2025, '2', 200, 217, 30),
(30, 2025, '2', 200, 218, 13),
(31, 2025, '2', 200, 219, 15),
(32, 2025, '2', 200, 220, 19),
-- ID's cadeiras Direito
(33, 2025, '1', 200, 301, 29),
(34, 2025, '1', 200, 302, 30),
(35, 2025, '1', 200, 303, 13),
(36, 2025, '1', 200, 304, 15),
(37, 2025, '1', 200, 305, 29),
(38, 2025, '1', 200, 306, 30),
(39, 2025, '2', 200, 307, 13),
(40, 2025, '2', 200, 308, 15),
(41, 2025, '2', 200, 309, 29),
(42, 2025, '2', 200, 310, 30),
(43, 2025, '2', 200, 311, 13),
(44, 2025, '2', 200, 312, 15),
-- ID's cadeiras Criminologia
(45, 2025, '1', 200, 401, 29),
(46, 2025, '1', 200, 402, 30),
(47, 2025, '1', 200, 403, 13),
(48, 2025, '1', 200, 404, 15),
(49, 2025, '1', 200, 405, 29),
(50, 2025, '1', 200, 406, 30),
(51, 2025, '2', 200, 407, 13),
(52, 2025, '2', 200, 408, 15),
(53, 2025, '2', 200, 409, 29),
(54, 2025, '2', 200, 410, 30),
(55, 2025, '2', 200, 411, 13),
(56, 2025, '2', 200, 412, 15),
-- ID's cadeiras Economia
(57, 2025, '1', 200, 501, 29),
(58, 2025, '1', 200, 502, 30),
(59, 2025, '1', 200, 503, 13),
(60, 2025, '1', 200, 504, 15),
(61, 2025, '1', 200, 505, 29),
(62, 2025, '1', 200, 506, 30),
(63, 2025, '2', 200, 507, 13),
(64, 2025, '2', 200, 508, 15),
(65, 2025, '2', 200, 509, 29),
(66, 2025, '2', 200, 510, 30),
(67, 2025, '2', 200, 511, 13),
(68, 2025, '2', 200, 512, 15);

/* - FIM - ADICIONAR CADEIRAS AOS CURSOS */


/* - INÍCIO - ADICIONAR CURSOS NA TABELA degreeprogram */

INSERT INTO degreeprogram (type, duration) VALUES 
('Engenharia Informática', 3),
('Direito', 3),
('Criminologia', 3),
('Economia', 3),
('Medicina', 5);

/* - FIM - ADICIONAR CURSOS NA TABELA degreeprogram */


/* - INÍCIO - ADICIONAR ATIVIDADES NA TABELA */

CREATE TABLE activity (
    activity_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    fee FLOAT NOT NULL
);

CREATE TABLE student_activity (
    student_id INTEGER NOT NULL,
    activity_id INTEGER NOT NULL,
    PRIMARY KEY (student_id, activity_id),
    FOREIGN KEY (student_id) REFERENCES student(person_person_id),
    FOREIGN KEY (activity_id) REFERENCES activity(activity_id)
);

INSERT INTO activity (name, fee) VALUES
('Futebol', 10),
('Teatro', 5),
('Xadrez', 5),
('Voluntariado', 0),
('Ginástica', 10);

/* - FIM - ADICIONAR ATIVIDADES NA TABELA */


/* - INÍCIO - SCRIPT PARA CRIAR TABELAS */

CREATE TABLE student (
	date_of_birth	 DATE NOT NULL,
	enrolment_date	 DATE NOT NULL,
	area		 TEXT NOT NULL,
	person_person_id INTEGER,
	PRIMARY KEY(person_person_id)
);

CREATE TABLE course (
	course_id	 INTEGER,
	name	 VARCHAR(100) NOT NULL,
	description TEXT,
	credits	 INTEGER NOT NULL,
	PRIMARY KEY(course_id)
);

CREATE TABLE courseedition (
	edition_id				 SERIAL NOT NULL,
	edition_year			 INTEGER NOT NULL,
	semester				 VARCHAR(5) NOT NULL,
	capacity				 INTEGER NOT NULL,
	course_course_id			 INTEGER,
	instructor_employee_person_person_id INTEGER NOT NULL,
	PRIMARY KEY(course_course_id)
);

CREATE TABLE instructor (
	department		 VARCHAR(100) NOT NULL,
	employee_person_person_id INTEGER,
	PRIMARY KEY(employee_person_person_id)
);

CREATE TABLE instructor_course (
	instructor_employee_person_person_id INTEGER,
	course_course_id			 INTEGER,
	PRIMARY KEY(instructor_employee_person_person_id,course_course_id)
);

CREATE TABLE person (
	person_id	 SERIAL,
	email	 VARCHAR(100) NOT NULL,
	name	 VARCHAR(100) NOT NULL,
	phone_number VARCHAR(512) NOT NULL,
	address	 TEXT NOT NULL,
	password	 TEXT NOT NULL,
	role	 TEXT NOT NULL,
	PRIMARY KEY(person_id)
);

CREATE TABLE admstaff (
	employee_person_person_id INTEGER,
	PRIMARY KEY(employee_person_person_id)
);

CREATE TABLE employee (
	hire_date	 DATE,
	person_person_id INTEGER,
	PRIMARY KEY(person_person_id)
);

CREATE TABLE degreeprogram (
	type	 VARCHAR(512) DEFAULT '50',
	duration INTEGER NOT NULL,
	PRIMARY KEY(type)
);

CREATE TABLE subject_grade (
	subject_id		 SERIAL,
	grade_grade		 FLOAT(5) NOT NULL,
	grade_evaluation_period	 VARCHAR(20) NOT NULL,
	student_person_person_id INTEGER NOT NULL,
	course_course_id	 INTEGER,
	PRIMARY KEY(subject_id,course_course_id)
);

CREATE TABLE course_degreeprogram (
	course_course_id	 INTEGER,
	degreeprogram_type VARCHAR(512) DEFAULT '50',
	PRIMARY KEY(course_course_id,degreeprogram_type)
);

ALTER TABLE student ADD CONSTRAINT student_fk1 FOREIGN KEY (person_person_id) REFERENCES person(person_id);
ALTER TABLE enrolment_activity_financialtr ADD UNIQUE (enrolment_id, activity_financialtr_activity_id, activity_financialtr_financialtr_tr_id);
ALTER TABLE enrolment_activity_financialtr ADD CONSTRAINT enrolment_activity_financialtr_fk1 FOREIGN KEY (course_course_id) REFERENCES course(course_id);
ALTER TABLE enrolment_activity_financialtr ADD CONSTRAINT enrolment_activity_financialtr_fk2 FOREIGN KEY (student_person_person_id) REFERENCES student(person_person_id);
ALTER TABLE enrolment_activity_financialtr ADD CONSTRAINT enrolment_activity_financialtr_fk3 FOREIGN KEY (student_person_person_id1) REFERENCES student(person_person_id);
ALTER TABLE enrolment_activity_financialtr ADD CONSTRAINT enrolment_activity_financialtr_fk4 FOREIGN KEY (admstaff_employee_person_person_id) REFERENCES admstaff(employee_person_person_id);
ALTER TABLE course ADD UNIQUE (name);
ALTER TABLE courseedition ADD UNIQUE (edition_id);
ALTER TABLE courseedition ADD CONSTRAINT courseedition_fk1 FOREIGN KEY (course_course_id) REFERENCES course(course_id);
ALTER TABLE courseedition ADD CONSTRAINT courseedition_fk2 FOREIGN KEY (instructor_employee_person_person_id) REFERENCES instructor(employee_person_person_id);
ALTER TABLE instructor ADD CONSTRAINT instructor_fk1 FOREIGN KEY (employee_person_person_id) REFERENCES employee(person_person_id);
ALTER TABLE person ADD UNIQUE (email, phone_number);
ALTER TABLE admstaff ADD CONSTRAINT admstaff_fk1 FOREIGN KEY (employee_person_person_id) REFERENCES employee(person_person_id);
ALTER TABLE classroom_class ADD UNIQUE (class_class_id);
ALTER TABLE classroom_class ADD CONSTRAINT classroom_class_fk1 FOREIGN KEY (courseedition_course_course_id) REFERENCES courseedition(course_course_id);
ALTER TABLE employee ADD CONSTRAINT employee_fk1 FOREIGN KEY (person_person_id) REFERENCES person(person_id);
ALTER TABLE subject_grade ADD UNIQUE (grade_grade_id);
ALTER TABLE subject_grade ADD CONSTRAINT subject_grade_fk1 FOREIGN KEY (student_person_person_id) REFERENCES student(person_person_id);
ALTER TABLE subject_grade ADD CONSTRAINT subject_grade_fk2 FOREIGN KEY (course_course_id) REFERENCES course(course_id);
ALTER TABLE enrolment_activity_financialtr_student ADD CONSTRAINT enrolment_activity_financialtr_student_fk1 FOREIGN KEY (enrolment_activity_financialtr_course_course_id) REFERENCES enrolment_activity_financialtr(course_course_id);
ALTER TABLE enrolment_activity_financialtr_student ADD CONSTRAINT enrolment_activity_financialtr_student_fk2 FOREIGN KEY (student_person_person_id) REFERENCES student(person_person_id);
ALTER TABLE course_course ADD CONSTRAINT course_course_fk1 FOREIGN KEY (course_course_id) REFERENCES course(course_id);
ALTER TABLE course_course ADD CONSTRAINT course_course_fk2 FOREIGN KEY (course_course_id1) REFERENCES course(course_id);
ALTER TABLE course_degreeprogram ADD CONSTRAINT course_degreeprogram_fk1 FOREIGN KEY (course_course_id) REFERENCES course(course_id);
ALTER TABLE course_degreeprogram ADD CONSTRAINT course_degreeprogram_fk2 FOREIGN KEY (degreeprogram_type) REFERENCES degreeprogram(type);
ALTER TABLE instructor_course ADD CONSTRAINT instructor_course_fk1 FOREIGN KEY (instructor_employee_person_person_id) REFERENCES instructor(employee_person_person_id);
ALTER TABLE instructor_course ADD CONSTRAINT instructor_course_fk2 FOREIGN KEY (course_course_id) REFERENCES course(course_id);

/* - FIM - SCRIPT PARA CRIAR TABELAS */


/* -INÍCIO - COMANDO PARA CRIAR O ADMIN */

CREATE EXTENSION IF NOT EXISTS pgcrypto;
-- Atualizar a senha do admin com hash 
UPDATE person
SET password = 'scrypt:32768:8:1$NjdcOQrwNWRxzpGN$c896fa894f5b76b85636e502d2990213a2d414ee8a86940d1fe58ba3743353b06cabbde8289540f5c9f45eb3d4bb761460d99025c2b56808422b86c9a294f876'
WHERE email = 'admin@universidade.pt';
INSERT INTO person (email, name, phone_number, address, password, role)
VALUES (
    'admin@universidade.pt',
    'Admin',
    '111111111',
    'Admin',
    'admin123',
    'staff'
);
INSERT INTO employee (person_person_id, hire_date)
VALUES (1, CURRENT_DATE);
INSERT INTO admstaff (employee_person_person_id)
VALUES (1);

/* - FIM - COMANDO PARA CRIAR O ADMIN */