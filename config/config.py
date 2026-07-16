from sqlalchemy.engine import URL

DATABASE_URL = URL.create(
    drivername="postgresql+psycopg2",
    username="postgres",
    password="srikar@123",
    host="postgres",      # Docker service name
    port=5432,
    database="olist_dw"   # Your project database
)