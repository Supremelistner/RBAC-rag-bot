# RBAC-Enabled Retrieval-Augmented Generation (RAG) Bot  
_A Role-Based Access Controlled AI Question-Answering System_

---

## 📌 Project Overview

This project implements a secure **RBAC-powered RAG (Retrieval-Augmented Generation) system** that answers user queries based strictly on the documents available to their assigned roles.

It integrates:

- **JWT authentication**
- **Role-based access control**
- **Vector similarity search (ChromaDB)**
- **HuggingFace LLM (FLAN-T5)**
- **Streamlit frontend**
- **FastAPI backend**

Users log in, ask questions, and get AI-generated answers **only from the documents they are authorized to view**.

---

## 🎯 Purpose

The goal of this project is to showcase how AI assistants can be made secure and enterprise-ready by enforcing:

- **Access control on document retrieval**
- **Strict role filtering in the RAG pipeline**
- **Secure authentication**
- **Private, offline LLM inference**

This makes the system suitable for:

✔ Internal knowledge assistants  
✔ Corporate AI tools  
✔ College project submissions  
✔ Research on secure RAG architectures  

---

## 🧩 Features

### ✔ Role-Based Access Control (RBAC)
Each user belongs to a role (e.g., Marketing, HR).  
The system retrieves only documents belonging to that role.

### ✔ JWT Authentication
Every request is authenticated using a secure token.

### ✔ RAG Pipeline with ChromaDB
- PDF ingestion  
- Chunking  
- Embedding  
- Storage with metadata  
- Top-k retrieval  

### ✔ Local LLM Inference
Uses **google/flan-t5-base** — lightweight and runs on CPU.

### ✔ Streamlit UI
Simple UI to log in, ask questions, and view sources.

---



