#!/usr/bin/python

import smtplib

sender = 'mark.guthrie@17ways.com.au'
receivers = ['mark.guthrie@17ways.com.au']

message = """From: Mr Spock <mark.guthrie@17ways.com.au>
To: To Person <mark.guthrie@17ways.com.au>
MIME-Version: 1.0
Content-type: text/html
Subject: SMTP HTML e-mail test

  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <meta name="viewport" content="width=device-width" />
  </head>
  <body style="width: 100% !important; min-width: 100%; -webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; color: #222222; font-family: 'Helvetica', 'Arial', sans-serif; font-weight: normal; text-align: left; line-height: 19px; font-size: 14px; margin: 0; padding: 0;"><style type="text/css">
a:hover { color: #2795b6 !important; }
a:active { color: #2795b6 !important; }
a:visited { color: #2ba6cb !important; }
h1 a:active { color: #2ba6cb !important; }
h2 a:active { color: #2ba6cb !important; }
h3 a:active { color: #2ba6cb !important; }
h4 a:active { color: #2ba6cb !important; }
h5 a:active { color: #2ba6cb !important; }
h6 a:active { color: #2ba6cb !important; }
h1 a:visited { color: #2ba6cb !important; }
h2 a:visited { color: #2ba6cb !important; }
h3 a:visited { color: #2ba6cb !important; }
h4 a:visited { color: #2ba6cb !important; }
h5 a:visited { color: #2ba6cb !important; }
h6 a:visited { color: #2ba6cb !important; }
table.button:hover td { background: #2795b6 !important; }
table.button:visited td { background: #2795b6 !important; }
table.button:active td { background: #2795b6 !important; }
table.button:hover td a { color: #fff !important; }
table.button:visited td a { color: #fff !important; }
table.button:active td a { color: #fff !important; }
table.button:hover td { background: #2795b6 !important; }
table.tiny-button:hover td { background: #2795b6 !important; }
table.small-button:hover td { background: #2795b6 !important; }
table.medium-button:hover td { background: #2795b6 !important; }
table.large-button:hover td { background: #2795b6 !important; }
table.button:hover td a { color: #ffffff !important; }
table.button:active td a { color: #ffffff !important; }
table.button td a:visited { color: #ffffff !important; }
table.tiny-button:hover td a { color: #ffffff !important; }
table.tiny-button:active td a { color: #ffffff !important; }
table.tiny-button td a:visited { color: #ffffff !important; }
table.small-button:hover td a { color: #ffffff !important; }
table.small-button:active td a { color: #ffffff !important; }
table.small-button td a:visited { color: #ffffff !important; }
table.medium-button:hover td a { color: #ffffff !important; }
table.medium-button:active td a { color: #ffffff !important; }
table.medium-button td a:visited { color: #ffffff !important; }
table.large-button:hover td a { color: #ffffff !important; }
table.large-button:active td a { color: #ffffff !important; }
table.large-button td a:visited { color: #ffffff !important; }
table.secondary:hover td { background: #d0d0d0 !important; color: #555 !important; }
table.secondary:hover td a { color: #555 !important; }
table.secondary td a:visited { color: #555 !important; }
table.secondary:active td a { color: #555 !important; }
table.success:hover td { background: #457a1a !important; }
table.alert:hover td { background: #970b0e !important; }
table.facebook:hover td { background: #2d4473 !important; }
table.twitter:hover td { background: #0087bb !important; }
table.google-plus:hover td { background: #CC0000 !important; }
&gt;</style>&#13;
	<table class="body" style="border-spacing: 0; border-collapse: collapse; vertical-align: top; text-align: left; height: 100%; width: 100%; color: #222222; font-family: 'Helvetica', 'Arial', sans-serif; font-weight: normal; line-height: 19px; font-size: 14px; margin: 0; padding: 0;"><tr style="vertical-align: top; text-align: left; padding: 0;" align="left"><td class="center" align="center" valign="top" style="word-break: break-word; -webkit-hyphens: auto; -moz-hyphens: auto; hyphens: auto; border-collapse: collapse !important; vertical-align: top; text-align: center; color: #222222; font-family: 'Helvetica', 'Arial', sans-serif; font-weight: normal; line-height: 19px; font-size: 14px; margin: 0; padding: 0;">&#13;
        <center style="width: 100%; min-width: 0 !important;">&#13;
&#13;
&#13;
          <table class="row header" style="border-spacing: 0; border-collapse: collapse; vertical-align: top; text-align: left; width: 100% !important; position: relative; display: block !important; background-color: #999999; padding: 0px;" bgcolor="#999999"><tr style="vertical-align: top; text-align: left; padding: 0;" align="left"><td class="center" align="center" style="word-break: break-word; -webkit-hyphens: auto; -moz-hyphens: auto; hyphens: auto; border-collapse: collapse !important; vertical-align: top; text-align: center; color: #222222; font-family: 'Helvetica', 'Arial', sans-serif; font-weight: normal; line-height: 19px; font-size: 14px; margin: 0; padding: 0;" valign="top">&#13;
                <center style="width: 100%; min-width: 0 !important;">&#13;
&#13;
                  <table class="container" style="border-spacing: 0; border-collapse: collapse; vertical-align: top; text-align: inherit; width: 95% !important; margin: 0 auto; padding: 0;"><tr style="vertical-align: top; text-align: left; padding: 0;" align="left"><td class="wrapper last" style="word-break: break-word; -webkit-hyphens: auto; -moz-hyphens: auto; hyphens: auto; border-collapse: collapse !important; vertical-align: top; text-align: left; position: relative; color: #222222; font-family: 'Helvetica', 'Arial', sans-serif; font-weight: normal; line-height: 19px; font-size: 14px; display: block !important; margin: 0; padding: 10px 0 0px 0px;" align="left" valign="top">&#13;
&#13;
                        <table class="twelve columns" style="border-spacing: 0; border-collapse: collapse; vertical-align: top; text-align: left; width: 100% !important; table-layout: fixed !important; float: none !important; display: block !important; margin: 0 auto; padding: 0 0px;"><tr style="vertical-align: top; text-align: left; padding: 0;" align="left"><td class="six sub-columns" style="word-break: break-word; -webkit-hyphens: auto; -moz-hyphens: auto; hyphens: auto; border-collapse: collapse !important; vertical-align: top; text-align: left; min-width: 0px; width: 50% !important; color: #222222; font-family: 'Helvetica', 'Arial', sans-serif; font-weight: normal; line-height: 19px; font-size: 14px; margin: 0; padding: 0px 10px 10px 0px;" align="left" valign="top">&#13;
                              <img src="http://placehold.it/200x50" style="outline: none; text-decoration: none; -ms-interpolation-mode: bicubic; width: auto !important; max-width: 100%; float: left; clear: both; display: block; height: auto !important;" align="left" /></td>&#13;
                            <td class="six sub-columns last" align="right" style="text-align: right; vertical-align: middle; word-break: break-word; -webkit-hyphens: auto; -moz-hyphens: auto; hyphens: auto; border-collapse: collapse !important; min-width: 0px; width: 50% !important; color: #222222; font-family: 'Helvetica', 'Arial', sans-serif; font-weight: normal; line-height: 19px; font-size: 14px; margin: 0; padding: 0px 0px 10px;" valign="middle">&#13;
                              <span class="template-label" style="color: #ffffff; font-weight: bold; font-size: 11px;">HERO</span>&#13;
                            </td>&#13;
                            <td class="expander" style="word-break: break-word; -webkit-hyphens: auto; -moz-hyphens: auto; hyphens: auto; border-collapse: collapse !important; vertical-align: top; text-align: left; visibility: hidden; width: 1px !important; color: #222222; font-family: 'Helvetica', 'Arial', sans-serif; font-weight: normal; line-height: 19px; font-size: 14px; margin: 0; padding: 0;" align="left" valign="top"></td>&#13;
&#13;
                          </tr></table></td>&#13;
                    </tr></table></center>&#13;
              </td>&#13;
            </tr></table><br /><table class="container" style="border-spacing: 0; border-collapse: collapse; vertical-align: top; text-align: inherit; width: 95% !important; margin: 0 auto; padding: 0;"><tr style="vertical-align: top; text-align: left; padding: 0;" align="left"><td style="word-break: break-word; -webkit-hyphens: auto; -moz-hyphens: auto; hyphens: auto; border-collapse: collapse !important; vertical-align: top; text-align: left; color: #222222; font-family: 'Helvetica', 'Arial', sans-serif; font-weight: normal; line-height: 19px; font-size: 14px; margin: 0; padding: 0;" align="left" valign="top">&#13;
&#13;
                <!-- content start -->&#13;
                <table class="row" style="border-spacing: 0; border-collapse: collapse; vertical-align: top; text-align: left; width: 100% !important; position: relative; display: block !important; padding: 0px;"><tr style="vertical-align: top; text-align: left; padding: 0;" align="left"><td class="wrapper last" style="word-break: break-word; -webkit-hyphens: auto; -moz-hyphens: auto; hyphens: auto; border-collapse: collapse !important; vertical-align: top; text-align: left; position: relative; color: #222222; font-family: 'Helvetica', 'Arial', sans-serif; font-weight: normal; line-height: 19px; font-size: 14px; display: block !important; margin: 0; padding: 10px 0 0px 0px;" align="left" valign="top">&#13;
&#13;
                      <table class="twelve columns" style="border-spacing: 0; border-collapse: collapse; vertical-align: top; text-align: left; width: 100% !important; table-layout: fixed !important; float: none !important; display: block !important; margin: 0 auto; padding: 0 0px;"><tr style="vertical-align: top; text-align: left; padding: 0;" align="left"><td style="word-break: break-word; -webkit-hyphens: auto; -moz-hyphens: auto; hyphens: auto; border-collapse: collapse !important; vertical-align: top; text-align: left; color: #222222; font-family: 'Helvetica', 'Arial', sans-serif; font-weight: normal; line-height: 19px; font-size: 14px; width: 100% !important; margin: 0; padding: 0px 0px 10px;" align="left" valign="top">&#13;
&#13;
                            <h1 style="color: #222222; font-family: 'Helvetica', 'Arial', sans-serif; font-weight: normal; text-align: left; line-height: 1.3; word-break: normal; font-size: 40px; margin: 0; padding: 0;" align="left">Hi, Elijah Baily</h1>&#13;
                						<p class="lead" style="color: #222222; font-family: 'Helvetica', 'Arial', sans-serif; font-weight: normal; text-align: left; line-height: 21px; font-size: 18px; margin: 0 0 10px; padding: 0;" align="left">Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et.</p>&#13;
                						<img width="580" height="300" src="http://placehold.it/580x300" style="outline: none; text-decoration: none; -ms-interpolation-mode: bicubic; width: auto !important; max-width: 100%; float: left; clear: both; display: block; height: auto !important;" align="left" /></td>&#13;
                          <td class="expander" style="word-break: break-word; -webkit-hyphens: auto; -moz-hyphens: auto; hyphens: auto; border-collapse: collapse !important; vertical-align: top; text-align: left; visibility: hidden; width: 1px !important; color: #222222; font-family: 'Helvetica', 'Arial', sans-serif; font-weight: normal; line-height: 19px; font-size: 14px; margin: 0; padding: 0;" align="left" valign="top"></td>&#13;
                        </tr></table></td>&#13;
                  </tr></table><table class="row callout" style="border-spacing: 0; border-collapse: collapse; vertical-align: top; text-align: left; width: 100% !important; position: relative; display: block !important; padding: 0px;"><tr style="vertical-align: top; text-align: left; padding: 0;" align="left"><td class="wrapper last" style="word-break: break-word; -webkit-hyphens: auto; -moz-hyphens: auto; hyphens: auto; border-collapse: collapse !important; vertical-align: top; text-align: left; position: relative; color: #222222; font-family: 'Helvetica', 'Arial', sans-serif; font-weight: normal; line-height: 19px; font-size: 14px; display: block !important; margin: 0; padding: 10px 0 0px 0px;" align="left" valign="top">&#13;
&#13;
                      <table class="twelve columns" style="border-spacing: 0; border-collapse: collapse; vertical-align: top; text-align: left; width: 100% !important; table-layout: fixed !important; float: none !important; display: block !important; margin: 0 auto; padding: 0 0px;"><tr style="vertical-align: top; text-align: left; padding: 0;" align="left"><td class="panel" style="word-break: break-word; -webkit-hyphens: auto; -moz-hyphens: auto; hyphens: auto; border-collapse: collapse !important; vertical-align: top; text-align: left; color: #222222; font-family: 'Helvetica', 'Arial', sans-serif; font-weight: normal; line-height: 19px; font-size: 14px; width: 100% !important; background-color: #ECF8FF; margin: 0; padding: 10px; border: 1px solid #b9e5ff;" align="left" bgcolor="#ECF8FF" valign="top">&#13;
&#13;
                          </td>&#13;
                          <td class="expander" style="word-break: break-word; -webkit-hyphens: auto; -moz-hyphens: auto; hyphens: auto; border-collapse: collapse !important; vertical-align: top; text-align: left; visibility: hidden; width: 1px !important; color: #222222; font-family: 'Helvetica', 'Arial', sans-serif; font-weight: normal; line-height: 19px; font-size: 14px; margin: 0; padding: 0;" align="left" valign="top"></td>&#13;
                        </tr></table></td>&#13;
                  </tr></table><table class="row" style="border-spacing: 0; border-collapse: collapse; vertical-align: top; text-align: left; width: 100% !important; position: relative; display: block !important; padding: 0px;"><tr style="vertical-align: top; text-align: left; padding: 0;" align="left"><td class="wrapper last" style="word-break: break-word; -webkit-hyphens: auto; -moz-hyphens: auto; hyphens: auto; border-collapse: collapse !important; vertical-align: top; text-align: left; position: relative; color: #222222; font-family: 'Helvetica', 'Arial', sans-serif; font-weight: normal; line-height: 19px; font-size: 14px; display: block !important; margin: 0; padding: 10px 0 0px 0px;" align="left" valign="top">&#13;
&#13;
                      <table class="twelve columns" style="border-spacing: 0; border-collapse: collapse; vertical-align: top; text-align: left; width: 100% !important; table-layout: fixed !important; float: none !important; display: block !important; margin: 0 auto; padding: 0 0px;"><tr style="vertical-align: top; text-align: left; padding: 0;" align="left"><td style="word-break: break-word; -webkit-hyphens: auto; -moz-hyphens: auto; hyphens: auto; border-collapse: collapse !important; vertical-align: top; text-align: left; color: #222222; font-family: 'Helvetica', 'Arial', sans-serif; font-weight: normal; line-height: 19px; font-size: 14px; width: 100% !important; margin: 0; padding: 0px 0px 10px;" align="left" valign="top">&#13;
&#13;
                            <h3 style="color: #222222; font-family: 'Helvetica', 'Arial', sans-serif; font-weight: normal; text-align: left; line-height: 1.3; word-break: normal; font-size: 32px; margin: 0; padding: 0;" align="left">Title Ipsum <small style="font-size: 10px;">This is a note.</small></h3>&#13;
                            <p style="color: #222222; font-family: 'Helvetica', 'Arial', sans-serif; font-weight: normal; text-align: left; line-height: 19px; font-size: 14px; margin: 0 0 10px; padding: 0;" align="left">Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.</p>&#13;
&#13;
                          </td>&#13;
                          <td class="expander" style="word-break: break-word; -webkit-hyphens: auto; -moz-hyphens: auto; hyphens: auto; border-collapse: collapse !important; vertical-align: top; text-align: left; visibility: hidden; width: 1px !important; color: #222222; font-family: 'Helvetica', 'Arial', sans-serif; font-weight: normal; line-height: 19px; font-size: 14px; margin: 0; padding: 0;" align="left" valign="top"></td>&#13;
                        </tr></table></td>&#13;
                  </tr></table><table class="row" style="border-spacing: 0; border-collapse: collapse; vertical-align: top; text-align: left; width: 100% !important; position: relative; display: block !important; padding: 0px;"><tr style="vertical-align: top; text-align: left; padding: 0;" align="left"><td class="wrapper last" style="word-break: break-word; -webkit-hyphens: auto; -moz-hyphens: auto; hyphens: auto; border-collapse: collapse !important; vertical-align: top; text-align: left; position: relative; color: #222222; font-family: 'Helvetica', 'Arial', sans-serif; font-weight: normal; line-height: 19px; font-size: 14px; display: block !important; margin: 0; padding: 10px 0 0px 0px;" align="left" valign="top">&#13;
&#13;
                      <table class="three columns" style="border-spacing: 0; border-collapse: collapse; vertical-align: top; text-align: left; width: 100% !important; table-layout: fixed !important; float: none !important; display: block !important; margin: 0 auto; padding: 0 0px;"><tr style="vertical-align: top; text-align: left; padding: 0;" align="left"><td style="word-break: break-word; -webkit-hyphens: auto; -moz-hyphens: auto; hyphens: auto; border-collapse: collapse !important; vertical-align: top; text-align: left; color: #222222; font-family: 'Helvetica', 'Arial', sans-serif; font-weight: normal; line-height: 19px; font-size: 14px; width: 100% !important; margin: 0; padding: 0px 0px 10px;" align="left" valign="top">&#13;
&#13;
                            <table class="button" style="border-spacing: 0; border-collapse: collapse; vertical-align: top; text-align: left; width: 100%; overflow: hidden; padding: 0;"><tr style="vertical-align: top; text-align: left; padding: 0;" align="left"><td style="word-break: break-word; -webkit-hyphens: auto; -moz-hyphens: auto; hyphens: auto; border-collapse: collapse !important; vertical-align: top; text-align: center; color: #ffffff; font-family: 'Helvetica', 'Arial', sans-serif; font-weight: normal; line-height: 19px; font-size: 14px; display: block; width: 100% !important; background-color: #2ba6cb; margin: 0; padding: 8px 0; border: 1px solid #2284a1;" align="center" bgcolor="#2ba6cb" valign="top">&#13;
                                  <a href="#" style="color: #ffffff; text-decoration: none; font-weight: bold; font-family: Helvetica, Arial, sans-serif; font-size: 16px;">Click Me!</a>&#13;
                                </td>&#13;
                              </tr></table></td>&#13;
                          <td class="expander" style="word-break: break-word; -webkit-hyphens: auto; -moz-hyphens: auto; hyphens: auto; border-collapse: collapse !important; vertical-align: top; text-align: left; visibility: hidden; width: 1px !important; color: #222222; font-family: 'Helvetica', 'Arial', sans-serif; font-weight: normal; line-height: 19px; font-size: 14px; margin: 0; padding: 0;" align="left" valign="top"></td>&#13;
                        </tr></table></td>&#13;
                  </tr></table><table class="row footer" style="border-spacing: 0; border-collapse: collapse; vertical-align: top; text-align: left; width: 100% !important; position: relative; display: block !important; padding: 0px;"><tr style="vertical-align: top; text-align: left; padding: 0;" align="left"><td class="wrapper" style="word-break: break-word; -webkit-hyphens: auto; -moz-hyphens: auto; hyphens: auto; border-collapse: collapse !important; vertical-align: top; text-align: left; position: relative; color: #222222; font-family: 'Helvetica', 'Arial', sans-serif; font-weight: normal; line-height: 19px; font-size: 14px; display: block !important; background-color: #ebebeb; margin: 0; padding: 10px 0 0px 0px;" align="left" bgcolor="#ebebeb" valign="top">&#13;
&#13;
                      <table class="six columns" style="border-spacing: 0; border-collapse: collapse; vertical-align: top; text-align: left; width: 100% !important; table-layout: fixed !important; float: none !important; display: block !important; margin: 0 auto; padding: 0 0px;"><tr style="vertical-align: top; text-align: left; padding: 0;" align="left"><td class="left-text-pad" style="word-break: break-word; -webkit-hyphens: auto; -moz-hyphens: auto; hyphens: auto; border-collapse: collapse !important; vertical-align: top; text-align: left; color: #222222; font-family: 'Helvetica', 'Arial', sans-serif; font-weight: normal; line-height: 19px; font-size: 14px; width: 100% !important; margin: 0; padding: 0px 10px 10px;" align="left" valign="top">&#13;
&#13;
                            <h5 style="color: #222222; font-family: 'Helvetica', 'Arial', sans-serif; font-weight: normal; text-align: left; line-height: 1.3; word-break: normal; font-size: 24px; margin: 0; padding: 0 0 10px;" align="left">Connect With Us:</h5>&#13;
&#13;
                            <table class="tiny-button facebook" style="border-spacing: 0; border-collapse: collapse; vertical-align: top; text-align: left; width: 100%; overflow: hidden; padding: 0;"><tr style="vertical-align: top; text-align: left; padding: 0;" align="left"><td style="word-break: break-word; -webkit-hyphens: auto; -moz-hyphens: auto; hyphens: auto; border-collapse: collapse !important; vertical-align: top; text-align: center; color: #ffffff; font-family: 'Helvetica', 'Arial', sans-serif; font-weight: normal; line-height: 19px; font-size: 14px; display: block; width: 100% !important; background-color: #3b5998; margin: 0; padding: 5px 0 4px; border: 1px solid #2d4473;" align="center" bgcolor="#3b5998" valign="top">&#13;
                                  <a href="#" style="color: #ffffff; text-decoration: none; font-weight: normal; font-family: Helvetica, Arial, sans-serif; font-size: 12px;">Facebook</a>&#13;
                                </td>&#13;
                              </tr></table><br /><table class="tiny-button twitter" style="border-spacing: 0; border-collapse: collapse; vertical-align: top; text-align: left; width: 100%; overflow: hidden; padding: 0;"><tr style="vertical-align: top; text-align: left; padding: 0;" align="left"><td style="word-break: break-word; -webkit-hyphens: auto; -moz-hyphens: auto; hyphens: auto; border-collapse: collapse !important; vertical-align: top; text-align: center; color: #ffffff; font-family: 'Helvetica', 'Arial', sans-serif; font-weight: normal; line-height: 19px; font-size: 14px; display: block; width: 100% !important; background-color: #00acee; margin: 0; padding: 5px 0 4px; border: 1px solid #0087bb;" align="center" bgcolor="#00acee" valign="top">&#13;
                                  <a href="#" style="color: #ffffff; text-decoration: none; font-weight: normal; font-family: Helvetica, Arial, sans-serif; font-size: 12px;">Twitter</a>&#13;
                                </td>&#13;
                              </tr></table><br /><table class="tiny-button google-plus" style="border-spacing: 0; border-collapse: collapse; vertical-align: top; text-align: left; width: 100%; overflow: hidden; padding: 0;"><tr style="vertical-align: top; text-align: left; padding: 0;" align="left"><td style="word-break: break-word; -webkit-hyphens: auto; -moz-hyphens: auto; hyphens: auto; border-collapse: collapse !important; vertical-align: top; text-align: center; color: #ffffff; font-family: 'Helvetica', 'Arial', sans-serif; font-weight: normal; line-height: 19px; font-size: 14px; display: block; width: 100% !important; background-color: #DB4A39; margin: 0; padding: 5px 0 4px; border: 1px solid #cc0000;" align="center" bgcolor="#DB4A39" valign="top">&#13;
                                  <a href="#" style="color: #ffffff; text-decoration: none; font-weight: normal; font-family: Helvetica, Arial, sans-serif; font-size: 12px;">Google +</a>&#13;
                                </td>&#13;
                              </tr></table></td>&#13;
                          <td class="expander" style="word-break: break-word; -webkit-hyphens: auto; -moz-hyphens: auto; hyphens: auto; border-collapse: collapse !important; vertical-align: top; text-align: left; visibility: hidden; width: 1px !important; color: #222222; font-family: 'Helvetica', 'Arial', sans-serif; font-weight: normal; line-height: 19px; font-size: 14px; margin: 0; padding: 0;" align="left" valign="top"></td>&#13;
                        </tr></table></td>&#13;
                    <td class="wrapper last" style="word-break: break-word; -webkit-hyphens: auto; -moz-hyphens: auto; hyphens: auto; border-collapse: collapse !important; vertical-align: top; text-align: left; position: relative; color: #222222; font-family: 'Helvetica', 'Arial', sans-serif; font-weight: normal; line-height: 19px; font-size: 14px; display: block !important; background-color: #ebebeb; margin: 0; padding: 10px 0 0px 0px;" align="left" bgcolor="#ebebeb" valign="top">&#13;
&#13;
                      <table class="six columns" style="border-spacing: 0; border-collapse: collapse; vertical-align: top; text-align: left; width: 100% !important; table-layout: fixed !important; float: none !important; display: block !important; margin: 0 auto; padding: 0 0px;"><tr style="vertical-align: top; text-align: left; padding: 0;" align="left"><td class="last right-text-pad" style="word-break: break-word; -webkit-hyphens: auto; -moz-hyphens: auto; hyphens: auto; border-collapse: collapse !important; vertical-align: top; text-align: left; color: #222222; font-family: 'Helvetica', 'Arial', sans-serif; font-weight: normal; line-height: 19px; font-size: 14px; width: 100% !important; margin: 0; padding: 0px 0px 10px 10px;" align="left" valign="top">&#13;
                            <h5 style="color: #222222; font-family: 'Helvetica', 'Arial', sans-serif; font-weight: normal; text-align: left; line-height: 1.3; word-break: normal; font-size: 24px; margin: 0; padding: 0 0 10px;" align="left">Contact Info:</h5>&#13;
                            <p style="color: #222222; font-family: 'Helvetica', 'Arial', sans-serif; font-weight: normal; text-align: left; line-height: 19px; font-size: 14px; margin: 0 0 10px; padding: 0;" align="left">Phone: 408.341.0600</p>&#13;
                            <p style="color: #222222; font-family: 'Helvetica', 'Arial', sans-serif; font-weight: normal; text-align: left; line-height: 19px; font-size: 14px; margin: 0 0 10px; padding: 0;" align="left">Email: <a href="mailto:hseldon@trantor.com" style="color: #2ba6cb; text-decoration: none;">hseldon@trantor.com</a></p>&#13;
                          </td>&#13;
                          <td class="expander" style="word-break: break-word; -webkit-hyphens: auto; -moz-hyphens: auto; hyphens: auto; border-collapse: collapse !important; vertical-align: top; text-align: left; visibility: hidden; width: 1px !important; color: #222222; font-family: 'Helvetica', 'Arial', sans-serif; font-weight: normal; line-height: 19px; font-size: 14px; margin: 0; padding: 0;" align="left" valign="top"></td>&#13;
                        </tr></table></td>&#13;
                  </tr></table><table class="row" style="border-spacing: 0; border-collapse: collapse; vertical-align: top; text-align: left; width: 100% !important; position: relative; display: block !important; padding: 0px;"><tr style="vertical-align: top; text-align: left; padding: 0;" align="left"><td class="wrapper last" style="word-break: break-word; -webkit-hyphens: auto; -moz-hyphens: auto; hyphens: auto; border-collapse: collapse !important; vertical-align: top; text-align: left; position: relative; color: #222222; font-family: 'Helvetica', 'Arial', sans-serif; font-weight: normal; line-height: 19px; font-size: 14px; display: block !important; margin: 0; padding: 10px 0 0px 0px;" align="left" valign="top">&#13;
&#13;
                      <table class="twelve columns" style="border-spacing: 0; border-collapse: collapse; vertical-align: top; text-align: left; width: 100% !important; table-layout: fixed !important; float: none !important; display: block !important; margin: 0 auto; padding: 0 0px;"><tr style="vertical-align: top; text-align: left; padding: 0;" align="left"><td align="center" style="word-break: break-word; -webkit-hyphens: auto; -moz-hyphens: auto; hyphens: auto; border-collapse: collapse !important; vertical-align: top; text-align: left; color: #222222; font-family: 'Helvetica', 'Arial', sans-serif; font-weight: normal; line-height: 19px; font-size: 14px; width: 100% !important; margin: 0; padding: 0px 0px 10px;" valign="top">&#13;
                            <center style="width: 100%; min-width: 0 !important;">&#13;
                              <p style="text-align: center; color: #222222; font-family: 'Helvetica', 'Arial', sans-serif; font-weight: normal; line-height: 19px; font-size: 14px; margin: 0 0 10px; padding: 0;" align="center"><a href="#" style="color: #2ba6cb; text-decoration: none;">Terms</a> | <a href="#" style="color: #2ba6cb; text-decoration: none;">Privacy</a> | <a href="#" style="color: #2ba6cb; text-decoration: none;">Unsubscribe</a></p>&#13;
                            </center>&#13;
                          </td>&#13;
                          <td class="expander" style="word-break: break-word; -webkit-hyphens: auto; -moz-hyphens: auto; hyphens: auto; border-collapse: collapse !important; vertical-align: top; text-align: left; visibility: hidden; width: 1px !important; color: #222222; font-family: 'Helvetica', 'Arial', sans-serif; font-weight: normal; line-height: 19px; font-size: 14px; margin: 0; padding: 0;" align="left" valign="top"></td>&#13;
                        </tr></table></td>&#13;
                  </tr></table><!-- container end below --></td>&#13;
            </tr></table></center>&#13;
			</td>&#13;
		</tr></table></body>
</html>


"""


try:
   smtpObj = smtplib.SMTP('localhost')
   smtpObj.sendmail(sender, receivers, message)         
   print "Successfully sent email"
except SMTPException:
   print "Error: unable to send email"