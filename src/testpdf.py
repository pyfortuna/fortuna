# Import Libraries
from fpdf import FPDF
import fortunacommon as fc

# Create PDF
pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=12)
pdf.write(5, 'Ashok Leyland')
pdf.image('/home/ec2-user/plutus/smaplot003.png', w=150)
pdf.image('/home/ec2-user/plutus/candleplot003.png', w=150)
pdf.output('/home/ec2-user/plutus/testpdf.pdf')

# Send Mail
fc.sendMail('PDF','test pdf','/home/ec2-user/plutus/testpdf.pdf')
