import re
import pandas as pd
import PyPDF2
from PIL import Image
import pytesseract
import io
import os
import json
import logging
from difflib import SequenceMatcher
from typing import Dict, List, Any, Optional, Union
import numpy as np
from datetime import datetime
import openpyxl
from openpyxl.utils import get_column_letter
import pdfplumber
import camelot

# Configure logging
logger = logging.getLogger(__name__)

# Set tesseract path for Windows and common Linux installations
def setup_tesseract():
    """Setup tesseract path for different operating systems"""
    if os.name == 'nt':  # Windows
        tesseract_paths = [
            r'C:\Program Files\Tesseract-OCR\tesseract.exe',
            r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe',
            r'C:\Users\{}\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'.format(os.getlogin()),
            r'D:\Program Files\Tesseract-OCR\tesseract.exe'
        ]
        for path in tesseract_paths:
            try:
                if os.path.exists(path):
                    pytesseract.pytesseract.tesseract_cmd = path
                    logger.info(f"Tesseract found at: {path}")
                    return True
            except:
                continue
    else:  # Linux/Unix
        tesseract_paths = ['/usr/bin/tesseract', '/usr/local/bin/tesseract', '/opt/homebrew/bin/tesseract']
        for path in tesseract_paths:
            if os.path.exists(path):
                pytesseract.pytesseract.tesseract_cmd = path
                logger.info(f"Tesseract found at: {path}")
                return True
    
    logger.warning("Tesseract not found in common locations")
    return False

# Initialize tesseract
setup_tesseract()

class FileProcessor:
    def __init__(self):
        """Initialize the file processor with comprehensive parameter mapping"""
        
        # Enhanced CBC parameter mapping with all possible variations
        self.cbc_params = {
            'WBC': [
                'wbc', 'w.b.c', 'w b c', 'white blood cell', 'white blood cells', 'leucocyte', 
                'leukocyte', 'leukocytes', 'total wbc', 'twbc', 'tc', 'total count', 
                'total leukocyte count', 'total leucocyte count', 'white cell count',
                'wcc', 'leucocyte count', 'leukocyte count', 'total white cell count'
            ],
            'LY%': [
                'ly%', 'lymph%', 'lymphocyte%', 'lymphocytes%', 'l%', 'lym%', 'lymph percent', 
                'lymphocyte percent', 'lymphocytes', 'lymph percentage', 'lymphocyte percentage',
                'ly %', 'lym %', 'lymph %', 'lymphocyte %', 'lymphocytes %'
            ],
            'MO%': [
                'mo%', 'mono%', 'monocyte%', 'monocytes%', 'm%', 'mon%', 'monocyte percent', 
                'monocytes', 'monocyte percentage', 'mono percent', 'mono percentage',
                'mo %', 'mono %', 'monocyte %', 'monocytes %'
            ],
            'NE%': [
                'ne%', 'neut%', 'neutrophil%', 'neutrophils%', 'n%', 'neu%', 'neutrophil percent', 
                'pmn%', 'segmented neutrophils', 'neutrophils', 'neutrophil percentage',
                'neut percent', 'seg%', 'segs%', 'polymorphs%', 'polys%',
                'ne %', 'neut %', 'neutrophil %', 'neutrophils %'
            ],
            'EO%': [
                'eo%', 'eosinophil%', 'eosinophils%', 'e%', 'eos%', 'eosinophil percent', 
                'eosinophils', 'eosinophil percentage', 'eos percent',
                'eo %', 'eos %', 'eosinophil %', 'eosinophils %'
            ],
            'BA%': [
                'ba%', 'baso%', 'basophil%', 'basophils%', 'b%', 'bas%', 'basophil percent', 
                'basophils', 'basophil percentage', 'baso percent',
                'ba %', 'baso %', 'basophil %', 'basophils %'
            ],
            'LY#': [
                'ly#', 'lymph#', 'lymphocyte#', 'lymphocytes#', 'l#', 'lym#', 'lymph count', 
                'lymphocyte count', 'lymph abs', 'lymph absolute', 'absolute lymphocyte count',
                'lymphocyte absolute', 'ly #', 'lymph #', 'lymphocyte #'
            ],
            'MO#': [
                'mo#', 'mono#', 'monocyte#', 'monocytes#', 'm#', 'mon#', 'monocyte count', 
                'mono count', 'mono abs', 'absolute monocyte count', 'monocyte absolute',
                'mo #', 'mono #', 'monocyte #'
            ],
            'NE#': [
                'ne#', 'neut#', 'neutrophil#', 'neutrophils#', 'n#', 'neu#', 'neutrophil count', 
                'neut count', 'pmn#', 'neutrophil abs', 'absolute neutrophil count',
                'neutrophil absolute', 'seg#', 'segs#', 'ne #', 'neut #', 'neutrophil #'
            ],
            'EO#': [
                'eo#', 'eosinophil#', 'eosinophils#', 'e#', 'eos#', 'eosinophil count', 
                'eos count', 'eosinophil abs', 'absolute eosinophil count',
                'eosinophil absolute', 'eo #', 'eos #', 'eosinophil #'
            ],
            'BA#': [
                'ba#', 'baso#', 'basophil#', 'basophils#', 'b#', 'bas#', 'basophil count', 
                'baso count', 'basophil abs', 'absolute basophil count',
                'basophil absolute', 'ba #', 'baso #', 'basophil #'
            ],
            'RBC': [
                'rbc', 'r.b.c', 'r b c', 'red blood cell', 'red blood cells', 'erythrocyte', 
                'erythrocytes', 'total rbc', 'trbc', 'red cell count', 'rbc count',
                'red blood cell count', 'erythrocyte count', 'red cells'
            ],
            'HGB': [
                'hgb', 'hb', 'hemoglobin', 'haemoglobin', 'hemo', 'haemo', 'hemoglobin level',
                'haemoglobin level', 'hgb level', 'hb level', 'hemoglobin concentration'
            ],
            'HCT': [
                'hct', 'hematocrit', 'haematocrit', 'pcv', 'packed cell volume', 'hematocrit level',
                'haematocrit level', 'hct level', 'pcv level', 'packed cell vol'
            ],
            'MCV': [
                'mcv', 'mean corpuscular volume', 'mean cell volume', 'average cell volume',
                'mean corpuscular vol', 'mean cell vol', 'avg cell volume'
            ],
            'MCHC': [
                'mchc', 'mean corpuscular hemoglobin concentration', 'mean cell hemoglobin concentration',
                'mean corpuscular haemoglobin concentration', 'mean cell haemoglobin concentration',
                'mean corpuscular hgb conc', 'mean cell hgb conc'
            ],
            'MCH': [
                'mch', 'mean corpuscular hemoglobin', 'mean cell hemoglobin', 'average cell hemoglobin',
                'mean corpuscular haemoglobin', 'mean cell haemoglobin', 'mean corpuscular hgb',
                'mean cell hgb', 'avg cell hemoglobin'
            ],
            'RDW': [
                'rdw', 'red cell distribution width', 'red blood cell distribution width', 
                'rdw-cv', 'rdw-sd', 'rdw cv', 'rdw sd', 'red cell dist width',
                'rbc distribution width', 'red cell distribution'
            ],
            'PLT': [
                'plt', 'platelet', 'platelets', 'platelet count', 'thrombocyte', 'thrombocytes', 
                'pc', 'platelet cnt', 'plt count', 'thrombocyte count', 'platelet number',
                'total platelet count', 'total platelets'
            ],
            'MPV': [
                'mpv', 'mean platelet volume', 'average platelet volume', 'mean thrombocyte volume',
                'avg platelet volume', 'mean plt volume', 'mean platelet vol'
            ],
            'Age': [
                'age', 'years', 'yrs', 'yr', 'years old', 'age in years', 'patient age',
                'age(years)', 'age (years)', 'age(yrs)', 'age (yrs)'
            ],
            'Gender': [
                'gender', 'sex', 'male', 'female', 'm', 'f', 'patient sex', 'patient gender',
                'gender/sex', 'sex/gender', 'pt sex', 'pt gender'
            ]
        }
        
        # Medical reference ranges for validation
        self.reference_ranges = {
            'WBC': {'min': 1.0, 'max': 50.0, 'normal': (4.0, 11.0), 'unit': '10³/μL'},
            'RBC': {'min': 2.0, 'max': 8.0, 'normal': (4.2, 5.4), 'unit': '10⁶/μL'},
            'HGB': {'min': 5.0, 'max': 20.0, 'normal': (12.0, 16.0), 'unit': 'g/dL'},
            'HCT': {'min': 15.0, 'max': 60.0, 'normal': (36.0, 48.0), 'unit': '%'},
            'MCV': {'min': 60.0, 'max': 120.0, 'normal': (80.0, 100.0), 'unit': 'fL'},
            'MCH': {'min': 20.0, 'max': 40.0, 'normal': (27.0, 33.0), 'unit': 'pg'},
            'MCHC': {'min': 25.0, 'max': 40.0, 'normal': (32.0, 36.0), 'unit': 'g/dL'},
            'RDW': {'min': 10.0, 'max': 25.0, 'normal': (11.5, 14.5), 'unit': '%'},
            'PLT': {'min': 50.0, 'max': 1500.0, 'normal': (150.0, 450.0), 'unit': '10³/μL'},
            'MPV': {'min': 5.0, 'max': 20.0, 'normal': (7.5, 11.5), 'unit': 'fL'},
            'LY%': {'min': 0.0, 'max': 100.0, 'normal': (20.0, 40.0), 'unit': '%'},
            'MO%': {'min': 0.0, 'max': 100.0, 'normal': (2.0, 8.0), 'unit': '%'},
            'NE%': {'min': 0.0, 'max': 100.0, 'normal': (50.0, 70.0), 'unit': '%'},
            'EO%': {'min': 0.0, 'max': 100.0, 'normal': (1.0, 4.0), 'unit': '%'},
            'BA%': {'min': 0.0, 'max': 100.0, 'normal': (0.0, 1.0), 'unit': '%'},
            'LY#': {'min': 0.0, 'max': 15.0, 'normal': (1.2, 3.4), 'unit': '10³/μL'},
            'MO#': {'min': 0.0, 'max': 5.0, 'normal': (0.1, 0.9), 'unit': '10³/μL'},
            'NE#': {'min': 0.0, 'max': 25.0, 'normal': (1.8, 7.7), 'unit': '10³/μL'},
            'EO#': {'min': 0.0, 'max': 5.0, 'normal': (0.05, 0.5), 'unit': '10³/μL'},
            'BA#': {'min': 0.0, 'max': 2.0, 'normal': (0.0, 0.2), 'unit': '10³/μL'},
            'Age': {'min': 0.0, 'max': 120.0, 'normal': (0.0, 120.0), 'unit': 'years'},
            'Gender': {'min': 0, 'max': 1, 'normal': (0, 1), 'unit': '0=F, 1=M'}
        }
        
        # Common lab report patterns and structures
        self.report_patterns = {
            'table_headers': [
                'test', 'result', 'reference range', 'units', 'flag',
                'parameter', 'value', 'normal range', 'unit', 'status',
                'investigation', 'findings', 'range', 'remarks'
            ],
            'section_headers': [
                'complete blood count', 'cbc', 'hematology', 'blood count',
                'full blood count', 'fbc', 'hemogram', 'blood picture'
            ]
        }

    def process_file(self, file_content: bytes, file_type: str, patient_id: Optional[int] = None) -> Union[Dict, List]:
        """
        Main method to process different file types with comprehensive error handling
        """
        try:
            logger.info(f"Processing file type: {file_type}")
            
            if patient_id is not None:
                return self.extract_specific_patient(file_content, file_type, patient_id)
            
            if file_type.lower() == 'pdf':
                return self.extract_from_pdf(file_content)
            elif file_type.lower() in ['jpg', 'jpeg', 'png', 'tiff', 'bmp', 'gif']:
                return self.extract_from_image(file_content)
            elif file_type.lower() in ['csv']:
                return self.extract_from_csv(file_content)
            elif file_type.lower() in ['xlsx', 'xls']:
                return self.extract_from_excel(file_content)
            elif file_type.lower() in ['txt']:
                return self.extract_from_text(file_content)
            else:
                return {'error': f'Unsupported file type: {file_type}'}
                
        except Exception as e:
            logger.error(f"File processing failed: {str(e)}")
            return {'error': f'File processing failed: {str(e)}'}

    def extract_from_pdf(self, file_content: bytes) -> Dict:
        """
        Enhanced PDF extraction using multiple methods for better accuracy
        """
        try:
            # Method 1: Try pdfplumber for better table extraction
            try:
                    with pdfplumber.open(io.BytesIO(file_content)) as pdf:
                        text = ""
                        tables = []
                        
                        for page in pdf.pages:
                            # Extract text
                            page_text = page.extract_text()
                            if page_text:
                                text += page_text + "\n"
                            
                            # Extract tables
                            page_tables = page.extract_tables()
                            if page_tables:
                                tables.extend(page_tables)
                        
                        # Try table-based extraction first
                        if tables:
                            table_result = self._extract_from_tables(tables)
                            if table_result and not table_result.get('error'):
                                logger.info("Successfully extracted data from PDF tables")
                                return table_result
                        
                        # Fallback to text extraction
                        if text:
                            text_result = self._parse_text_for_cbc(text)
                            if text_result and not text_result.get('error'):
                                logger.info("Successfully extracted data from PDF text")
                                return text_result
            except Exception as e:
                logger.warning(f"pdfplumber extraction failed: {e}")
            
            # Method 2: Try camelot for table extraction
            try:
                    tables = camelot.read_pdf(io.BytesIO(file_content), pages='all')
                    if tables:
                        camelot_tables = [table.df.values.tolist() for table in tables]
                        table_result = self._extract_from_tables(camelot_tables)
                        if table_result and not table_result.get('error'):
                            logger.info("Successfully extracted data from PDF using camelot")
                            return table_result
            except Exception as e:
                logger.warning(f"Camelot extraction failed: {e}")
            
            # Method 3: Fallback to PyPDF2
            try:
                pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_content))
                text = ""
                for page in pdf_reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
                
                if text:
                    result = self._parse_text_for_cbc(text)
                    logger.info("Extracted data using PyPDF2")
                    return result
            except Exception as e:
                logger.error(f"PyPDF2 extraction failed: {e}")
            
            return {'error': 'Could not extract readable content from PDF'}
            
        except Exception as e:
            return {'error': f'PDF processing error: {str(e)}'}

    def extract_from_image(self, file_content: bytes) -> Dict:
        """
        Enhanced image extraction with preprocessing for better OCR accuracy
        """
        try:
            image = Image.open(io.BytesIO(file_content))
            
            # Preprocess image for better OCR
            processed_images = self._preprocess_image(image)
            
            best_result = None
            best_score = 0
            
            for processed_image in processed_images:
                try:
                    # Try different OCR configurations
                    ocr_configs = [
                        '--psm 6',  # Single uniform block
                        '--psm 4',  # Single column of text
                        '--psm 3',  # Fully automatic page segmentation
                        '--psm 11', # Sparse text
                        '--psm 12'  # Single text line
                    ]
                    
                    for config in ocr_configs:
                        try:
                            text = pytesseract.image_to_string(processed_image, config=config)
                            if text and len(text.strip()) > 50:  # Minimum text length
                                result = self._parse_text_for_cbc(text)
                                if result and not result.get('error'):
                                    score = len([k for k in result.keys() if not k.startswith('_')])
                                    if score > best_score:
                                        best_result = result
                                        best_score = score
                                        logger.info(f"OCR config '{config}' found {score} parameters")
                        except Exception as e:
                            continue
                            
                except pytesseract.TesseractNotFoundError:
                    return {'error': 'Tesseract OCR not installed. Please install Tesseract to process images.'}
                except Exception as e:
                    continue
            
            if best_result:
                return best_result
            else:
                return {'error': 'Could not extract readable CBC data from image'}
                
        except Exception as e:
            return {'error': f'Image processing error: {str(e)}'}

    def _preprocess_image(self, image: Image.Image) -> List[Image.Image]:
        """
        Preprocess image for better OCR results
        """
        processed_images = []
        
        try:
            # Convert to RGB if needed
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Original image
            processed_images.append(image)
            
            # Convert to grayscale
            gray_image = image.convert('L')
            processed_images.append(gray_image)
            
            # Enhance contrast
            from PIL import ImageEnhance
            enhancer = ImageEnhance.Contrast(gray_image)
            contrast_image = enhancer.enhance(2.0)
            processed_images.append(contrast_image)
            
            # Resize if too small
            width, height = image.size
            if width < 1000 or height < 1000:
                scale_factor = max(1000 / width, 1000 / height)
                new_size = (int(width * scale_factor), int(height * scale_factor))
                resized_image = image.resize(new_size, Image.Resampling.LANCZOS)
                processed_images.append(resized_image)
            
        except Exception as e:
            logger.warning(f"Image preprocessing failed: {e}")
        
        return processed_images

    def extract_from_csv(self, file_content: bytes) -> Union[Dict, List]:
        try:
            encodings = ['utf-8', 'utf-8-sig', 'latin-1', 'cp1252']
            for encoding in encodings:
                try:
                    content_str = file_content.decode(encoding)
                    df = pd.read_csv(io.StringIO(content_str))
                    return self._process_dataframe(df)
                except Exception:
                    continue
            return {'error': 'Could not parse CSV file'}
        except Exception as e:
            return {'error': f'CSV error: {str(e)}'}

    def extract_from_excel(self, file_content: bytes) -> Union[Dict, List]:
        """
        Enhanced Excel extraction with support for multiple sheets
        """
        try:
            # Try different Excel engines
            engines = ['openpyxl', 'xlrd']
            df = None
            
            for engine in engines:
                try:
                    excel_file = pd.ExcelFile(io.BytesIO(file_content), engine=engine)
                    
                    # Try to find the best sheet
                    best_sheet = None
                    best_score = 0
                    
                    for sheet_name in excel_file.sheet_names:
                        try:
                            sheet_df = pd.read_excel(excel_file, sheet_name=sheet_name)
                            if len(sheet_df) > 0:
                                # Score based on CBC-related content
                                score = self._score_dataframe_for_cbc(sheet_df)
                                if score > best_score:
                                    best_sheet = sheet_name
                                    best_score = score
                                    df = sheet_df
                        except Exception:
                            continue
                    
                    if df is not None:
                        logger.info(f"Successfully parsed Excel with engine: {engine}, sheet: {best_sheet}")
                        break
                        
                except Exception:
                    continue
            
            if df is None:
                return {'error': 'Could not parse Excel file'}
            
            return self._process_dataframe(df)
            
        except Exception as e:
            return {'error': f'Excel processing error: {str(e)}'}

    def extract_from_text(self, file_content: bytes) -> Dict:
        try:
            encodings = ['utf-8', 'utf-8-sig', 'latin-1', 'cp1252']
            for encoding in encodings:
                try:
                    text = file_content.decode(encoding)
                    return self._parse_text_for_cbc(text)
                except Exception:
                    continue
            return {'error': 'Could not decode text file'}
        except Exception as e:
            return {'error': f'Text error: {str(e)}'}

    def _process_dataframe(self, df: pd.DataFrame) -> Union[Dict, List]:
        """
        Process pandas DataFrame for CBC data extraction
        """
        try:
            # Check for multiple patients
            if len(df) > 1:
                # Try to detect if this is multiple patients or multiple test results for same patient
                potential_patients = self._detect_multiple_patients(df)
                if potential_patients:
                    return {
                        'multiple_patients': True,
                        'patients': potential_patients,
                        'total_records': len(df),
                        'message': f'Found {len(df)} records. Please select which record to diagnose.'
                    }
            
            # Extract single patient data
            return self._extract_single_patient_dataframe(df, 0)
            
        except Exception as e:
            return {'error': f'DataFrame processing error: {str(e)}'}

    def _detect_multiple_patients(self, df: pd.DataFrame) -> Optional[List[Dict]]:
        """
        Detect if DataFrame contains multiple patients
        """
        try:
            patients = []
            
            # Look for patient identifiers
            id_columns = [col for col in df.columns if any(term in col.lower() for term in 
                         ['patient', 'id', 'name', 'mrn', 'accession', 'sample'])]
            
            for i in range(len(df)):
                patient_info = {'id': i}
                
                # Try to extract patient name or ID
                if id_columns:
                    for col in id_columns:
                        value = df.iloc[i][col]
                        if pd.notna(value) and str(value).strip():
                            patient_info['name'] = f"Patient {str(value)} (Row {i+1})"
                            break
                    else:
                        patient_info['name'] = f"Patient {i+1} (Row {i+1})"
                else:
                    patient_info['name'] = f"Patient {i+1} (Row {i+1})"
                
                patients.append(patient_info)
            
            return patients if len(patients) > 1 else None
            
        except Exception:
            return None

    def _parse_text_for_cbc(self, text: str) -> Dict:
        extracted_data = {}
        text_lower = text.lower()
        
        # Simple patterns for parameter extraction
        patterns = [
            r'([a-zA-Z][a-zA-Z0-9\s%#]+?)\s*[:\-=]\s*([0-9]+\.?[0-9]*)',
            r'([a-zA-Z][a-zA-Z0-9\s%#]+)\s+([0-9]+\.?[0-9]*)'
        ]
        
        # Extract parameter-value pairs
        lines = text.split('\n')
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            for param, keywords in self.cbc_params.items():
                if param in extracted_data:
                    continue
                    
                for keyword in keywords[:5]:
                    if keyword in line.lower():
                        # Look for number after the keyword
                        match = re.search(rf'{re.escape(keyword)}[:\s=]*([0-9]+\.?[0-9]*)', line, re.IGNORECASE)
                        if match:
                            value = self._process_extracted_value(param, match.group(1), line)
                            if value is not None:
                                extracted_data[param] = value
                                break
                if param in extracted_data:
                    break
        
        # Add basic gender/age extraction
        if 'Gender' not in extracted_data:
            if re.search(r'\b(male|m)\b', text_lower):
                extracted_data['Gender'] = 1
            elif re.search(r'\b(female|f)\b', text_lower):
                extracted_data['Gender'] = 0
        
        if 'Age' not in extracted_data:
            age_match = re.search(r'age[:\s]*(\d+)', text_lower)
            if age_match:
                age = int(age_match.group(1))
                if 0 <= age <= 120:
                    extracted_data['Age'] = age
        
        return extracted_data if extracted_data else {'error': 'No CBC parameters found'}

    def _extract_cbc_section(self, text: str) -> Optional[str]:
        """
        Extract the CBC-specific section from text
        """
        try:
            text_lower = text.lower()
            
            # Look for CBC section markers
            section_starts = []
            section_ends = []
            
            for header in self.report_patterns['section_headers']:
                start_pos = text_lower.find(header)
                if start_pos != -1:
                    section_starts.append(start_pos)
            
            # Look for section end markers
            end_markers = ['chemistry', 'biochemistry', 'lipid profile', 'liver function', 
                          'kidney function', 'thyroid', 'conclusion', 'impression']
            
            for marker in end_markers:
                end_pos = text_lower.find(marker)
                if end_pos != -1:
                    section_ends.append(end_pos)
            
            if section_starts:
                start_pos = min(section_starts)
                end_pos = min([pos for pos in section_ends if pos > start_pos]) if section_ends else len(text)
                return text[start_pos:end_pos]
            
        except Exception:
            pass
        
        return None

    def _extract_by_context(self, param: str, lines: List[str], current_idx: int) -> Optional[float]:
        """
        Extract parameter value using context from surrounding lines
        """
        try:
            # Look in nearby lines
            search_range = range(max(0, current_idx - 2), min(len(lines), current_idx + 3))
            
            for idx in search_range:
                line = lines[idx]
                for keyword in self.cbc_params[param]:
                    if keyword in line:
                        # Look for numbers in this line
                        numbers = re.findall(r'\b\d+\.?\d*\b', line)
                        for num in numbers:
                            try:
                                value = float(num)
                                if self._validate_range(param, value):
                                    return value
                            except ValueError:
                                continue
            
        except Exception:
            pass
        
        return None

    def _alternative_text_extraction(self, text: str) -> Dict:
        """
        Alternative extraction method using different parsing strategies
        """
        extracted_data = {}
        
        try:
            # Method 1: Extract all number-text pairs
            pairs = re.findall(r'([a-zA-Z][a-zA-Z0-9\s%#\(\)]+?)\s*[:\-=]?\s*(\d+\.?\d*)', text, re.IGNORECASE)
            
            for param_text, value_text in pairs:
                param_text = param_text.strip().lower()
                
                for param, keywords in self.cbc_params.items():
                    if param in extracted_data:
                        continue
                    
                    for keyword in keywords:
                        if self._fuzzy_match(keyword, param_text, threshold=0.6):
                            try:
                                value = float(value_text)
                                if self._validate_range(param, value):
                                    extracted_data[param] = value
                                    break
                            except ValueError:
                                continue
                    
                    if param in extracted_data:
                        break
            
            # Method 2: Look for specific patterns by parameter type
            if 'Gender' not in extracted_data:
                gender_match = re.search(r'\b(male|female|m|f)\b', text, re.IGNORECASE)
                if gender_match:
                    extracted_data['Gender'] = 1 if gender_match.group().lower() in ['male', 'm'] else 0
            
            if 'Age' not in extracted_data:
                age_patterns = [
                    r'age[:\s]*(\d+)',
                    r'(\d+)\s*years?\s*old',
                    r'(\d+)\s*yrs?'
                ]
                for pattern in age_patterns:
                    age_match = re.search(pattern, text, re.IGNORECASE)
                    if age_match:
                        try:
                            age = int(age_match.group(1))
                            if 0 <= age <= 120:
                                extracted_data['Age'] = age
                                break
                        except ValueError:
                            continue
        
        except Exception:
            pass
        
        return extracted_data

    def _score_dataframe_for_cbc(self, df: pd.DataFrame) -> int:
        """
        Score DataFrame based on CBC-related content
        """
        score = 0
        df_lower = df.astype(str).apply(lambda x: x.str.lower())
        
        for param, keywords in self.cbc_params.items():
            for keyword in keywords[:3]:  # Check first 3 keywords for performance
                if df_lower.isin([keyword]).any().any():
                    score += 1
                    break
        
        return score

    def _extract_from_tables(self, tables: List[List]) -> Optional[Dict]:
        """
        Extract CBC data from table structures
        """
        extracted_data = {}
        
        try:
            for table in tables:
                if not table or len(table) < 2:
                    continue
                
                # Convert table to DataFrame for easier processing
                df = pd.DataFrame(table[1:], columns=table[0] if table[0] else None)
                
                # Try to identify parameter and value columns
                param_col_idx = None
                value_col_idx = None
                
                for i, col in enumerate(df.columns):
                    if col and isinstance(col, str):
                        col_lower = col.lower()
                        if any(term in col_lower for term in ['test', 'parameter', 'investigation']):
                            param_col_idx = i
                        elif any(term in col_lower for term in ['result', 'value', 'finding']):
                            value_col_idx = i
                
                # If columns not identified, try first two columns
                if param_col_idx is None:
                    param_col_idx = 0
                if value_col_idx is None:
                    value_col_idx = 1 if len(df.columns) > 1 else 0
                
                # Extract data
                for _, row in df.iterrows():
                    try:
                        param_text = str(row.iloc[param_col_idx]).strip().lower()
                        value_text = str(row.iloc[value_col_idx]).strip()
                        
                        if not param_text or not value_text or value_text.lower() in ['nan', 'none', '']:
                            continue
                        
                        # Match parameter
                        for param, keywords in self.cbc_params.items():
                            if param in extracted_data:
                                continue
                                
                            for keyword in keywords:
                                if self._fuzzy_match(keyword, param_text, threshold=0.7):
                                    # Extract numeric value
                                    value = self._extract_numeric_value(value_text)
                                    if value is not None:
                                        if param == 'Gender':
                                            value = self._parse_gender(value_text)
                                        
                                        if self._validate_range(param, value):
                                            extracted_data[param] = value
                                            break
                            
                            if param in extracted_data:
                                break
                                
                    except Exception:
                        continue
            
            if extracted_data:
                return self._cross_validate_data(extracted_data)
            
        except Exception as e:
            logger.error(f"Table extraction error: {e}")
        
        return None

    def _extract_single_patient_dataframe(self, df: pd.DataFrame, row_idx: int) -> Dict:
        """
        Extract single patient data from DataFrame row
        """
        extracted_data = {}
        
        try:
            row = df.iloc[row_idx]
            
            # Check all columns for CBC parameters
            for col_name in df.columns:
                col_name_lower = str(col_name).lower().strip()
                col_value = row[col_name]
                
                # Skip empty values
                if pd.isna(col_value) or str(col_value).strip() == '':
                    continue
                
                # Match column name to CBC parameters
                for param, keywords in self.cbc_params.items():
                    if param in extracted_data:
                        continue
                    
                    for keyword in keywords:
                        if (keyword in col_name_lower or 
                            col_name_lower in keyword or 
                            self._fuzzy_match(keyword, col_name_lower, threshold=0.7)):
                            
                            value = self._process_extracted_value(param, str(col_value), col_name)
                            if value is not None:
                                extracted_data[param] = value
                                break
                    
                    if param in extracted_data:
                        break
            
            return self._cross_validate_data(extracted_data)
            
        except Exception as e:
            logger.error(f"Single patient extraction error: {e}")
            return {'error': f'Failed to extract patient data: {str(e)}'}

    def extract_specific_patient(self, file_content: bytes, file_type: str, patient_id: int) -> Dict:
        """
        Extract specific patient data from multi-patient file
        """
        try:
            if file_type.lower() in ['csv']:
                df = pd.read_csv(io.StringIO(file_content.decode('utf-8')))
            elif file_type.lower() in ['xlsx', 'xls']:
                df = pd.read_excel(io.BytesIO(file_content))
            else:
                return {'error': 'Patient selection only supported for CSV and Excel files'}
            
            if patient_id >= len(df):
                return {'error': f'Patient ID {patient_id} not found. File has {len(df)} records.'}
            
            return self._extract_single_patient_dataframe(df, patient_id)
            
        except Exception as e:
            return {'error': f'Patient extraction error: {str(e)}'}

    def _process_extracted_value(self, param: str, value_str: str, context: str = "") -> Optional[float]:
        """
        Process and validate extracted parameter value
        """
        try:
            # Handle gender specially
            if param == 'Gender':
                return self._parse_gender(value_str)
            
            # Extract numeric value
            value = self._extract_numeric_value(value_str)
            if value is None:
                return None
            
            # Apply parameter-specific processing
            if param.endswith('%') and value > 1 and value <= 100:
                # Likely percentage format
                pass
            elif param.endswith('#') and value < 1 and value > 0:
                # Might need scaling
                if param in ['LY#', 'MO#', 'NE#', 'EO#', 'BA#']:
                    # These are typically in 10³/μL, so small values might need scaling
                    pass
            
            # Validate range
            if self._validate_range(param, value):
                return value
            
            # Try unit conversions if value is out of range
            converted_value = self._try_unit_conversion(param, value, context)
            if converted_value is not None and self._validate_range(param, converted_value):
                return converted_value
            
            # If still out of range but not too extreme, accept with warning
            if param in self.reference_ranges:
                range_info = self.reference_ranges[param]
                if range_info['min'] * 0.1 <= value <= range_info['max'] * 10:
                    logger.warning(f"{param}={value} outside normal range but accepted")
                    return value
            
            return None
            
        except Exception as e:
            logger.error(f"Value processing error for {param}={value_str}: {e}")
            return None

    def _parse_gender(self, value_str: str) -> Optional[int]:
        """
        Parse gender from various string formats
        """
        value_lower = str(value_str).lower().strip()
        
        if value_lower in ['male', 'm', '1', 'man', 'boy']:
            return 1
        elif value_lower in ['female', 'f', '0', 'woman', 'girl']:
            return 0
        
        # Try to extract from longer strings
        if 'male' in value_lower and 'female' not in value_lower:
            return 1
        elif 'female' in value_lower:
            return 0
        
        return None

    def _extract_numeric_value(self, value_str: str) -> Optional[float]:
        """
        Extract numeric value from string, handling various formats
        """
        try:
            value_str = str(value_str).strip()
            
            # Remove common non-numeric characters
            cleaned = re.sub(r'[^\d\.\-\+]', '', value_str)
            
            if not cleaned:
                return None
            
            # Handle negative values
            if cleaned.startswith('-'):
                return -float(cleaned[1:]) if cleaned[1:] else None
            
            # Handle positive values with explicit +
            if cleaned.startswith('+'):
                cleaned = cleaned[1:]
            
            if cleaned:
                return float(cleaned)
            
        except (ValueError, AttributeError):
            pass
        
        return None

    def _validate_range(self, param: str, value: float) -> bool:
        if param not in self.reference_ranges:
            return True
        range_info = self.reference_ranges[param]
        # Be more lenient with range validation
        return range_info['min'] * 0.5 <= value <= range_info['max'] * 2

    def _try_unit_conversion(self, param: str, value: float, context: str) -> Optional[float]:
        """
        Try to convert units if value seems to be in wrong units
        """
        try:
            context_lower = context.lower()
            
            # Common unit conversions
            if param in ['HGB'] and value > 200:
                # Might be in g/L instead of g/dL
                return value / 10
            
            elif param in ['HCT'] and value > 1 and value < 10:
                # Might be fraction instead of percentage
                return value * 100
            
            elif param.endswith('#') and value > 100:
                # Absolute counts might be in wrong units
                if 'thou' in context_lower or '10³' in context_lower or 'k/' in context_lower:
                    return value / 1000 if value > 1000 else value
            
            elif param.endswith('%') and value > 100:
                # Percentage might be given as decimal
                return value / 100 if value < 1000 else None
            
        except Exception:
            pass
        
        return None

    def _fuzzy_match(self, keyword: str, text: str, threshold: float = 0.8) -> bool:
        """
        Fuzzy string matching for parameter names
        """
        try:
            # Clean both strings
            keyword_clean = re.sub(r'[^\w\s]', '', keyword.lower()).strip()
            text_clean = re.sub(r'[^\w\s]', '', text.lower()).strip()
            
            if not keyword_clean or not text_clean:
                return False
            
            # Exact match
            if keyword_clean == text_clean:
                return True
            
            # Substring match
            if keyword_clean in text_clean or text_clean in keyword_clean:
                return True
            
            # Fuzzy match using SequenceMatcher
            ratio = SequenceMatcher(None, keyword_clean, text_clean).ratio()
            return ratio >= threshold
            
        except Exception:
            return False

    def _cross_validate_data(self, extracted_data: Dict) -> Dict:
        """
        Cross-validate extracted data for consistency and calculate missing values
        """
        try:
            validated_data = extracted_data.copy()
            
            # Validate differential count percentages sum to ~100%
            percentage_params = ['LY%', 'MO%', 'NE%', 'EO%', 'BA%']
            percentages = {p: validated_data.get(p) for p in percentage_params if p in validated_data}
            
            if len(percentages) >= 3:
                total_percent = sum(percentages.values())
                if abs(total_percent - 100) > 10:
                    logger.warning(f"Differential percentages sum to {total_percent}%, expected ~100%")
                    # Normalize if close to 100
                    if 85 <= total_percent <= 115:
                        factor = 100 / total_percent
                        for param in percentages:
                            validated_data[param] = round(validated_data[param] * factor, 1)
            
            # Cross-validate absolute counts with percentages and WBC
            if 'WBC' in validated_data:
                wbc = validated_data['WBC']
                
                for pct_param in percentage_params:
                    abs_param = pct_param.replace('%', '#')
                    
                    if pct_param in validated_data and abs_param not in validated_data:
                        # Calculate absolute count from percentage
                        percentage = validated_data[pct_param]
                        absolute_count = (percentage / 100) * wbc
                        if self._validate_range(abs_param, absolute_count):
                            validated_data[abs_param] = round(absolute_count, 2)
                    
                    elif abs_param in validated_data and pct_param not in validated_data:
                        # Calculate percentage from absolute count
                        absolute_count = validated_data[abs_param]
                        percentage = (absolute_count / wbc) * 100
                        if self._validate_range(pct_param, percentage):
                            validated_data[pct_param] = round(percentage, 1)
            
            # Validate RBC indices consistency
            if all(param in validated_data for param in ['RBC', 'HGB', 'HCT']):
                rbc, hgb, hct = validated_data['RBC'], validated_data['HGB'], validated_data['HCT']
                
                # Calculate MCV if missing (HCT / RBC * 10)
                if 'MCV' not in validated_data:
                    calculated_mcv = (hct / rbc) * 10
                    if self._validate_range('MCV', calculated_mcv):
                        validated_data['MCV'] = round(calculated_mcv, 1)
                
                # Calculate MCH if missing (HGB / RBC * 10)
                if 'MCH' not in validated_data:
                    calculated_mch = (hgb / rbc) * 10
                    if self._validate_range('MCH', calculated_mch):
                        validated_data['MCH'] = round(calculated_mch, 1)
                
                # Calculate MCHC if missing (HGB / HCT * 100)
                if 'MCHC' not in validated_data:
                    calculated_mchc = (hgb / hct) * 100
                    if self._validate_range('MCHC', calculated_mchc):
                        validated_data['MCHC'] = round(calculated_mchc, 1)
            
            # Add metadata
            validated_data['_extraction_timestamp'] = datetime.now().isoformat()
            validated_data['_parameters_found'] = len([k for k in validated_data.keys() if not k.startswith('_')])
            validated_data['_completeness'] = (len([k for k in validated_data.keys() if not k.startswith('_')]) / len(self.cbc_params)) * 100
            
            return validated_data
            
        except Exception as e:
            logger.error(f"Cross-validation error: {e}")
            return extracted_data