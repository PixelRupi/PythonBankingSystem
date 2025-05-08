-- Tworzenie tabel

DROP TABLE IF EXISTS history;
DROP TABLE IF EXISTS funds;
DROP TABLE IF EXISTS credentials;

CREATE TABLE credentials (
    id INT AUTO_INCREMENT PRIMARY KEY,
    login VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(100) NOT NULL,
    pin VARCHAR(10) NOT NULL,
    uuid_client CHAR(36) NOT NULL UNIQUE
);

CREATE TABLE funds (
    uuid CHAR(36) PRIMARY KEY,
    funds DECIMAL(12,2) NOT NULL DEFAULT 0.00,
    max_amount DECIMAL(12,2) NOT NULL DEFAULT 1000.00
);

CREATE TABLE history (
    transaction_id INT AUTO_INCREMENT PRIMARY KEY,
    uuid_from CHAR(36) NOT NULL,
    uuid_to CHAR(36) NOT NULL,
    operation VARCHAR(50) NOT NULL,
    amount DECIMAL(12,2) NOT NULL,
    FOREIGN KEY (uuid_from) REFERENCES funds(uuid),
    FOREIGN KEY (uuid_to) REFERENCES funds(uuid)
);

-- Przykładowi użytkownicy

INSERT INTO credentials (login, password, pin, uuid_client) VALUES
('jan_kowalski', 'haslo123', '1234', '11111111-1111-1111-1111-111111111111'),
('anna_nowak', 'bezpiecznehaslo', '5678', '22222222-2222-2222-2222-222222222222'),
('mercedes', 'haselko#', '2137', '33333333-3333-3333-3333-333333333333');

INSERT INTO funds (uuid, funds, max_amount) VALUES
('11111111-1111-1111-1111-111111111111', 1200.00, 2000.00),
('22222222-2222-2222-2222-222222222222', 450.00, 1500.00),
('33333333-3333-3333-3333-333333333333', 3000.00, 5000.00);

-- Przykładowe transakcje

INSERT INTO history (uuid_from, uuid_to, operation, amount) VALUES
('11111111-1111-1111-1111-111111111111', '22222222-2222-2222-2222-222222222222', 'transfer', 100.00),
('33333333-3333-3333-3333-333333333333', '11111111-1111-1111-1111-111111111111', 'transfer', 500.00);



-- logowanie do bazy i import init.sq;: 
-- docker cp init.sql <nazwa>:/init.sql
-- docker exec -it <nazwa> mariadb -u root -p
-- use PythonBank;
-- source init.sql

-- nazwa docker -ps w kategorii name