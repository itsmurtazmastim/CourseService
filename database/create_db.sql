--SELECT 'CREATE DATABASE courseservice'
--WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'courseservice')\gexec;
--GRANT ALL PRIVILEGES ON DATABASE courseservice TO postgres;
DO $$
BEGIN
  IF NOT EXISTS (SELECT FROM pg_database WHERE datname = 'courseservice') THEN
    CREATE DATABASE courseservice;
    GRANT ALL PRIVILEGES ON DATABASE courseservice TO postgres;
  END IF;
END $$;