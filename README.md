University Management System – RESTful Web App
– Python (Flask) & PostgreSQL
Co-developed a full-stack university management system with RESTful architecture. Implemented student/staff registration, course and activity enrollment, grade submission, and financial tracking. Designed and managed a relational database in PostgreSQL using SQL and PL/pgSQL, applying transactional logic and access control. Developed and tested secure endpoints with JWT authentication using Postman.

O projeto consiste no desenvolvimento de um sistema de gestão universitária
concebido para gerir os principais processos académicos e extracurriculares no
âmbito de uma universidade. O sistema é implementado como uma aplicação de
base de dados distribuída, seguindo uma arquitetura RESTful. Suporta
funcionalidades como o registo de estudantes e funcionários, a gestão de cursos e
turmas, a inscrição de estudantes, o envio de notas e o acompanhamento
financeiro.
O backend é desenvolvido em Python utilizando Flask, com uma base de dados
relacional PostgreSQL. Todas as interações com o sistema são realizadas através
de uma API REST, que é testada via Postman. O sistema garante que apenas os
utilizadores autorizados (estudantes, funcionários e instrutores) podem aceder e
realizar operações relevantes de acordo com as suas funções. As principais
restrições de dados e o tratamento de transações são implementados utilizando
SQL e PL/pgSQL para garantir a integridade, a consistência e a segurança.
O modelo da base de dados foi concebido utilizando a ONDA e inclui entidades
como Person, Student, Instructor, Course, CourseEdition, DegreeProgram,
Enrolment e FinancialTransaction.
