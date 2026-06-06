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