
# Project Title

A brief description of what this project does and who it's for

# Exception Simulator

This project is an application designed to simulate various common errors encountered during file exchanges. The goal is to provide a testing environment for error management in an application dealing with files. In this case, we have chosen images only as a case study.
<br>
<br>
We can find the 2 implementations of the program in the different languages (Java and Python) by browsing the branch corresponding to each language.

- Python in the branch [feature/python](https://github.com/hei-school/cc-hei-hub-prog5-exception/tree/feature/python).
- Java in the branch [feature/java](https://github.com/hei-school/cc-hei-hub-prog5-exception/tree/feature/java).


## Description

For this exception simulator, we have a simple RESTful API application that allows image files to be uploaded and downloaded from endpoints.

## Requirement

[Download](https://www.python.org/downloads/) and install Python 3.10 or higher

## Installation

Install the dependencies of the python project with pip

```bash
  pip install fastapi
  pip install uvicorn
  pip install python-magic
  pip install schedule
```

## Usage

Go to the application's root directory, then run the command :

```bash
  python server.py
```

To test these exceptions, submit requests by following [the postman collection](https://raw.githubusercontent.com/hei-school/cc-hei-hub-prog5-exception/feature/python/docs/prog5p2.postman_collection.json).

## Features

### 1. `SensitiveFileException` (HTTP Status Code: 400)

This exception is raised when processing or attempting to upload or download a file that contains sensitive information, such as explicit terms like "Xxx" or "Sex" in its label. The exception is triggered to prevent the handling or dissemination of content that violates privacy or security policies.

### 2. `NotAuthorizedException` (HTTP Status Code: 401)

This exception is generated when access to a specific directory is denied. This can simulate a situation where a user tries to access a folder for which they do not have the necessary permissions.
<br>
<u>Example</u>: The user tries to upload a picture into Videos file.

### 3. `BadFileTypeException` (HTTP Status Code: 400)

This exception is thrown when a file of an unauthorized type is submitted. For example, if the application expects an image and receives a text file, this exception will be generated.
<br>
<u>Example</u>: The user tries to upload a picture `.mkv` extension.

### 4. `FileNameInvalidException` (HTTP Status Code: 400)

This exception indicates that a file is rejected due to an invalid filename. The application may apply specific rules regarding allowed filenames.
<br>
<u>Example</u>: The file name contains one or more of the following characters: :*<>?/\".

### 5. `DuplicateFileException` (HTTP Status Code: 400)

When a user tries to upload a file that already exists, this exception is thrown to signal a conflict with an existing file.
<br>
<u>Example</u>: File with the same name.

### 6. `LargeFileException` (HTTP Status Code: 413)

This exception is generated when the size of a file exceeds a predefined limit. This could simulate a restriction on the size of uploadable files.
<br>
<u>Example</u>: The user tries to upload an 8 MB-sized picture.

### 7. `NotFoundException` (HTTP Status Code: 404)

When a request is made to obtain a file that does not exist, this exception is thrown. It indicates that the requested file was not found.

### 8. `StockageInsuffisantException` (HTTP Status Code: 507)

This exception is thrown when there is insufficient storage space available on the server to process the request.

### 9. `ServerDownException` (HTTP Status Code: 503)

This exception is thrown when the server is temporarily unable to handle the request due to maintenance or other reasons.

### 10. `TooManyRequestException` (HTTP Status Code: 429)

Generated when a user exceeds the allowed number of requests within a specified time frame.
<br>
<u>Use Case</u>: The user tries to do 2 requests per second.

### 11. `RequestTimeOutException` (HTTP Status Code: 408)

Thrown when the server times out while waiting for a request to be completed.
<br>
<u>Use Case</u>: When a request takes more than 1 second to respond.

### 12. `NotImplementedException` (HTTP Status Code: 501)

Indicates that the server does not support the functionality required to fulfill the request.

### 13. `ServerErrorException` (HTTP Status Code: 500)

This exception is a generic server error that can be used for various unexpected server-side issues.

### 14. `CorruptedFileException` (HTTP Status Code: 500)

Thrown when a file is detected to be corrupted during the upload or download process.
<br>
<u>Use Case</u>: By using a file checker to determine whether the file is corrupted or not.

### 15. `LockedException` (HTTP Status Code: 423)

Indicates that the requested resource is locked and cannot be accessed.

### 16. `LegalReasonException` (HTTP Status Code: 453)

Thrown when access to a resource is denied for legal reasons.
## License

This project is licensed under the [MIT License](LICENSE.md).

[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-24ddc0f5d75046c5622901739e7c5dd533143b0c8e959d652212380cedb1ea36.svg)](https://classroom.github.com/a/wTBA-Etm)