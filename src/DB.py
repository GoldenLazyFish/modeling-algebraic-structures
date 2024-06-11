import psycopg2
import ast
from credentials import host, user, password, db_name


class DB:
    def __init__(self):
        pass

    def save(self, matrix_values, size):
        # Connect to the database
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        connection.autocommit = True

        # Create a cursor
        with connection.cursor() as cursor:
            # Create a table to store the matrix data
            cursor.execute(
                "CREATE TABLE IF NOT EXISTS matrix_data (id SERIAL PRIMARY KEY, matrix_size INTEGER, matrix_data TEXT)"
            )

            # Convert the matrix to a string and store it in the database
            matrix_str = str(matrix_values)
            cursor.execute(
                "INSERT INTO matrix_data (matrix_size, matrix_data) VALUES (%s, %s)",
                (size, matrix_str)
            )

        # Close the connection
        connection.close()
        print("[INFO] Matrix data saved to the database")

    def load_by_id(self, matrix_id):
        # Connect to the database
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        connection.autocommit = True

        # Create a cursor
        with connection.cursor() as cursor:
            # Fetch the matrix data for the given ID
            cursor.execute(
                "SELECT matrix_size, matrix_data FROM matrix_data WHERE id = %s",
                (matrix_id,)
            )
            result = cursor.fetchone()

        # Close the connection
        connection.close()

        # Extract the matrix size and matrix data from the result
        matrix_size = result[0]
        matrix_data = ast.literal_eval(result[1])
        return matrix_data, matrix_size
    
    def update_by_id(self, matrix_id, matrix_str, matrix_size):
        # Connect to the database
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        connection.autocommit = True

        # Create a cursor
        with connection.cursor() as cursor:
            # Update the matrix data in the database
            cursor.execute(
                "UPDATE matrix_data SET matrix_size = %s, matrix_data = %s WHERE id = %s",
                (matrix_size, matrix_str, matrix_id)
            )

        # Close the connection
        connection.close()

        print(f"[INFO] Matrix data with ID {matrix_id} updated in the database")
