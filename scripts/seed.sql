
    CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
    CREATE TABLE IF NOT EXISTS theme(
        id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
        theme_name VARCHAR(100)    NOT NULL
    );
    INSERT INTO theme (theme_name)
    VALUES ('code quality'), ('meeting user needs'), ('the ci cd pipeline'), ('refreshing and patching'), ('operability'), ('data persistence'), ('automation'), ('data security');

    CREATE OR REPLACE FUNCTION trigger_set_timestamp()
    RETURNS TRIGGER AS $$
    BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;

    CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
    CREATE TABLE IF NOT EXISTS ksb(
        id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
        ksb_type   VARCHAR(9)    NOT NULL,
        ksb_code   INT    NOT NULL,
        description TEXT NOT NULL,
        created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
        updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
        is_complete BOOLEAN NOT NULL
    );
    CREATE TRIGGER set_timestamp
    BEFORE UPDATE ON ksb
    FOR EACH ROW
    EXECUTE PROCEDURE trigger_set_timestamp();

    INSERT INTO ksb (ksb_type, ksb_code, description, is_complete)
    VALUES  ('Knowledge', 5, 'Modern security tools and techniques, including threat modelling and vulnerability scanning.', false),  
            ('Knowledge', 7, 'General purpose programming and infrastructure-as-code.',false),  
            ('Skill', 9, 'Using cloud security tools and automating security in pipelines.', false),  
            ('Behaviour', 3, 'Takes ownership of deployed code and learns from failures.', false);  

    CREATE TABLE IF NOT EXISTS themeksb(
        theme_id UUID REFERENCES theme(id)  ON DELETE CASCADE,
        ksb_id UUID REFERENCES ksb(id)  ON DELETE CASCADE,
        PRIMARY KEY (theme_id, ksb_id)
      
    );
    INSERT INTO themeksb (theme_id, ksb_id)
    SELECT 
        (SELECT id FROM theme WHERE theme_name = 'code quality'),
        (SELECT id FROM ksb WHERE description = 'Modern security tools and techniques, including threat modelling and vulnerability scanning.');

    INSERT INTO themeksb (theme_id, ksb_id)
    SELECT 
        (SELECT id FROM theme WHERE theme_name = 'code quality'),
        (SELECT id FROM ksb WHERE description = 'General purpose programming and infrastructure-as-code.');

    INSERT INTO themeksb (theme_id, ksb_id)
    SELECT 
        (SELECT id FROM theme WHERE theme_name = 'the ci cd pipeline'),
        (SELECT id FROM ksb WHERE description = 'Using cloud security tools and automating security in pipelines.');

    INSERT INTO themeksb (theme_id, ksb_id)
    SELECT 
        (SELECT id FROM theme WHERE theme_name = 'data security'),
        (SELECT id FROM ksb WHERE description = 'Modern security tools and techniques, including threat modelling and vulnerability scanning.');

