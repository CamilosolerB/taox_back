import pandas as pd
import io
import csv
from typing import List, Dict, Any
from fpdf import FPDF

class ReportService:
    @staticmethod
    def generate_excel(data: List[Dict[str, Any]]) -> io.BytesIO:
        """Generates an Excel file from a list of dictionaries."""
        df = pd.DataFrame(data)
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Report')
        output.seek(0)
        return output

    @staticmethod
    def generate_csv(data: List[Dict[str, Any]]) -> io.StringIO:
        """Generates a CSV file from a list of dictionaries."""
        output = io.StringIO()
        if not data:
            return output
            
        fieldnames = data[0].keys()
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)
            
        output.seek(0)
        return output

    @staticmethod
    def generate_pdf(data: List[Dict[str, Any]], title: str = "Report") -> io.BytesIO:
        """Generates a PDF file from a list of dictionaries."""
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("helvetica", size=12)
        pdf.cell(0, 10, text=title, new_x="LMARGIN", new_y="NEXT", align='C')
        
        if not data:
            pdf.cell(0, 10, text="No data available", new_x="LMARGIN", new_y="NEXT", align='C')
            output = io.BytesIO(pdf.output())
            output.seek(0)
            return output
            
        # Basic PDF layout for table
        pdf.set_font("helvetica", size=8)
        
        # Determine column widths roughly
        headers = list(data[0].keys())
        col_width = pdf.epw / len(headers)
        
        # Header
        pdf.set_font("helvetica", 'B', 8)
        for header in headers:
            pdf.cell(col_width, 10, str(header)[:15], border=1)
        pdf.ln()
        
        # Data
        pdf.set_font("helvetica", '', 8)
        for row in data:
            for header in headers:
                val = str(row.get(header, ''))
                # Replace unsupported characters or handle unicode if necessary (helvetica is standard latin-1)
                safe_val = val.encode('latin-1', 'replace').decode('latin-1')
                pdf.cell(col_width, 10, safe_val[:15], border=1)
            pdf.ln()

        output = io.BytesIO(pdf.output())
        output.seek(0)
        return output
