# Student Budget App - README

## 1. Introduction
The **Student Budget App** is a financial management web application designed to help students track their income and expenses efficiently. The app provides a user-friendly dashboard, transaction management features, and graphical summaries to offer insights into spending habits.

## 2. How It Works
1. **User Registration/Login** – A new user signs up or logs in to access their personal dashboard.
2. **Adding Transactions** – Users can add income or expense transactions by selecting a category, amount, and date.
3. **Viewing Transactions** – The latest transactions are displayed on the dashboard, and users can view all transactions in a separate table.
4. **Editing/Deleting Transactions** – Users can modify or remove transactions from their history.
5. **Monthly Summary** – A visual summary using a **pie chart** and **bar chart** shows the breakdown of income and expenses by category.
6. **Contact Us** – Users can send feedback or inquiries through a contact form.

## 3. Screenshots

- **Home Page:** Introduction to the app. ![img_1.png](img_1.png)
- **Signup/Login Page:** User authentication interface. ![img_2.png](img_2.png)  ![img_3.png](img_3.png)
- **Dashboard:** Displays recent transactions and quick access to financial management. ![img_4.png](img_4.png) ![img_5.png](img_5.png)
- **Add Transaction Page:** Form to add new income or expense transactions. ![img_6.png](img_6.png)
- **Monthly Summary Page:** Graphical representation of user spending. ![img_7.png](img_7.png)
- **Contact Us Page:** Allows users to submit inquiries. ![img_8.png](img_8.png)

## 4. Setup Instructions
To run the project locally:
1. Clone the repository:
   ```bash
   git clone <[repository-link](https://github.com/Zainabm10/Group35-part-C.git)>
   ```
2. Navigate to the project directory:
   ```bash
   cd StudentBudgetApp
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a `.env` file and configure the MongoDB URI:
   ```plaintext
   DB_URI="mongodb+srv://dbstudentBudjet:ramy1106@studentbudgetdb.tdtyz.mongodb.net/?retryWrites=true&w=majority&appName=StudentBudgetDB"

   ```
5. Start the Flask server:
   ```bash
   python app.py
   ```
6. Open a browser and navigate to `http://127.0.0.1:5000`.

## 5. Notes
- If MongoDB is not running, the site will still function, but data will not persist.
- The **charts** on the summary page provide insights based on user data.
- Ensure all dependencies are installed to avoid errors.

---
**Project Team:** [Rami abu srihan 213006208 & zainab mohsen 324882810]  
**Submission Date:** [7.3.2025]
**prefer Email for test:**[ramy11062002@gmail.com  password 123456]
