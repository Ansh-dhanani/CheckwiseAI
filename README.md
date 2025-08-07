# CheckWise - AI-Powered CBC Analysis System

---

###Live : https://check-wise.netlify.app/

**CheckWise** is an intelligent medical diagnosis system that analyzes Complete Blood Count (CBC) test results to predict potential diseases using machine learning. The system combines advanced file processing, parameter extraction, and AI-powered analysis to provide healthcare insights.

---

## 🏗️ System Architecture

### Overview
CheckWise follows a **client-server architecture** with clear separation of concerns:

```
┌─────────────────┐    HTTP/REST API    ┌──────────────────┐
│   Frontend      │◄──────────────────►│    Backend       │
│   (React)       │                     │    (Flask)       │
│                 │                     │                  │
│ • User Interface│                     │ • File Processing│
│ • File Upload   │                     │ • ML Prediction  │
│ • Results Display│                     │ • Data Validation│
└─────────────────┘                     └──────────────────┘
                                                   │
                                                   ▼
                                        ┌──────────────────┐
                                        │   ML Models      │
                                        │                  │
                                        │ • Disease Model  │
                                        │ • Label Encoder  │
                                        └──────────────────┘
```

---

## 📁 Project Structure

```
CheckWise/
├── 🖥️ backend/                     # Python Flask API Server
│   ├── api.py                      # Main API endpoints & business logic
│   ├── file_processor.py           # File processing & data extraction
│   ├── requirements.txt            # Python dependencies
│   ├── cbc_disease_model.joblib    # Trained ML model for disease prediction
│   └── disease_label_encoder.joblib # Label encoder for disease names
│
├── 🌐 frontend/                    # React Web Application
│   ├── src/
│   │   ├── components/
│   │   │   ├── DiagnosisForm.jsx   # Main form component
│   │   │   └── ResultsDisplay.jsx  # Results visualization
│   │   ├── App.jsx                 # Main application component
│   │   ├── App.css                 # Application styles
│   │   └── main.jsx                # Application entry point
│   ├── package.json                # Node.js dependencies
│   ├── index.html                  # HTML template
│   └── vite.config.js              # Vite build configuration
│
├── 🚀 start-app.bat                # Application launcher script
├── 📋 README.md                    # This documentation
├── 🔧 git-setup.bat               # Git initialization script
└── 📝 .gitignore                  # Git ignore rules
```

---

## 🔄 Data Flow & System Workflow

### 1. File Upload Process
```
User Uploads File → Frontend → Backend API → File Processor → Extracted Data
     │                │           │              │               │
     │                │           │              │               ▼
     │                │           │              │        ┌─────────────┐
     │                │           │              │        │ Text/CSV    │
     │                │           │              │        │ Parsing     │
     │                │           │              │        └─────────────┘
     │                │           │              │               │
     │                │           │              │               ▼
     │                │           │              │        ┌─────────────┐
     │                │           │              │        │ Parameter   │
     │                │           │              │        │ Matching    │
     │                │           │              │        └─────────────┘
     │                │           │              │               │
     │                │           │              │               ▼
     │                │           │              │        ┌─────────────┐
     │                │           │              │        │ Data        │
     │                │           │              │        │ Validation  │
     │                │           │              │        └─────────────┘
```

### 2. AI Prediction Process
```
CBC Parameters → Data Preprocessing → ML Model → Disease Predictions → Results
      │                  │               │             │              │
      │                  │               │             │              ▼
      │                  │               │             │       ┌─────────────┐
      │                  │               │             │       │ Probability │
      │                  │               │             │       │ Scores      │
      │                  │               │             │       └─────────────┘
      │                  │               │             │              │
      │                  │               │             │              ▼
      │                  │               │             │       ┌─────────────┐
      │                  │               │             │       │ Top 5       │
      │                  │               │             │       │ Predictions │
      │                  │               │             │       └─────────────┘
```

---

## 🧠 Core Components Explained

### Backend Components

#### 1. **api.py** - Main API Server
**Purpose**: Central hub for all API endpoints and business logic

**Key Functions**:
- `load_models()`: Loads pre-trained ML models at startup
- `predict()`: Processes CBC data and returns disease predictions
- `upload_file()`: Handles file uploads and triggers data extraction
- `health_check()`: System health monitoring

**API Endpoints**:
```python
GET  /                    # API information
GET  /api/health         # Health check
POST /api/upload         # File upload
POST /api/predict        # Disease prediction
GET  /api/diseases       # Available diseases
GET  /api/parameters     # CBC parameters info
```

#### 2. **file_processor.py** - Data Extraction Engine
**Purpose**: Extracts CBC parameters from various file formats

**Key Classes & Methods**:
```python
class FileProcessor:
    def process_file()           # Main processing entry point
    def _extract_from_pdf()      # PDF text extraction
    def _extract_from_image()    # OCR image processing
    def _extract_from_csv()      # CSV/Excel parsing
    def _parse_text()            # Text pattern matching
    def _fuzzy_match()           # Smart parameter matching
    def _validate_range()        # Data validation
```

**Parameter Recognition System**:
- **300+ keyword variations** for each CBC parameter
- **Fuzzy matching** algorithm for similar names
- **Range validation** for medical accuracy
- **Cross-validation** for data consistency

### Frontend Components

#### 1. **DiagnosisForm.jsx** - Main Interface
**Purpose**: User interface for data input and file upload

**Key Features**:
- **File Upload**: Drag-and-drop file processing
- **Auto-fill**: Populates form with extracted data
- **Manual Input**: Allows manual parameter entry
- **Validation**: Real-time input validation
- **Clear Function**: Resets all form data

#### 2. **ResultsDisplay.jsx** - Results Visualization
**Purpose**: Displays AI predictions and analysis results

**Key Features**:
- **Primary Diagnosis**: Main prediction with confidence
- **Top Predictions**: Ranked list with probabilities
- **Data Quality**: Shows completeness and missing parameters
- **Visual Charts**: Pie chart for probability distribution
- **Warnings**: Alerts for data quality issues

---

## 🤖 Machine Learning Pipeline

### Model Architecture
```
Input: 22 CBC Parameters
         │
         ▼
┌─────────────────┐
│ Data Preprocessing │
│ • Normalization    │
│ • Missing Value    │
│   Handling         │
└─────────────────┘
         │
         ▼
┌─────────────────┐
│ ML Model        │
│ (Scikit-learn)  │
│ • Classification │
│ • Probability   │
│   Estimation    │
└─────────────────┘
         │
         ▼
┌─────────────────┐
│ Label Encoder   │
│ • Disease Name  │
│   Mapping       │
└─────────────────┘
         │
         ▼
Output: Disease Predictions
```

### CBC Parameters (22 Total)

#### Blood Cell Counts
- **WBC** (White Blood Cells): Infection indicator
- **RBC** (Red Blood Cells): Oxygen transport
- **PLT** (Platelets): Blood clotting

#### Differential Count (Percentages)
- **LY%** (Lymphocytes): Immune response
- **MO%** (Monocytes): Infection fighting
- **NE%** (Neutrophils): Bacterial infections
- **EO%** (Eosinophils): Allergic reactions
- **BA%** (Basophils): Inflammatory response

#### Absolute Counts
- **LY#, MO#, NE#, EO#, BA#**: Absolute cell counts

#### Red Blood Cell Indices
- **HGB** (Hemoglobin): Oxygen carrying capacity
- **HCT** (Hematocrit): Blood volume percentage
- **MCV** (Mean Corpuscular Volume): Cell size
- **MCH** (Mean Corpuscular Hemoglobin): Cell hemoglobin
- **MCHC** (Mean Corpuscular Hemoglobin Concentration): Hemoglobin concentration
- **RDW** (Red Cell Distribution Width): Cell size variation

#### Platelet Indices
- **MPV** (Mean Platelet Volume): Platelet size

#### Patient Information
- **Age**: Patient age in years
- **Gender**: 1 for Male, 0 for Female

---

## 🔧 File Processing System

### Supported File Types

#### 1. **PDF Files** (.pdf)
**Technology**: PyPDF2
**Process**:
1. Extract text from all pages
2. Parse medical report format
3. Identify CBC parameters using regex patterns
4. Validate extracted values

#### 2. **Image Files** (.jpg, .png, .bmp, .tiff)
**Technology**: Tesseract OCR + PIL
**Process**:
1. Load image using PIL
2. Apply OCR to extract text
3. Parse extracted text for CBC parameters
4. Handle OCR errors and noise

#### 3. **Spreadsheet Files** (.csv, .xlsx, .xls)
**Technology**: Pandas + OpenPyXL
**Process**:
1. Load spreadsheet data
2. Identify parameter columns by name matching
3. Extract values from appropriate rows
4. Handle multiple data formats

### Parameter Extraction Algorithm

```python
# Example of parameter matching
parameter_variations = {
    'WBC': [
        'wbc', 'w.b.c', 'white blood cell', 'white blood cells',
        'leucocyte', 'leukocyte', 'total wbc', 'twbc'
    ],
    'HGB': [
        'hgb', 'hb', 'hemoglobin', 'haemoglobin',
        'hemoglobin level', 'hemo'
    ]
}

# Fuzzy matching for variations
def fuzzy_match(keyword, text):
    # Remove special characters
    # Calculate similarity score
    # Return match if above threshold
```

---

## 🚀 Getting Started

### Prerequisites
- **Python 3.7+**: Backend runtime
- **Node.js 14+**: Frontend build system
- **Tesseract OCR**: Image text extraction (optional)

### Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/checkwise.git
   cd checkwise
   ```

2. **Run the application**:
   ```bash
   start-app.bat
   ```
   This script will:
   - Check system requirements
   - Install Python dependencies
   - Install Node.js dependencies
   - Start both backend and frontend servers

3. **Access the application**:
   - **Frontend**: http://localhost:5173
   - **Backend API**: http://localhost:5000

### Manual Setup (Alternative)

#### Backend Setup
```bash
cd backend
pip install -r requirements.txt
python api.py
```

#### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

---

## 📊 Usage Guide

### Method 1: File Upload
1. **Upload File**: Click "Choose File" and select your CBC report
2. **Auto-extraction**: System extracts parameters automatically
3. **Review Data**: Check extracted values for accuracy
4. **Fill Missing**: Manually enter any missing parameters
5. **Analyze**: Click "Diagnose" for AI predictions

### Method 2: Manual Entry
1. **Clear Form**: Click "Clear Form" to start fresh
2. **Enter Values**: Input CBC parameters manually
3. **Validate**: System validates ranges automatically
4. **Analyze**: Click "Diagnose" for predictions

### Understanding Results

#### Primary Diagnosis
- **Disease Name**: Most likely condition
- **Confidence Level**: Very High, High, Moderate, Low, Very Low

#### Top Predictions
- **Ranked List**: Top 5 most probable diseases
- **Probability Scores**: Percentage likelihood
- **Visual Chart**: Pie chart representation

#### Data Quality Indicators
- **Completeness**: Percentage of provided parameters
- **Missing Parameters**: List of unavailable data
- **Warnings**: Data validation alerts

---

## 🔒 Data Security & Privacy

- **No Data Storage**: Files and data are processed in memory only
- **Local Processing**: All analysis happens on your server
- **No External APIs**: No data sent to third-party services
- **Session-based**: Data cleared after each session

---

## 🛠️ Development & Customization

### Adding New File Formats
1. Extend `FileProcessor` class in `file_processor.py`
2. Add new extraction method
3. Update file type validation in API

### Modifying Parameter Recognition
1. Update `cbc_params` dictionary in `FileProcessor`
2. Add new keyword variations
3. Adjust fuzzy matching thresholds

### Customizing UI
1. Modify React components in `frontend/src/components/`
2. Update styles in CSS files
3. Add new visualization components

---

## 🐛 Troubleshooting

### Common Issues

#### "Models not found" Error
- Ensure `*.joblib` files are in the backend directory
- Check file permissions

#### "Tesseract not found" Error
- Install Tesseract OCR for image processing
- Add Tesseract to system PATH

#### File Upload Fails
- Check file size (max 10MB)
- Verify file format is supported
- Ensure file is not corrupted

#### Poor Parameter Extraction
- Try different file formats (PDF usually works best)
- Ensure text is clear and readable
- Check for proper CBC report format

---

## 📈 Performance & Scalability

### Current Limitations
- **File Size**: 10MB maximum
- **Concurrent Users**: Single-threaded Flask server
- **Processing Time**: 1-5 seconds per file

### Scaling Recommendations
- Use **Gunicorn** for production deployment
- Implement **Redis** for caching
- Add **database** for result storage
- Use **Docker** for containerization

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

---

## ⚠️ Medical Disclaimer

**IMPORTANT**: CheckWise is for educational and research purposes only. It is not intended for clinical diagnosis or medical decision-making. Always consult with qualified healthcare professionals for medical advice and diagnosis.

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🙏 Acknowledgments

- **Scikit-learn**: Machine learning framework
- **React**: Frontend framework
- **Flask**: Backend framework
- **Tesseract**: OCR engine
- **Medical Community**: For CBC reference ranges and insights
