**Project Overview**

This project demonstrates building an image search engine using FastAPI and image embeddings and pgvector. Users can
upload a dataset of cropped face images and then search for similar images by uploading a query image.

**Dependencies**

* Python 3.10
* FastAPI
* uvicorn
* psycopg2
* Pillow
* opencv-python
* imgbeddings
* pytorch

**Database Setup**

1. **Create Database:**

```   
CREATE DATABASE <database_name>;
```

2. **Connect to Database:**


3. **Ensure you have setup pgevctor by following the steps listed in this README file**

```
https://github.com/pgvector/pgvector/blob/master/README.md
```

4. **Enable the extension (do this once in each database where you want to use it)**

```
CREATE EXTENSION vector;
```

5. **Create Table:**

```
CREATE TABLE image_search (
        id BIGSERIAL PRIMARY KEY,
        image_name TEXT UNIQUE NOT NULL,
        embeddings vector NOT NULL
    );

```

**Running the Project**

1. **Install dependencies:**

```
pip install -r requirements.txt
```

2. **Create a .env file and add your Database credentials to it:**

```
database_hostname = <database_hostname>
database_name = <database_name>
database_username = <database_username> 
database_password = <database_password> 
```

3. **Start the application:**

```
uvicorn main:app --reload
```

**Usage**

1. **Access the application:** Open your web browser and navigate to http://localhost:8000/
2. **Upload Dataset:**
    * Click "Choose File" under "Upload Dataset".
    * Select multiple image files to upload.
    * Click "Upload" to process and store the images and their embeddings in the database.
3. **Search Images:**
    * Click "Choose File" under "Search Images".
    * Select a query image file.
    * Click "Search" to find similar images based on embedding similarity.
    * The results will display up to 5 closest matches from the dataset.

**Project Structure**

* **database.py:** Contains functions for connecting to the PostgreSQL database.
* **main.py:** Defines the main FastAPI application and includes the router.
* **routers.py:** Defines API routes for uploading datasets, searching images, and handling the main page.
* **templates/**: Stores HTML templates for the application interface.
* **static/images:** Directory for storing uploaded image files.

**Additional Notes**

* You can adjust the number of search results returned by modifying the `LIMIT` clause in the SQL query within
  the `search_embedding` function.

**By following these instructions, you should be able to successfully set up and use this image search engine project.** 

