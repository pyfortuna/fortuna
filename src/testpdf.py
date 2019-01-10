from fpdf import FPDF
import fortunacommon as fc

pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=12)
pdf.cell(200, 10, txt="Welcome to Python!", ln=1, align="C")
pdf.output('/home/ec2-user/plutus/simple_demo.pdf')

fc.sendMail('PDF','test pdf','/home/ec2-user/plutus/simple_demo.pdf')
