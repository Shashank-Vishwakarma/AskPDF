# AskPDF 📄💬
AskPDF is a cutting-edge platform where users can upload PDF documents and interact with them through a chat interface. 
Powered by advanced technologies, AskPDF processes and indexes your documents, enabling seamless question-and-answer interactions.

---

### 🌟 Key Features
- **PDF Upload**: Upload and manage PDF documents with ease.
- **Interactive Chat**: Ask questions about the content of your PDF and get accurate responses.
- **Document Indexing**: Efficiently index PDFs for quick retrieval of relevant content.
- **Real-time Responses**: Enjoy fast and reliable interactions.
- **Secure Storage**: Ensure data safety with Supabase storage.
- **Groq-Optimized LLM**: Leverage high-performance machine learning for accurate and efficient responses.

---

## Tech Stack 🛠️

### **Frontend**
- **Next.js**: Framework for building the UI.
- **React.js**: Component-based architecture.
- **Zustand**: Lightweight state management.
- **TailwindCSS**: Responsive and modern styling.
- **Axios**: API requests made easy.

### **Backend**
- **FastAPI**: Backend framework for high performance.
- **Celery**: Task queue for asynchronous processing.
- **Qdrant**: Vector database for document chunk indexing.
- **LangChain**: AI-powered natural language processing.
- **Groq**: High-performance large language model execution.
- **Supabase Storage**: Secure file storage solution.
- **Postgres**: Reliable database for structured data.

---

## Screenshots 📸

### Dashboard Page
![askpdf-dashboard](https://github.com/user-attachments/assets/a3f672dc-1c45-4da9-9fba-c9f57683ac06)

### Chat Interface
![askpdf-chat-interface](https://github.com/user-attachments/assets/0a5c9d2a-5900-4b1f-bc76-8bf632e54ead)

### PDF Upload
![Screenshot 2025-06-27 220850](https://github.com/user-attachments/assets/c078cc54-251b-4511-8cc5-ff22c33417f9)

### Login Page
![Screenshot 2025-06-27 220926](https://github.com/user-attachments/assets/4bcf6262-4a2b-4fb2-8660-0f77bce96131)

### Register Page
![askpdf-register](https://github.com/user-attachments/assets/3aa4a571-f347-46b8-aa56-3e829f05b78a)

---

## How It Works ⚙️
- **Upload a PDF**: The user uploads a document.
- **Chunking and Indexing**: The PDF is processed, split into smaller chunks, and indexed using Qdrant.
- **Query Handling**: User queries are processed with LangChain and Groq for efficient and accurate answers.
- **Chat Interface**: Results are displayed in an intuitive and interactive chat format.
