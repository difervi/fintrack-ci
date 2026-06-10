-- Schemas
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(120) NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT (NOW() AT TIME ZONE 'UTC')
);

CREATE TABLE IF NOT EXISTS categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(80) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS transactions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    category_id INTEGER NOT NULL REFERENCES categories(id),
    type VARCHAR(10) NOT NULL CHECK (type IN ('income', 'expense')),
    amount NUMERIC(12, 2) NOT NULL,
    description VARCHAR(255),
    date TIMESTAMP DEFAULT (NOW() AT TIME ZONE 'UTC')
);

-- Seed categories (idempotente)
INSERT INTO categories (name) VALUES
    ('Food'),
    ('Transportation'),
    ('Housing'),
    ('Health'),
    ('Entertainment'),
    ('Education'),
    ('Salary'),
    ('Other')
ON CONFLICT (name) DO NOTHING;

-- Seed users (idempotente)
INSERT INTO users (name, email) VALUES
    ('Alice', 'alice@example.com'),
    ('Bob', 'bob@example.com'),
    ('Carol', 'carol@example.com')
ON CONFLICT (email) DO NOTHING;

-- Seed example transactions idempotentes (buscan por email/nombre de categoría)
INSERT INTO transactions (user_id, category_id, type, amount, description, date)
SELECT u.id, c.id, 'expense', 12.50, 'Lunch at cafe', '2024-06-01 12:00:00+00'::timestamptz
FROM users u JOIN categories c ON c.name = 'Food'
WHERE u.email = 'alice@example.com'
  AND NOT EXISTS (
    SELECT 1 FROM transactions t WHERE t.user_id = u.id AND t.category_id = c.id AND t.amount = 12.50 AND t.description = 'Lunch at cafe'
  );

INSERT INTO transactions (user_id, category_id, type, amount, description, date)
SELECT u.id, c.id, 'income', 2500.00, 'Monthly salary', '2024-06-01 09:00:00+00'::timestamptz
FROM users u JOIN categories c ON c.name = 'Salary'
WHERE u.email = 'bob@example.com'
  AND NOT EXISTS (
    SELECT 1 FROM transactions t WHERE t.user_id = u.id AND t.category_id = c.id AND t.amount = 2500.00 AND t.description = 'Monthly salary'
  );

INSERT INTO transactions (user_id, category_id, type, amount, description, date)
SELECT u.id, c.id, 'expense', 75.30, 'Concert ticket', '2024-05-20 20:30:00+00'::timestamptz
FROM users u JOIN categories c ON c.name = 'Entertainment'
WHERE u.email = 'carol@example.com'
  AND NOT EXISTS (
    SELECT 1 FROM transactions t WHERE t.user_id = u.id AND t.category_id = c.id AND t.amount = 75.30 AND t.description = 'Concert ticket'
  );

-- Ajustar secuencias
SELECT setval(pg_get_serial_sequence('users','id'), COALESCE((SELECT MAX(id) FROM users), 1), true);
SELECT setval(pg_get_serial_sequence('categories','id'), COALESCE((SELECT MAX(id) FROM categories), 1), true);
SELECT setval(pg_get_serial_sequence('transactions','id'), COALESCE((SELECT MAX(id) FROM transactions), 1), true);