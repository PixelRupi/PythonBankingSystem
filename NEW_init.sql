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


-- haslo123
-- haslo1234
-- haselko#
-- haslo123
-- haslo1234
-- haselko#

INSERT INTO credentials (login, password, pin, uuid_client) VALUES
('jan_kowalski', 'a15f8ae07675bfb96e084bfb4f52fb2c22091061aae86e0eb76a55f4e52dd74e', '1234', '11111111-1111-1111-1111-111111111111'),
('anna_nowak', '04a875420e73e666e46ca88e300592fe63f3890b86e115bfd0ffcf02aa1d65c1', '5678', '22222222-2222-2222-2222-222222222222'),
('mercedes', 'aa30aa052a05879e00eb8347861c15e9929b7f3ec1897c29d785697d2fd3273c', '2137', '33333333-3333-3333-3333-333333333333'),
('zelislaw-zyzynski', 'a15f8ae07675bfb96e084bfb4f52fb2c22091061aae86e0eb76a55f4e52dd74e', '9712', '44444444-4444-4444-4444-444444444444'),
('sigmund_freud', '04a875420e73e666e46ca88e300592fe63f3890b86e115bfd0ffcf02aa1d65c1', '8921', '55555555-5555-5555-5555-555555555555');


INSERT INTO funds (uuid, funds, max_amount) VALUES
('11111111-1111-1111-1111-111111111111', 1200.00, 2000.00),
('22222222-2222-2222-2222-222222222222', 450.00, 1500.00),
('33333333-3333-3333-3333-333333333333', 3000.00, 5000.00),
('44444444-4444-4444-4444-444444444444', 12000.00, 350.00),
('55555555-5555-5555-5555-555555555555', 124718.00, 1350.00);

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
