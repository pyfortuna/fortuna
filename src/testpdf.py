# Import Libraries
import fortunacommon as fc
from fpdf import FPDF, HTMLMixin
 
class HTML2PDF(FPDF, HTMLMixin):
    pass
 
# Main Program
pdf = HTML2PDF()

table = """<table border="0" width="100%">
<thead><tr><th width="25%">Details</th><th width="15%">Mar '18</th><th width="15%">Mar '17</th><th width="15%">Mar '16</th><th width="15%">Mar '15</th><th width="15%">Mar '14</th></tr></thead>
<tbody>
<tr><td>Profit</td><td>1562.59</td><td>1223.08</td><td>389.6</td><td>334.81</td><td>29.38</td></tr>
<tr><td>EPS</td><td>5.34</td><td>4.24</td><td>1.37</td><td>1.2</td><td>0.11</td></tr>
</tbody>
</table>"""

pdf.add_page()
pdf.write_html(table)
pdf.output('/home/ec2-user/plutus/testpdf.pdf')

# Send Mail
fc.sendMail('PDF','test pdf','/home/ec2-user/plutus/testpdf.pdf')
