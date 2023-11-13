<<<<<<< HEAD
DO $$
BEGIN
 IF NOT EXISTS(SELECT FROM pg_database WHERE datname = 'courseservice') THEN
    CREATE DATABASE courseservice;
    GRANT ALL PRIVILEGES ON DATABASE courseservice TO postgres;
 END IF;
END $$;
=======
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
>>>>>>> a370d7b534c76dce922b3bdcde3d9755981b1b9d
