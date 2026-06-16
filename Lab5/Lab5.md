# CST8921 Lab 5：Serverless Computing

- Name: Bosi Chen
- Student ID: 041040774
- Course: CST8921 Cloud Industry Trends
- Lab: Lab 5 - Serverless Computing
- Submission Date: Jun 15, 2026

---

## Introduction

The purpose of this lab was to explore serverless computing using Azure services. The lab showed how Azure Event Grid and Azure Functions can be integrated to automatically process file uploads to Azure Blob Storage. 

By implementing a serverless architecture, event-driven workloads can be executed without managing servers or infrastructure.

The key task was to upload a file to Azure Blob Storage, automatically trigger an Azure Function using Event Grid, retrieve information about the uploaded file, and validate the end-to-end execution through Azure logs and monitoring tools.

## Workflow

The serverless workflow implemented in this lab consists of the following steps:

1. A JSON file is uploaded to Azure Blob Storage.
2. Azure Event Grid detects the Blob Created event.
3. Event Grid triggers the Azure Function.
4. The Azure Function extracts the event information and retrieves the Blob URL.
5. Execution details are logged through Azure Functions and Application Insights.

This is an event-driven serverless design where services communicate automatically without manual intervention.

## Implementation

### Storage Configuration

A Storage Account was created and a Blob Container named `raw-data` was configured. The container was used to store test files that would generate Event Grid events.

![storage account](/Lab5/screenshots/storage-acc.png)

### Azure Function

An Event Grid Trigger Function named `ProcessBlobUpload` was created.

The function performed the following tasks:

- Receives Event Grid notifications
- Extracts the uploaded Blob URL from the event payload
- Logs event information
- Attempts to retrieve the uploaded file contents
- Records execution information for monitoring purposes

![function app](/Lab5/screenshots/function-app.png)
![code](/Lab5/screenshots/code.png)

The integration route showed as follow:

![integration](/Lab5/screenshots/integration.png)

### Event Subscription

An Event Grid Subscription was added to the Storage Account.

```
Event Type: Blob Created
Endpoint Type: Azure Function
Function: ProcessBlobUpload
```

Whenever a new file was uploaded to the `raw-data` container, the Event Grid would invoke the Azure Function automatically.

![events](/Lab5/screenshots/events.png)
![event subscription](/Lab5/screenshots/event-subscription.png)

### Testing and Validation

A sample JSON file named `wind_data.json` was uploaded to the Blob container `raw-data`.

![container](/Lab5/screenshots/container.png)

After uploading the file, Azure Function logs confirmed that the Event Grid trigger fired successfully.

The logs showed:

![logs](/Lab5/screenshots/logs.png)

While the invocations showed:

![invocations](/Lab5/screenshots/invocations.png)

The successful execution confirmed that the end-to-end serverless workflow was functioning correctly.

## Challenges Encountered

1. Creating Function

Azure Functions in Flex Consumption plan had to be deployed using VS Code and the Azure Functions extension. Some additional configuration was also required to ensure the Event Grid trigger function was correctly detected and registered after deployment.

![vscode](/Lab5/screenshots/vscode.png)

2. Function Detection Issues

The updated Azure Function in step D1 was not detected after deployment. This happened because the Event Grid trigger function needed to follow the Azure Functions Python v2 programming model requirements. The function entry point and decorator configuration were adjusted to align with requirements.

3. Dependency Management

The deployment initially failed because the required `requests` package was not included in the `requirements.txt` and thus not installed. Installing the dependency and updating the `requirements.txt` resolved the issue.

4. Storage Access Restrictions

Although the Azure Function received the Blob URL from the Event Grid event successfully, retrieving the blob contents through a direct HTTP request resulted in a PublicAccessNotPermitted error because anonymous access was disabled on the storage account.

## Analysis

This lab shows the advantages of serverless computing and event-driven architectures. 

Azure Event Grid efficiently detected storage events and automatically triggered Azure Functions without requiring manual intervention or dedicated infrastructure.

The benefits of serverless model:

- Automatic scaling
- Pay-per-use pricing
- Event-driven processing
- Simplified integration between Azure services

The integration of Blob Storage, Event Grid, and Azure Functions provides an effective architecture for processing uploaded files, IoT data, and other real-time events.

The lab also highlighted practical considerations such as deployment configuration, dependency management, and storage security settings.

## Conclusion

In this lab, Azure Blob Storage, Event Grid, and Azure Functions were integrated to create an event-driven serverless workflow. Uploading a file to Blob Storage automatically triggered an Azure Function, which processed the event information and logged execution details.

The successful end-to-end execution confirmed the serverless architecture is working and showed how Azure services can be combined to build scalable and efficient cloud-native solutions.