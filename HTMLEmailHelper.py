class HTMLEmailHelper:

# Put all of the mess in one place.
# lets you produce nicely formatted HTML emails using inline CSS

    def __init__(self, to, frm):

        self.to=to
        self.frm=frm

    def header(self, subject):
        msg="""From: %s <%s>
To: %s <%s>
MIME-Version: 1.0
Content-type: text/html
Subject: %s

  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <meta name="viewport" content="width=device-width" />
  </head>
  <body style="width: 100%%; min-width: 100%%; -webkit-text-size-adjust: 100%%; -ms-text-size-adjust: 100%%; color: #222222; font-family: 'Helvetica', 'Arial', sans-serif; font-weight: normal; text-align: left; line-height: 19px; font-size: 14px; margin: 0; padding: 0;">
  <style type="text/css">
a:hover { color: #2795b6; }
a:active { color: #2795b6; }
a:visited { color: #2ba6cb; }
h1 a:active { color: #2ba6cb; }
h2 a:active { color: #2ba6cb; }
h3 a:active { color: #2ba6cb; }
h4 a:active { color: #2ba6cb; }
h5 a:active { color: #2ba6cb; }
h6 a:active { color: #2ba6cb; }
h1 a:visited { color: #2ba6cb; }
h2 a:visited { color: #2ba6cb; }
h3 a:visited { color: #2ba6cb; }
h4 a:visited { color: #2ba6cb; }
h5 a:visited { color: #2ba6cb; }
h6 a:visited { color: #2ba6cb; }
table.button:hover td { background: #2795b6; }
table.button:visited td { background: #2795b6; }
table.button:active td { background: #2795b6; }
table.button:hover td a { color: #fff; }
table.button:visited td a { color: #fff; }
table.button:active td a { color: #fff; }
table.button:hover td { background: #2795b6; }
table.tiny-button:hover td { background: #2795b6; }
table.small-button:hover td { background: #2795b6; }
table.medium-button:hover td { background: #2795b6; }
table.large-button:hover td { background: #2795b6; }
table.button:hover td a { color: #ffffff; }
table.button:active td a { color: #ffffff; }
table.button td a:visited { color: #ffffff; }
table.tiny-button:hover td a { color: #ffffff; }
table.tiny-button:active td a { color: #ffffff; }
table.tiny-button td a:visited { color: #ffffff; }
table.small-button:hover td a { color: #ffffff; }
table.small-button:active td a { color: #ffffff; }
table.small-button td a:visited { color: #ffffff; }
table.medium-button:hover td a { color: #ffffff; }
table.medium-button:active td a { color: #ffffff; }
table.medium-button td a:visited { color: #ffffff; }
table.large-button:hover td a { color: #ffffff; }
table.large-button:active td a { color: #ffffff; }
table.large-button td a:visited { color: #ffffff; }
table.secondary:hover td { background: #d0d0d0; color: #555; }
table.secondary:hover td a { color: #555; }
table.secondary td a:visited { color: #555; }
table.secondary:active td a { color: #555; }
table.success:hover td { background: #457a1a; }
table.alert:hover td { background: #970b0e; }
table.facebook:hover td { background: #2d4473; }
table.twitter:hover td { background: #0087bb; }
table.google-plus:hover td { background: #CC0000; }
&gt;</style>&#13;""" % (self.frm["name"], self.frm["email"], self.to["name"], self.to["email"], subject)

        return(msg)

    def font(self):
        return("font-family: 'Helvetica', 'Arial', sans-serif; font-weight: normal; ")

    def i(self, txt):
        return("<i>%s</i><br><br>" % txt)

    def h1(self, txt):
        return("""<h1 style="color: #222222; font-family: 'Helvetica', 'Arial', sans-serif; font-weight: normal; text-align: left; line-height: 1.3; word-break: normal; font-size: 40px; margin: 0; padding: 0;" align="left">
        %s</h1>""" % txt)
    
    def h2(self, txt):
        return("""<br><br><hr><h2 style="color: #222222; font-family: 'Helvetica', 'Arial', sans-serif; font-weight: normal; text-align: left; line-height: 1.1; word-break: normal; font-size: 32px; margin: 0; padding: 0;" align="left">
        %s</h2><br>""" % txt)
    
    def img1(self,url):
        return("""<img width="580" height="300" src="%s" """ % url)

    def footer(self):
        return("</body>")


