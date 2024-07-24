# OCR Learning Project

This project demonstrates how to extract and store data from PDF files using OCR, and save it to a MySQL database.

## Video Demonstration

<div style="position: relative; padding-bottom: 64.90384615384616%; height: 0;">
  <iframe src="https://www.loom.com/embed/bdcc626e09b240f2a98c0e9a77531425?sid=9fd85024-a355-40bd-a5dd-1b2f1040a950" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe>
</div>

## Setup Instructions

1. **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

2. **Set Up Environment Variables:**
    Create a `.env` file with the following variables:
    ```plaintext
    DB_HOST=localhost
    DB_USER=root
    DB_PASS=YourPasswordHere
    DB_NAME=Receipts
    DB_URI=mysql+mysqlconnector://root:YourPasswordHere@localhost/Receipts
    ```

3. **Create Database and Tables:**
    Run the `create_db.py` script to create the database and tables:
    ```bash
    python create_db.py
    ```

4. **Run the Application:**
    ```bash
    python app.py
    ```

## Usage

1. **Upload a PDF File:**
    Navigate to the upload form and upload a PDF file.

2. **View Extracted Data:**
    The extracted data will be displayed in JSON format and saved to the MySQL database.

## Contributing

Feel free to fork this repository and make contributions.

## License

This project is licensed under the MIT License.
