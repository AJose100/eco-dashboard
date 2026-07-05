INSERT INTO users (email, name) VALUES ('teste@eco.com', 'Usuário Teste');
INSERT INTO properties (user_id, name, zip_code) VALUES (1, 'Minha Casa', '00000-000');
INSERT INTO consumption_readings (property_id, source_id, reading_date, value) 
VALUES (1, 1, '2023-09-01', 150.50), (1, 1, '2023-10-01', 130.00);