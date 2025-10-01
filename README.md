# UAV Strategic Deconfliction System

This project is a strategic deconfliction system for UAVs, built for the FlytBase Technical Assessment. It checks a primary drone's mission for spatiotemporal conflicts with other air traffic and provides a 4D (3D space + time) visualization of the flights.

---

## 🚀 Setup

To get the project running locally, follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone <https://github.com/Abhijeet857/flytbase-assessment.gite>
    cd <cd flytbase-assessment>
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    # For Windows
    python -m venv venv
    .\venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

---

## ▶️ Execution

To run the simulation with the default conflict scenario, execute the following command from the root directory:

```bash
python main.py

To run the automated test suite, use the command:
```bash
pytest