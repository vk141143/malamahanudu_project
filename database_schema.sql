-- ============================================
-- SQL QUERIES TO CREATE ALL TABLES
-- Database: PostgreSQL / SQLite Compatible
-- ============================================

-- 1. ADMINS TABLE
CREATE TABLE admins (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_admins_email ON admins(email);

-- 2. TOKEN BLACKLIST TABLE
CREATE TABLE token_blacklist (
    id SERIAL PRIMARY KEY,
    token VARCHAR(500) UNIQUE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_token_blacklist_token ON token_blacklist(token);

-- 3. MEMBERS TABLE
CREATE TABLE members (
    id SERIAL PRIMARY KEY,
    membership_id VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    email VARCHAR(255) NOT NULL,
    aadhaar VARCHAR(12) NOT NULL,
    state VARCHAR(100) NOT NULL,
    district VARCHAR(100) NOT NULL,
    mandal VARCHAR(100) NOT NULL,
    status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'approved', 'rejected')),
    is_active BOOLEAN DEFAULT TRUE,
    id_card_generated BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
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
    id SERIAL PRIMARY KEY,
    full_name VARCHAR(255) NOT NULL,
    father_husband_name VARCHAR(255) NOT NULL,
    gender VARCHAR(10) NOT NULL CHECK (gender IN ('male', 'female', 'other')),
    date_of_birth DATE NOT NULL,
    caste VARCHAR(100) NOT NULL,
    aadhaar_number VARCHAR(12) NOT NULL,
    phone_number VARCHAR(20) NOT NULL,
    email_address VARCHAR(255),
    state VARCHAR(100) NOT NULL,
    district VARCHAR(100) NOT NULL,
    mandal VARCHAR(100) NOT NULL,
    village VARCHAR(100) NOT NULL,
    full_address TEXT NOT NULL,
    photo_path VARCHAR(500),
    status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'approved', 'rejected')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_member_applications_full_name ON member_applications(full_name);
CREATE INDEX idx_member_applications_aadhaar ON member_applications(aadhaar_number);
CREATE INDEX idx_member_applications_phone ON member_applications(phone_number);
CREATE INDEX idx_member_applications_status ON member_applications(status);

-- 5. DONATIONS TABLE
CREATE TABLE donations (
    id SERIAL PRIMARY KEY,
    donor_name VARCHAR(255) NOT NULL,
    donor_email VARCHAR(255) NOT NULL,
    phone_number VARCHAR(20) NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    payment_method VARCHAR(50) NOT NULL CHECK (payment_method IN ('bank_transfer', 'upi', 'cash', 'cheque', 'online_payment')),
    transaction_id VARCHAR(100) NOT NULL,
    notes TEXT,
    status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'verified', 'acknowledged', 'failed')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_donations_donor_name ON donations(donor_name);
CREATE INDEX idx_donations_donor_email ON donations(donor_email);
CREATE INDEX idx_donations_transaction_id ON donations(transaction_id);
CREATE INDEX idx_donations_status ON donations(status);

-- 6. COMPLAINTS TABLE
CREATE TABLE complaints (
    id SERIAL PRIMARY KEY,
    complainant_name VARCHAR(255) NOT NULL,
    email VARCHAR(255),
    phone VARCHAR(20) NOT NULL,
    address TEXT NOT NULL,
    type VARCHAR(50) NOT NULL CHECK (type IN ('Healthcare', 'Education', 'Employment', 'Infrastructure', 'Social Welfare', 'Other')),
    subject VARCHAR(500) NOT NULL,
    description TEXT NOT NULL,
    reference_id VARCHAR(50) UNIQUE NOT NULL,
    supporting_document_path VARCHAR(500),
    status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'in_progress', 'resolved', 'closed')),
    admin_notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_complaints_complainant_name ON complaints(complainant_name);
CREATE INDEX idx_complaints_email ON complaints(email);
CREATE INDEX idx_complaints_type ON complaints(type);
CREATE INDEX idx_complaints_subject ON complaints(subject);
CREATE INDEX idx_complaints_reference_id ON complaints(reference_id);
CREATE INDEX idx_complaints_status ON complaints(status);

-- 7. GALLERY TABLE
CREATE TABLE gallery (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    media_url VARCHAR(500) NOT NULL,
    media_type VARCHAR(10) NOT NULL CHECK (media_type IN ('image', 'video')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_gallery_title ON gallery(title);
CREATE INDEX idx_gallery_media_type ON gallery(media_type);

-- ============================================
-- INSERT DEFAULT ADMIN USER
-- Password: admin123 (bcrypt hashed)
-- ============================================
INSERT INTO admins (email, hashed_password) VALUES 
('admin@example.com', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW');

-- ============================================
-- NOTES:
-- 1. For SQLite, replace SERIAL with INTEGER PRIMARY KEY AUTOINCREMENT
-- 2. For SQLite, remove CHECK constraints or use triggers
-- 3. For SQLite, TIMESTAMP WITH TIME ZONE becomes DATETIME
-- 4. Default admin password is: admin123
-- ============================================