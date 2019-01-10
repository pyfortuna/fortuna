# Import Libraries
from fpdf import FPDF
import fortunacommon as fc

# Create PDF
pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=12)
pdf.cell(20, 20, 'Ashok Leyland')
pdf.image('/home/ec2-user/plutus/smaplot003.png', x=20, y=40, w=170, h=110)
pdf.image('/home/ec2-user/plutus/candleplot003.png', x=20, y=160, w=170, h=110)
pdf.output('/home/ec2-user/plutus/testpdf.pdf')

# Send Mail
fc.sendMail('PDF','test pdf','/home/ec2-user/plutus/testpdf.pdf')
