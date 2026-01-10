-- Create admin accounts manually in PostgreSQL
-- Password hashes generated with bcrypt

-- Example admin: admin@example.com / admin123
INSERT INTO admins (email, hashed_password) VALUES 
('admin@example.com', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW');

-- Add more admins as needed:
-- INSERT INTO admins (email, hashed_password) VALUES 
-- ('admin2@example.com', '$2b$12$hashed_password_here');