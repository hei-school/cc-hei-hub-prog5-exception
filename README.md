# Exception Simulator

This project is an application designed to simulate various common errors encountered during file exchanges. The goal is to provide a testing environment for error management in an application dealing with files. In this case, we have chosen images only as a case study.
<br>
We can find the 2 implementations of the program in the different languages (Java and Python) by browsing the branch corresponding to each language.

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

## Usage

To test these exceptions, submit requests by following [the postman collection]("https://....").

The log of each exception can be found on the file named `applog.log` located at the root.

## License

This project is licensed under the [MIT License](LICENSE.md).
