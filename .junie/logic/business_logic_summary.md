# ProjectCare Business Logic Summary

## Overview

ProjectCare is a web application that connects elderly people and their responsible caregivers with professional caregivers. The system facilitates the creation and management of care contracts between these parties.

## Core Entities

### User
The base entity for all users in the system. Contains personal information such as name, contact details, and authentication credentials. A User can be associated with one of three roles: Caregiver, Responsible, or Elderly.

### Caregiver
Represents a professional caregiver who provides care services. Contains professional information such as specialty, experience, education, and skills. Each Caregiver is linked to exactly one User.

### Responsible
Represents a person who is responsible for one or more elderly people. Each Responsible is linked to exactly one User and can be associated with multiple Elderly people and Contracts.

### Elderly
Represents an elderly person who needs care. Contains specific information relevant to elderly care. Each Elderly is linked to exactly one User and exactly one Responsible.

### Contract
Represents an agreement between a Responsible and a Caregiver for care services. Contains start and end dates for the service period. Each Contract is linked to exactly one Responsible and exactly one Caregiver.

## Key Relationships

1. **User-Role Relationship**: A User can be either a Caregiver, a Responsible, or an Elderly (one-to-one relationship with one of these roles).

2. **Responsible-Elderly Relationship**: A Responsible can be responsible for multiple Elderly people, but each Elderly person has exactly one Responsible (one-to-many relationship).

3. **Contract Relationships**: 
   - A Responsible can initiate multiple Contracts (one-to-many relationship).
   - A Caregiver can be associated with multiple Contracts (one-to-many relationship).
   - Each Contract connects exactly one Responsible with exactly one Caregiver.

## Core Business Processes

### User Registration
1. A user registers with basic personal information.
2. The user selects a role (Caregiver, Responsible, or Elderly).
3. The user provides additional information specific to the selected role.
4. The system creates the appropriate profile for the user.

### Authentication
1. A user provides their email and password.
2. The system verifies the credentials.
3. If valid, the system creates a session for the user.

### Care Service Process
1. A Responsible registers in the system.
2. The Responsible registers Elderly people under their care.
3. The Responsible searches for available Caregivers.
4. The Responsible selects a Caregiver and creates a Contract.
5. The Caregiver provides care services according to the Contract.
6. The Responsible can rate the Caregiver's services.

## Business Rules and Constraints

1. **User Uniqueness**: Each User must have a unique email, CPF, and phone number.

2. **Profile Type**: A User can be either a Caregiver, a Responsible, or an Elderly.

3. **Elderly Responsibility**: Each Elderly must be associated with exactly one Responsible.

4. **Contract Validity**: A Contract's end date must be after its start date.

5. **Caregiver Registration**: A Caregiver must provide professional information such as specialty, experience, education, and skills.

6. **Responsible Registration**: A Responsible is created simply by associating a User with the Responsible role.

7. **Elderly Registration**: An Elderly must be associated with a Responsible and must provide additional information such as birthdate and gender.

## Security Considerations

1. **Password Security**: User passwords are hashed using the Argon2 algorithm before being stored in the database.

2. **Session Management**: User sessions are managed using Flask's session mechanism.

3. **Input Validation**: User inputs are validated to prevent security vulnerabilities.

## Conclusion

The ProjectCare application implements a comprehensive business logic for connecting elderly people and their responsible caregivers with professional caregivers. The system's data model and business processes are designed to facilitate the creation and management of care contracts while ensuring data integrity and security.