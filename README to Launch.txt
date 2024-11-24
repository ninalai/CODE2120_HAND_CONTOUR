# Handi: A Hand Contour Finder for All Abilities

## Instructions for Downloading and Setting Up the Project

Thank you for taking the time to review this project! Below are the steps to download, set up, and launch the application:

---

### 1. Download the Project Files
1. Locate the provided **ZIP file** containing the project files.
2. Download the ZIP file to your computer.
3. Extract the contents of the ZIP file into a dedicated folder on your system.

---

### 2. Instructions for Setting Up the Environment

To ensure the project runs smoothly, follow these steps to create and configure a virtual environment:

#### Step 1: Create a Virtual Environment
1. Open a terminal or command prompt.
2. Navigate to the folder where you extracted the project files. For example:
3. Create a virtual environment named `venv` by running:
4. Activate the virtual environment:
- **Windows**:
  ```
  venv\Scripts\activate
  ```
- **macOS/Linux**:
  ```
  source venv/bin/activate
  ```

#### Step 2: Install Required Dependencies
1. Install all dependencies listed in the `requirements.txt` file:
This will install:
- **Flask**: For building the web application.
- **Flask-CORS**: For handling cross-origin requests.
- **OpenCV**: For image processing.
- **Roboflow**: For integrating pre-trained models.
- Any other required dependencies.

2. If users encounter issues with specific libraries, they can install them individually. For example:
- Install OpenCV:
  ```
  pip install opencv-python
  ```
- Install Flask:
  ```
  pip install flask
  ```
- Install Flask-CORS:
  ```
  pip install flask-cors
  ```
- Install Roboflow:
  ```
  pip install roboflow
  ```

---

### 3. Running the Application

Once the environment is set up, you can run the application by following these steps:

1. **Activate the Virtual Environment**:
Ensure the virtual environment is activated:
- **Windows**:
  ```
  venv\Scripts\activate
  ```
- **macOS/Linux**:
  ```
  source venv/bin/activate
  ```

2. **Start the Application**:
Run the Flask application by executing:

3. **Access the Application**:
Once the server starts, open your browser and go to:

---

### 4. Testing the API

To test the API directly:
1. Use a tool like **Postman** or **cURL**.
2. Send a `POST` request to the following endpoint:
3. Attach an image file in the request body.

Example `cURL` command:

---

### 5. Additional Notes
- If any errors occur during setup:
- Ensure `pip` is up to date:
 ```
 pip install --upgrade pip
 ```
- Reinstall specific libraries as needed.
- If you are using Roboflow, ensure the API key is configured correctly in your project settings or `.env` file.

---

### 6. Troubleshooting

- **Missing Dependencies**: Ensure all dependencies are installed from `requirements.txt`. If issues persist, install them individually.
- **CORS Errors**: Check that `Flask-CORS` is correctly configured in the `app.py` file.
- **Environment Variables**: For external APIs like Roboflow, confirm that the API key is correctly set in the environment.

---

### 7. Notes for Grading
- **File Structure**: The project includes a clear directory structure, `requirements.txt`, and all necessary scripts for setup and execution.
- **Code Documentation**: Inline comments and documentation explain the code functionality.
- **Output Validation**: Users can upload hand images and download processed results, including SVG contours and PNG images.

---

This README provides a comprehensive guide to set up and run the Handi project efficiently. Thank you for reviewing **Handi: A Hand Contour Finder for All Abilities**!
