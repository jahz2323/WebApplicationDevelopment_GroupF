# Factory Machinery Status & Repair Tracking System
# User Guide

**Authors:**
- Jahziel Belmonte
- Thomas Viard

## Table of Contents
1. [Introduction](#introduction)
2. [System Overview](#system-overview)
3. [Getting Started](#getting-started)
   - [Accessing the System](#accessing-the-system)
   - [User Accounts and Roles](#user-accounts-and-roles)
   - [Logging In](#logging-in)
   - [Navigation](#navigation)
4. [For Managers](#for-managers)
   - [Dashboard Overview](#manager-dashboard-overview)
   - [Adding New Machinery](#adding-new-machinery)
   - [Managing Machinery](#managing-machinery)
   - [Assigning Technicians and Repair Staff](#assigning-technicians-and-repair-staff)
   - [Generating Reports](#generating-reports)
   - [User Management](#user-management)
5. [For Technicians](#for-technicians)
   - [Dashboard Overview](#technician-dashboard-overview)
   - [Viewing Assigned Machinery](#viewing-assigned-machinery)
   - [Reporting Warnings](#reporting-warnings)
   - [Creating Fault Cases](#creating-fault-cases)
   - [Adding Comments to Faults](#adding-comments-to-faults)
6. [For Repair Staff](#for-repair-staff)
   - [Dashboard Overview](#repair-dashboard-overview)
   - [Viewing Assigned Repairs](#viewing-assigned-repairs)
   - [Resolving Faults](#resolving-faults)
   - [Removing Warnings](#removing-warnings)
7. [Common Features](#common-features)
   - [Machinery List](#machinery-list)
   - [Fault Case Details](#fault-case-details)
   - [Commenting on Faults](#commenting-on-faults)
   - [Uploading Images](#uploading-images)
8. [For IT Staff](#for-it-staff)
   - [System Architecture](#system-architecture)
   - [Installation and Deployment](#installation-and-deployment)
   - [Database Management](#database-management)
   - [Backup and Recovery](#backup-and-recovery)
   - [Troubleshooting](#troubleshooting)
9. [Glossary](#glossary)
10. [Support](#support)

## Introduction

The Factory Machinery Status & Repair Tracking System is a comprehensive web application designed to monitor, manage, and maintain factory machinery. This system enables efficient tracking of machinery status, reporting of issues, and coordination of repair activities.

This user guide provides detailed instructions for all user types on how to use the system effectively.

## System Overview

The system provides the following core functionalities:

- **Machinery Management**: Add, view, and manage machinery across different collections or groups
- **Status Monitoring**: Track machinery status (OK, WARNING, FAULT) in real-time
- **Fault Reporting**: Report and document machinery issues with detailed descriptions and images
- **Repair Coordination**: Assign repair tasks and track resolution progress
- **User Management**: Manage user accounts with different roles and permissions
- **Data Visualization**: View charts and reports on machinery performance and status

## Getting Started

### Accessing the System

The Factory Machinery Status & Repair Tracking System is a web-based application that can be accessed through any modern web browser (Chrome, Firefox, Safari, Edge).

To access the system:
1. Open your web browser
2. Enter the URL provided by your IT department (typically http://localhost:8000 for local installations)
3. You will be directed to the system's homepage

### User Accounts and Roles

The system has four main user roles, each with different permissions:

1. **Managers**:
   - Can view all machinery
   - Can add, delete, and update machinery
   - Can assign technicians and repair staff to machinery
   - Can generate reports
   - Can comment on fault cases

2. **Technicians**:
   - Can view assigned machinery
   - Can add warnings to machinery
   - Can create fault cases
   - Can comment on fault cases

3. **Repair Staff**:
   - Can view assigned machinery
   - Can remove warnings from machinery
   - Can resolve fault cases
   - Can comment on fault cases

4. **View-only Users**:
   - Can view machinery information
   - Cannot make any changes to the system

### Logging In

To log in to the system:

1. Click on the "Login" button in the top-right corner of the homepage
2. Enter your username and password
   - For sample accounts, use the following credentials:
     - Admin: username "admin", password "admin"
     - Other sample users: password "project123"
3. Click "Login"
4. Upon successful login, you will be redirected to the dashboard

### Navigation

The system has a consistent navigation structure:

- **Top Navigation Bar**: Contains links to main sections and login/logout options
- **Left Menu**: Appears when hovering near the left edge of the screen, providing access to various features
- **Dashboard**: The main control center with role-specific views and features
- **Machinery List**: A comprehensive list of all machinery with filtering options
- **User Management**: For managers to manage user accounts (accessible from the dashboard)

## For Managers

### Manager Dashboard Overview

As a manager, your dashboard provides a comprehensive overview of the factory's machinery status and operations:

- **Status Charts**: Visual representation of machinery status distribution (OK, WARNING, FAULT)
- **Downtime Charts**: Shows downtime for machinery with FAULT status
- **Add Machinery Form**: Allows you to add new machinery to the system
- **Update Machinery Form**: Allows you to update existing machinery
- **File Reports Section**: Create reports for specific machinery

### Adding New Machinery

To add new machinery:

1. Navigate to your dashboard
2. Locate the "Add Machinery" form
3. Fill in the required information:
   - Machine Name
   - Description
   - Importance (higher value means more important)
   - Collection (optional)
   - Assigned Technicians (optional)
   - Assigned Repair Staff (optional)
4. Click "Add Machine"
5. The new machinery will be added to the system and appear in the machinery list

### Managing Machinery

To manage existing machinery:

1. Navigate to the Machinery List
2. Find the machinery you want to manage
3. Click "View More" to see detailed information
4. From the detail page, you can:
   - Update machinery information
   - Delete machinery (use with caution)
   - View fault history
   - Assign technicians and repair staff

### Assigning Technicians and Repair Staff

To assign personnel to machinery:

1. Navigate to your dashboard
2. Locate the "Update Machinery" form
3. Select the machinery you want to update
4. Choose technicians and repair staff from the dropdown lists
5. Click "Update Machine"
6. The assignments will be updated in the system

### Generating Reports

To generate reports:

1. Navigate to your dashboard
2. Locate the "File Reports" section
3. Select the machinery you want to include in the report
4. Enter report details in the text box
5. Click "Update Machine"
6. The report will be generated and can be viewed or downloaded

### User Management

To manage user accounts:

1. Navigate to the User Management section from your dashboard
2. View a list of all users with their roles and assigned machinery
3. To add a new user, click "Add User" and fill in the required information
4. To edit a user, click "Edit" next to the user's name
5. To delete a user, click "Delete" next to the user's name (use with caution)

## For Technicians

### Technician Dashboard Overview

As a technician, your dashboard focuses on the machinery assigned to you:

- **Assigned Machinery Overview**: Shows all machinery assigned to you with status indicators
- **Status Summary**: Displays the count of OK vs. total assigned machinery
- **Quick Access**: Links to view details and report issues for your assigned machinery

### Viewing Assigned Machinery

To view your assigned machinery:

1. Navigate to your dashboard
2. Your assigned machinery will be displayed with status indicators
3. Click on any machinery card to view more details
4. From the detail page, you can see the machinery's status, description, and fault history

### Reporting Warnings

To report a warning for machinery:

1. Navigate to the machinery detail page
2. Locate the "Add Warning" section
3. Enter the warning details in the text box
4. Click "Submit Warning"
5. The machinery status will be updated to WARNING

### Creating Fault Cases

To create a fault case:

1. Navigate to the machinery detail page
2. Click "Report a Fault"
3. Fill in the fault details:
   - Title: A brief description of the fault
   - Details: A comprehensive description of the issue
   - Image (optional): Upload an image of the fault
4. Click "Create Fault"
5. The machinery status will be updated to FAULT

### Adding Comments to Faults

To add comments to an existing fault:

1. Navigate to the fault detail page
2. Scroll down to the comment section
3. Enter your comment in the text box
4. Click "Submit Comment"
5. Your comment will be added to the fault case

## For Repair Staff

### Repair Dashboard Overview

As repair staff, your dashboard focuses on machinery that needs repair:

- **Assigned Repairs Overview**: Shows all machinery assigned to you for repair
- **Status Summary**: Displays the count of OK vs. total assigned machinery
- **Quick Access**: Links to view details and resolve issues for your assigned machinery

### Viewing Assigned Repairs

To view your assigned repairs:

1. Navigate to your dashboard
2. Your assigned machinery will be displayed with status indicators
3. Click on any machinery card to view more details
4. From the detail page, you can see the machinery's status, description, and fault history

### Resolving Faults

To resolve a fault:

1. Navigate to the fault detail page
2. Review the fault details and any comments
3. Add your own comment describing the resolution
4. Check the "Mark as Resolved" checkbox
5. Click "Submit"
6. The fault will be marked as resolved, and the machinery status will be updated accordingly

### Removing Warnings

To remove a warning:

1. Navigate to the machinery detail page
2. Locate the warning in the warnings list
3. Click "Remove Warning"
4. The warning will be removed, and the machinery status will be updated accordingly

## Common Features

### Machinery List

The Machinery List provides a comprehensive view of all machinery in the system:

1. Navigate to "Machinery List" from the left menu
2. View all machinery with basic information
3. Filter machinery by collection using the dropdown menu
4. Click "View More" on any machinery card to see detailed information

### Fault Case Details

The Fault Case Details page provides comprehensive information about a specific fault:

1. Navigate to a fault case from the machinery detail page
2. View fault details including title, description, creation date, and status
3. See uploaded images related to the fault
4. Read comments from technicians and repair staff
5. Add your own comments or images
6. Resolve the fault (if you have permission)

### Commenting on Faults

Commenting on faults is a key feature for communication between technicians and repair staff:

1. Navigate to the fault detail page
2. Scroll down to the comment section
3. Enter your comment in the text box
4. Click "Submit Comment"
5. Your comment will be added to the fault case with your username and timestamp

### Uploading Images

Images can be uploaded to document faults:

1. Navigate to the fault detail page
2. Scroll down to the comment section
3. Click "Choose File" next to the image upload field
4. Select an image from your computer
5. Add a comment to accompany the image
6. Click "Submit"
7. The image will be uploaded and associated with the fault case

## For IT Staff

### System Architecture

The Factory Machinery Status & Repair Tracking System is built using the following technologies:

- **Backend**: Django (Python web framework)
- **Frontend**: HTML, CSS, JavaScript, Bootstrap
- **Database**: SQLite (default) or any database supported by Django
- **Containerization**: Docker (optional)

The system follows a Model-View-Template (MVT) architecture:
- **Models**: Define the data structure (App/models.py)
- **Views**: Handle user requests and business logic (App/views.py)
- **Templates**: Define the user interface (templates/ directory)

### Installation and Deployment

#### With Docker

1. Install Docker and Docker Compose
2. Clone the repository
3. Run `docker-compose up -d --build`
4. Access the application at http://localhost:8000

#### Without Docker

1. Clone the repository
2. Create a virtual environment: `python -m venv environment`
3. Activate the virtual environment: `environment\Scripts\activate`
4. Install dependencies: `pip install --no-cache-dir -r requirements.txt`
5. Create group roles: `python manage.py setup_groups`
6. Run migrations: `python manage.py migrate`
7. Load sample data:
   ```
   python manage.py loaddata App/fixtures/collections.json
   python manage.py loaddata App/fixtures/users.json
   python manage.py loaddata App/fixtures/machineries.json
   python manage.py loaddata App/fixtures/machineryfaults.json
   ```
8. Start the server: `python manage.py runserver`
9. Access the application at http://localhost:8000

### Database Management

The system uses Django's ORM (Object-Relational Mapping) to interact with the database:

- **Models**: Defined in App/models.py
- **Migrations**: Generated automatically by Django
- **Admin Interface**: Available at /admin/ for superusers

To perform database operations:
- Create migrations: `python manage.py makemigrations`
- Apply migrations: `python manage.py migrate`
- Create superuser: `python manage.py createsuperuser`

### Backup and Recovery

To backup the database:
1. For SQLite: Copy the db.sqlite3 file
2. For other databases: Use database-specific backup tools

To restore from backup:
1. For SQLite: Replace the db.sqlite3 file
2. For other databases: Use database-specific restore tools

### Troubleshooting

Common issues and solutions:

1. **Login Issues**:
   - Check username and password
   - Ensure the user account is active
   - Verify the user has the correct group assignment

2. **Permission Issues**:
   - Check user group assignments
   - Verify permissions in setup_groups.py
   - Run `python manage.py setup_groups` to reset permissions

3. **Database Issues**:
   - Check database connection settings in settings.py
   - Ensure migrations are up to date
   - Verify database file permissions

4. **Docker Issues**:
   - Check Docker and Docker Compose installation
   - Verify port mappings in docker-compose.yml
   - Check container logs: `docker-compose logs`

## Glossary

- **Collection**: A logical grouping of machinery (e.g., Assembly Line A, Packaging Line)
- **Machinery**: Equipment being monitored and maintained in the system
- **Status**: Current state of machinery (OK, WARNING, FAULT)
- **Importance**: Priority level of machinery (higher value means more important)
- **Warning**: A minor issue with machinery that doesn't require immediate attention
- **Fault**: A significant issue with machinery that requires repair
- **Technician**: User responsible for monitoring machinery and reporting issues
- **Repair Staff**: User responsible for resolving machinery issues
- **Manager**: User responsible for overseeing the system and making administrative decisions

## Support

For additional support:

- Contact the system administrator
- Refer to the documentation in the project repository
- Submit issues through the designated support channel

---

© 2025 Factory Machinery Tracking System. All Rights Reserved.
