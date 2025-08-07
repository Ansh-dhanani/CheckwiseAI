# CheckWise

AI-powered medical diagnosis system using CBC (Complete Blood Count) test results.

## Features

- **File Upload**: Upload PDF, images, or CSV files containing CBC data
- **Auto-extraction**: Automatically extracts CBC parameters from uploaded files
- **AI Diagnosis**: Predicts potential diseases based on CBC values
- **Interactive UI**: Clean React interface with real-time results

## Project Structure

```
CheckWise/
├── backend/                 # Flask API server
│   ├── api.py              # Main API endpoints
│   ├── file_processor.py   # File processing logic
│   ├── requirements.txt    # Python dependencies
│   ├── *.joblib           # ML models
├── frontend/               # React application
│   ├── src/
│   │   ├── components/    # React components
│   │   └── ...
│   ├── package.json       # Node.js dependencies
│   └── ...
└── start-app.bat          # Application launcher
```

## Quick Start

1. **Run the application**:
   ```bash
   start-app.bat
   ```

2. **Access the application**:
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:5000

## Supported File Types

- **PDF**: Medical reports with CBC data
- **Images**: JPG, PNG, BMP, TIFF (requires Tesseract OCR)
- **Spreadsheets**: CSV, XLSX, XLS files

## Requirements

- Python 3.7+
- Node.js 14+
- Tesseract OCR (for image processing)

## Usage

1. Upload a file containing CBC test results
2. Review auto-extracted parameters
3. Fill in any missing values manually
4. Click "Diagnose" to get AI predictions
5. View results with probability scores

## CBC Parameters

The system recognizes 22 CBC parameters:
- WBC, RBC, HGB, HCT, PLT
- Lymphocyte %, Monocyte %, Neutrophil %, Eosinophil %, Basophil %
- Lymphocyte #, Monocyte #, Neutrophil #, Eosinophil #, Basophil #
- MCV, MCHC, MCH, RDW, MPV
- Age, Gender