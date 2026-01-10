-- ============================================
-- SQL QUERIES FOR SQLite DATABASE
-- ============================================

-- 1. ADMINS TABLE
CREATE TABLE admins (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    hashed_password TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_admins_email ON admins(email);

-- 2. TOKEN BLACKLIST TABLE
CREATE TABLE token_blacklist (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    token TEXT UNIQUE NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_token_blacklist_token ON token_blacklist(token);

-- 3. MEMBERS TABLE
CREATE TABLE members (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    membership_id TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    phone TEXT NOT NULL,
    email TEXT NOT NULL,
    aadhaar TEXT NOT NULL,
    state TEXT NOT NULL,
    district TEXT NOT NULL,
    mandal TEXT NOT NULL,
    status TEXT DEFAULT 'pending',
    is_active INTEGER DEFAULT 1,
    id_card_generated INTEGER DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_members_membership_id ON members(membership_id);
CREATE INDEX idx_members_name ON members(name);
CREATE INDEX idx_members_phone ON members(phone);
CREATE INDEX idx_members_email ON members(email);
CREATE INDEX idx_members_aadhaar ON members(aadhaar);
CREATE INDEX idx_members_state ON members(state);
CREATE INDEX idx_members_district ON members(district);
CREATE INDEX idx_members_mandal ON members(mandal);
CREATE INDEX idx_members_status ON members(status);

-- 4. MEMBER APPLICATIONS TABLE
CREATE TABLE member_applications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    father_husband_name TEXT NOT NULL,
    gender TEXT NOT NULL,
    date_of_birth DATE NOT NULL,
    caste TEXT NOT NULL,
    aadhaar_number TEXT NOT NULL,
    phone_number TEXT NOT NULL,
    email_address TEXT,
    state TEXT NOT NULL,
    district TEXT NOT NULL,
    mandal TEXT NOT NULL,
    village TEXT NOT NULL,
    full_address TEXT NOT NULL,
    photo_path TEXT,
    status TEXT DEFAULT 'pending',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_member_applications_full_name ON member_applications(full_name);
CREATE INDEX idx_member_applications_aadhaar ON member_applications(aadhaar_number);
CREATE INDEX idx_member_applications_phone ON member_applications(phone_number);
CREATE INDEX idx_member_applications_status ON member_applications(status);

-- 5. DONATIONS TABLE
CREATE TABLE donations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    donor_name TEXT NOT NULL,
    donor_email TEXT NOT NULL,
    phone_number TEXT NOT NULL,
    amount REAL NOT NULL,
    payment_method TEXT NOT NULL,
    transaction_id TEXT NOT NULL,
    notes TEXT,
    status TEXT DEFAULT 'pending',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_donations_donor_name ON donations(donor_name);
CREATE INDEX idx_donations_donor_email ON donations(donor_email);
CREATE INDEX idx_donations_transaction_id ON donations(transaction_id);
CREATE INDEX idx_donations_status ON donations(status);

-- 6. COMPLAINTS TABLE
CREATE TABLE complaints (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    complainant_name TEXT NOT NULL,
    email TEXT,
    phone TEXT NOT NULL,
    address TEXT NOT NULL,
    type TEXT NOT NULL,
    subject TEXT NOT NULL,
    description TEXT NOT NULL,
    reference_id TEXT UNIQUE NOT NULL,
    supporting_document_path TEXT,
    status TEXT DEFAULT 'pending',
    admin_notes TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_complaints_complainant_name ON complaints(complainant_name);
CREATE INDEX idx_complaints_email ON complaints(email);
CREATE INDEX idx_complaints_type ON complaints(type);
CREATE INDEX idx_complaints_subject ON complaints(subject);
CREATE INDEX idx_complaints_reference_id ON complaints(reference_id);
CREATE INDEX idx_complaints_status ON complaints(status);

-- 7. GALLERY TABLE
CREATE TABLE gallery (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    media_url TEXT NOT NULL,
    media_type TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_gallery_title ON gallery(title);
CREATE INDEX idx_gallery_media_type ON gallery(media_type);

-- ============================================
-- INSERT DEFAULT ADMIN USER
-- Email: admin@example.com
-- Password: admin123 (bcrypt hashed)
-- ============================================
INSERT INTO admins (email, hashed_password) VALUES 
('admin@example.com', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW');