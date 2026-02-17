-- Admins table
CREATE TABLE admins (
    id SERIAL PRIMARY KEY,
    email VARCHAR NOT NULL UNIQUE,
    hashed_password VARCHAR NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

-- Token blacklist table
CREATE TABLE token_blacklist (
    id SERIAL PRIMARY KEY,
    token VARCHAR NOT NULL UNIQUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

-- Members table
CREATE TABLE members (
    id SERIAL PRIMARY KEY,
    membership_id VARCHAR NOT NULL UNIQUE,
    name VARCHAR NOT NULL,
    phone VARCHAR NOT NULL,
    email VARCHAR NOT NULL,
    aadhaar VARCHAR NOT NULL,
    blood_group VARCHAR,
    designation VARCHAR,
    father_husband_name VARCHAR,
    state VARCHAR NOT NULL,
    district VARCHAR NOT NULL,
    mandal VARCHAR NOT NULL,
    village VARCHAR,
    full_address TEXT,
    status VARCHAR DEFAULT 'pending',
    is_active BOOLEAN DEFAULT true,
    id_card_generated BOOLEAN DEFAULT false,
    photo_path VARCHAR,
    qr_code_path VARCHAR,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

CREATE INDEX idx_members_name ON members(name);
CREATE INDEX idx_members_phone ON members(phone);
CREATE INDEX idx_members_email ON members(email);
CREATE INDEX idx_members_aadhaar ON members(aadhaar);
CREATE INDEX idx_members_state ON members(state);
CREATE INDEX idx_members_district ON members(district);
CREATE INDEX idx_members_mandal ON members(mandal);
CREATE INDEX idx_members_status ON members(status);

-- Member applications table
CREATE TABLE member_applications (
    id SERIAL PRIMARY KEY,
    full_name VARCHAR,
    father_husband_name VARCHAR,
    gender VARCHAR,
    date_of_birth DATE,
    caste VARCHAR,
    aadhaar_number VARCHAR,
    phone_number VARCHAR,
    email_address VARCHAR,
    blood_group VARCHAR,
    designation VARCHAR,
    state VARCHAR,
    district VARCHAR,
    mandal VARCHAR,
    village VARCHAR,
    full_address TEXT,
    photo_path VARCHAR,
    status VARCHAR DEFAULT 'pending',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

CREATE INDEX idx_member_applications_full_name ON member_applications(full_name);
CREATE INDEX idx_member_applications_aadhaar ON member_applications(aadhaar_number);
CREATE INDEX idx_member_applications_phone ON member_applications(phone_number);
CREATE INDEX idx_member_applications_status ON member_applications(status);

-- Donations table
CREATE TABLE donations (
    id SERIAL PRIMARY KEY,
    donor_name VARCHAR,
    donor_email VARCHAR,
    phone_number VARCHAR,
    amount FLOAT,
    payment_method VARCHAR,
    transaction_id VARCHAR,
    notes TEXT,
    status VARCHAR DEFAULT 'pending',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

CREATE INDEX idx_donations_donor_name ON donations(donor_name);
CREATE INDEX idx_donations_donor_email ON donations(donor_email);
CREATE INDEX idx_donations_transaction_id ON donations(transaction_id);
CREATE INDEX idx_donations_status ON donations(status);

-- Complaints table
CREATE TABLE complaints (
    id SERIAL PRIMARY KEY,
    complainant_name VARCHAR NOT NULL,
    email VARCHAR,
    phone VARCHAR NOT NULL,
    address TEXT NOT NULL,
    type VARCHAR NOT NULL,
    subject VARCHAR NOT NULL,
    description TEXT NOT NULL,
    reference_id VARCHAR NOT NULL UNIQUE,
    supporting_document_path VARCHAR,
    status VARCHAR DEFAULT 'pending',
    admin_notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

CREATE INDEX idx_complaints_complainant_name ON complaints(complainant_name);
CREATE INDEX idx_complaints_email ON complaints(email);
CREATE INDEX idx_complaints_type ON complaints(type);
CREATE INDEX idx_complaints_subject ON complaints(subject);
CREATE INDEX idx_complaints_status ON complaints(status);

-- Gallery table
CREATE TABLE gallery (
    id SERIAL PRIMARY KEY,
    title VARCHAR NOT NULL,
    description TEXT,
    media_url VARCHAR NOT NULL,
    media_type VARCHAR NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

CREATE INDEX idx_gallery_title ON gallery(title);
CREATE INDEX idx_gallery_media_type ON gallery(media_type);
