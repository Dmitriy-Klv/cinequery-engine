# Privacy Policy

**Last Updated:** March 2026

This document describes how data is handled within the **CineQuery Engine**. 

## 1. Scope of Responsibility
This is an open-source software project. The "Data Controller" is the individual or entity that installs and operates this application. The author of the source code does not have access to, nor does he collect or store, any data processed by independent installations of this software.

## 2. Types of Data Processed
The application is designed to function with minimal data processing. It only handles:
* **Search Queries:** Keywords entered by the user (e.g., movie titles or genres).
* **Metadata:** Timestamps of searches and the number of results found.
* **Database Credentials:** Stored locally in your `.env` file to connect to your MySQL and MongoDB instances.

## 3. Purpose of Processing
Data is processed locally on the user's infrastructure for the following purposes:
* Executing movie searches within the MySQL database.
* Generating local analytics, such as the "Top 5 Popular Queries".
* Displaying a local search history for the user's convenience.

## 4. No Collection of Personal Information
To ensure maximum privacy, this application **does not** collect:
* IP Addresses.
* Names, emails, or other personally identifiable information (PII).
* Browser fingerprints or tracking cookies.

## 5. Third-Party Access and Transfers
* **Local Storage:** All search logs are stored in the MongoDB instance defined by the user. 
* **No External Transmission:** No data is transmitted to the author or any third-party analytics services.

## 6. User Control and Rights
In alignment with data protection principles, users have full control over their information:
* **Transparency:** You can review all logged data anytime through the "History" and "Analytics" sections in the application.
* **Data Deletion:** You have the right to delete all logs at any time by clearing your MongoDB collection.
* **Opt-out:** You can stop all data processing simply by closing the application or modifying the logging logic in the source code.

## 7. Security Recommendations
To maintain data security, it is strongly recommended to:
* Never commit your `.env` file to public repositories.
* Use encrypted connections (TLS/SSL) if your database is hosted on a remote server.

## 8. Disclaimer
This software is provided "as is" for educational purposes. The author is not liable for any data breaches or legal issues resulting from insecure configurations or misuse by the operator.
