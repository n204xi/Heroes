# AI Friend Chatbot Database Documentation

This README file provides information about the database used in the AI Friend Chatbot project.

## Overview

The database is designed to store messages, user information, and shared files. It supports the functionality of the chatbot by ensuring that all interactions are logged and accessible for future reference.

## Database Schema

The database schema is defined in the `schema.sql` file located in this directory. It includes the necessary tables and relationships to support the application's features, such as:

- Users: Stores user information and preferences.
- Messages: Logs all messages exchanged between the user and the AI.
- Files: Manages uploaded documents and images.

## Setup Instructions

1. **Create the Database**: Use the SQL commands in `schema.sql` to create the database and its tables.
2. **Configure Database Connection**: Ensure that your backend application is configured to connect to this database. Update the connection settings in your backend configuration files as necessary.

## Usage

The database is accessed through the backend application, which handles all interactions with the stored data. Ensure that the backend services are running to enable communication with the database.

For more detailed information on how to interact with the database through the backend, refer to the backend documentation.