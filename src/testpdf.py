# Import Libraries
from fpdf import FPDF
import fortunacommon as fc

# Create PDF
pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=12)
pdf.cell(10, 10, 'Ashok Leyland')
pdf.image('/home/ec2-user/plutus/smaplot003.png', x=10, y=30, w=190, h=120)
pdf.image('/home/ec2-user/plutus/candleplot003.png', x=10, y=160, w=190, h=120)
pdf.output('/home/ec2-user/plutus/testpdf.pdf')

# Send Mail
fc.sendMail('PDF','test pdf','/home/ec2-user/plutus/testpdf.pdf')
