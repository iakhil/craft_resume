from flask import Flask, request, jsonify, send_file
from fpdf import FPDF
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Resume', border=False, ln=True, align='C')
        self.ln(10)

    def section_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, title, ln=True, align='L')
        self.ln(5)

    def section_body(self, body):
        self.set_font('Arial', '', 12)
        self.multi_cell(0, 10, body.encode('latin-1', 'replace').decode('latin-1'))
        self.ln()

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    pdf = PDF()
    pdf.add_page()

    # Adding sections
    for section, content in data.items():
        pdf.section_title(section.capitalize())
        pdf.section_body(content)

    # Save the PDF to a temporary file
    filename = 'resume.pdf'
    pdf.output(filename)

    # Return the file for download
    return send_file(filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
