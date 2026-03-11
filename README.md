# Sales Insight Automator

The **Sales Insight Automator** is a secure, containerized Quick-Response Tool designed to streamline the sales data analysis process for our executive leadership. It allows the team to upload massive `.csv` or `.xlsx` files, instantly processes the data via an AI model (Google Gemini), and emails a professional narrative summary to the requested recipient.

---

## The "Engineer's Log"

### 🚀 Getting Started

The application is fully containerized to ensure compatibility across our production environment. Follow these steps to spin it up locally:

#### Prerequisites
- **Git**
- **Docker** and **Docker Compose**
- Environment Variables (API Keys)

#### Setup Steps

1. **Clone the repository:**
   ```bash
   git clone <repository_url>
   cd sales-insight-automator
   ```

2. **Configure Environment Variables:**
   Copy the example environment file and fill in your actual credentials.
   ```bash
   cp .env.example .env
   ```
   *Required Keys:*
   - `GEMINI_API_KEY`: Get this from Google AI Studio.
   - `SMTP_USER` & `SMTP_PASS`: Your email credentials (use App Passwords for Gmail/M365).
   - `API_KEY`: Used to secure the internal endpoint. (Defaults to `dev_secret_key`).

3. **Start the Stack with Docker Compose:**
   ```bash
   docker-compose up --build
   ```
   This spins up both the **Frontend (Vite UI)** and the **Backend (FastAPI)** services.

4. **Access the Application:**
   - **Frontend UI:** Open [http://localhost:5173](http://localhost:5173) in your browser.
   - **Backend API Docs (Swagger):** Open [http://localhost:8000/docs](http://localhost:8000/docs)

---

### 🛡 Security Overview

The application is secured primarily using the following strategies:

- **API Endpoint Protection:** The `/api/upload` endpoint mandates an `X-API-Key` header. Requests lacking this exact matching key (set in `.env`) will be rejected with a `403 Forbidden` error. This guarantees that only authorized users or the authorized frontend application can trigger the resource-heavy AI generation and email dispatch.
- **Container Isolation:** The application separates the React SPA and the Python backend into their own independent Docker containers. They operate in a bridged secure network orchestrated by Docker Compose.
- **Background Processing:** File processing and AI API interactions are offloaded to FastAPI's BackgroundTasks. The endpoint itself immediately returns a HTTP 202 Accepted, protecting the server from timeout vulnerabilities or blocking I/O while waiting for the LLM response.
- **CORS Handling:** Implemented via FastAPI Middleware, restricting requests to authorized origins like our Vite instance (e.g., `http://localhost:5173`).

---

### ⛴ Deployment Strategy

The application is designed to be shipped instantly to cloud providers:

- **Frontend (Vercel / Netlify):** Can be deployed directly by connecting the GitHub repo and choosing the `frontend/` directory with `npm run build` commands.
- **Backend (Render / Railway):** Can be deployed by connecting the repository to Render, specifying the `backend/` directory, setting the Docker environment deployment, and attaching the `.env` configuration via the Render Dashboard.
- **CI/CD Automation:** A GitHub Action sits inside `.github/workflows/ci.yml`. On every PR to `main`, it runs parallel jobs to check the Python build, `npm run build` the Vite app, and validate the `docker-compose` build logic.

---

### 📚 Try it out!

There is a sample data file (`sales_q1_2026.csv`) provided in the prompt's context. Upload that file into the drag-and-drop zone, provide your email, input the API key (`dev_secret_key`), and await your executive summary!

*Built with ❤️ for the Rabbitt AI DevOps Team sprint.*
# sales-insight-automater
