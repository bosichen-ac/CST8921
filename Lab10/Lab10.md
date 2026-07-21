# CST8921 Lab 10: Building a RAG Solution with Azure AI Search + Self-Hosted Models on Kubernetes

- Name: Bosi Chen
- Student ID: 041040774
- Course: CST8921 Cloud Industry Trends
- Lab: Lab 10 - Building a RAG Solution with Azure AI Search + Self-Hosted Models on Kubernetes

---

## Introduction


---

## Workflow

### Module 0: Provisioning

Due to the shared Kubernetes cluster from the previous CloudLabs session no longer being available, the instructor instructed us to run Ollama locally instead of using the in-cluster model server.

**Creating Resources**

Creating Azure AI Search and import Ollama locally.

![0-1](/Lab10/Screenshots/0-1.png)
![0-2](/Lab10/Screenshots/0-2.png)

### Module 1: Data Ingestion & Indexing

![1-1](/Lab10/Screenshots/1-1.png)
![1-2](/Lab10/Screenshots/1-2.png)

### Module 2: Cognitive Search: Hybrid + Semantic Retrieval

![2-1](/Lab10/Screenshots/2-1.png)
![2-2](/Lab10/Screenshots/2-2.png)

### Module 3: Ground the AI Response

The first attempt failed to answer in scope.
![3-1](/Lab10/Screenshots/3-1.png)

Modified the prompt and set temperature to 0.
![3-2](/Lab10/Screenshots/3-2.png)

### Module 4: Security & Governance

The key-based call failed.
![4-1](/Lab10/Screenshots/4-1.png)

The RBAC-authenticated client still worked.
![4-2](/Lab10/Screenshots/4-2.png)

Governing the model-serving tier in Kubernetes part was skipped because the lab was adapted to run Ollama locally instead of using the shared AKS cluster.