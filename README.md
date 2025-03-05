# SSM-ISRO-Project

This project contains a web-based platform to analyze and visualize data obtained from the Scanning Sky Monitor (SSM) onboard India's Astrosat satellite. By addressing challenges such as data complexity, accessibility, and scalability, this system provides researchers with tools to explore and interpret light curves and spectra effectively.

The platform integrates advanced visualization techniques, user-friendly interfaces, and robust data management features to empower astronomers and researchers in time-domain astrophysics.

---

## Features
- **Data Handling:** Supports multiple file types, including FITS, ORB, and LBT. Handles Level 0, Level 1, and Level 2 SSM data.
- **Visualization:** Interactive light curves and spectra plotted using Plotly.js. Real-time visualization capabilities for transient event analysis.
- **Calibration:** Utilizes the Astropy library for data calibration, ensuring accurate and reliable insights.
- **Directory Management:** Organized file structures for seamless data access and analysis.
- **Collaboration:** Enables users to share data and visualizations within the platform.
- **Security:** Compliance with data privacy regulations.

---

## Technology Stack
- **Frontend:** HTML, CSS, JavaScript, Plotly.js
- **Backend:** Django Framework
- **Directory:** Path traversal method used
- **Modules Used:**
  - Astropy (for reading and calibrating FITS data)
  - NumPy and Pickle (for data processing and storage)

---

## System Requirements
- Python 3.10+
- Django 4.x
- Dependencies (Install via `requirements.txt`):
  - Astropy
  - NumPy
  - Plotly
  - Django
 
---

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-repository-name.git
   cd your-repository-name
   ```
2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Run Migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
4. **Start the Server:**
   ```bash
   python manage.py runserver
   ```
5. **Access the Application:**
   Open your browser and navigate to http://127.0.0.1:8000/

---

## Usage

1. **Home Page**: A small description about the project and the starting portal
2. **Date Selection**: Select the start date and end date of the data you wanted to visualize
3. **Visualization**: Here select the column you want and visualize as Scatter, Line as well as correlation
4. **Collabration**: Share visualizations or datasets with other users on the platform

---

## Testing
The system undergoes multiple testing phases:
- **Unit Testing:** Tests individual components like data handlers and visualization components.
- **Integration Testing:** Ensures seamless communication between different system components.
- **Performance Testing:** Evaluates system response and data rendering speed.
- **Visualization Testing:** Validates the accuracy and inteactovity of light curve and spectra plots.

- ---

## Future Enhancements
- Expand visualization techniques to include 3D plots and heatmaps.
- Implement real-time collaboration and data sharing.
- Host the platform on a cloud service for better scalability.
- Extend support to multi-wavelength data integration.

---

## Contributors
- Abishek Kumar
- Anush Bhat

---

## Acknowledgments
- ISRO for providing SSM data and virtual environment access.
- The open-source community for developing libraries like Astropy and Plotly.
- All contributors and collaborators for their support and insights.

