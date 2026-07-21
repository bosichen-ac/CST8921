# CST8921 Lab 10: Building a RAG Solution with Azure AI Search + Self-Hosted Models on Kubernetes

- Name: Bosi Chen
- Student ID: 041040774
- Course: CST8921 Cloud Industry Trends
- Lab: Lab 10 - Building a RAG Solution with Azure AI Search + Self-Hosted Models on Kubernetes

---

## Introduction

This lab showed how to build a Retrieval-Augmented Generation (RAG) application using Azure AI Search and a self-hosted Ollama model. The workflow includes data ingestion, hybrid and semantic retrieval, grounded response generation, and Azure RBAC-based security.

---

## Workflow

### Module 0: Provisioning

Due to the shared Kubernetes cluster no longer being available, the instructor instructed us to run Ollama locally instead of using the in-cluster model server.

**Creating Resources**

Created Azure AI Search and configured Ollama to run locally.

![0-1](/Lab10/Screenshots/0-1.png)
![0-2](/Lab10/Screenshots/0-2.png)

### Module 1: Data Ingestion & Indexing

Created a vector-enabled Azure AI Search index (768-dimensional embeddings) and uploaded the document chunks successfully.

![1-1](/Lab10/Screenshots/1-1.png)
![1-2](/Lab10/Screenshots/1-2.png)

### Module 2: Cognitive Search: Hybrid + Semantic Retrieval

Hybrid search combined keyword search, vector search, and semantic ranking to retrieve the most relevant document chunks.

![2-1](/Lab10/Screenshots/2-1.png)
![2-2](/Lab10/Screenshots/2-2.png)

### Module 3: Ground the AI Response

On the first attempt the local model failed to answer in-scope questions.
![3-1](/Lab10/Screenshots/3-1.png)

After updating the prompt with a more detailed instruction and setting the temperature to 0, the model could generate in-scope responses with source citations and refuse out-of-scope questions both correctly.
![3-2](/Lab10/Screenshots/3-2.png)

### Module 4: Security & Governance

Configured Azure RBAC authentication using DefaultAzureCredential. After local authentication was disabled, key-based authentication failed while RBAC-authenticated queries continued to work.

The key-based call failed.
![4-1](/Lab10/Screenshots/4-1.png)

The RBAC-authenticated client still worked.
![4-2](/Lab10/Screenshots/4-2.png)

Module 4.2 Governing the model-serving tier in Kubernetes part was skipped because the lab was adapted to run Ollama locally instead of using the shared AKS cluster.